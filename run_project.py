'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from os import link
from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self,ll1,ll2,skip = False):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        result = LinkedList()
        head1,head2 = ll1.start_node,ll2.start_node
        cnt = 0
        while head1 and head2:
            if head1.value == head2.value:
                cnt+=1
                result.insert_at_end((head2.value,max(head1.tf_idf,head2.tf_idf)))
                head1 = head1.next
                head2 = head2.next
            elif head1.value < head2.value:
                cnt+=1
                if skip and head1.skip and head1.skip.value<head2.value:
                    head1 = head1.skip
                    cnt+=1
                else:
                    head1 = head1.next
            else:
                cnt+=1
                if skip and head2.skip and head2.skip.value<head1.value:
                    head2 = head2.skip
                    cnt+=1
                else:
                    head2 = head2.next
        return result,cnt

    def _daat_and(self,query_terms,skip = False,sort = False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        if not query_terms:
            return [],0
        
        result = self.indexer.get_index()[query_terms[0]]
        cnt = 0
        for query in query_terms[1:]:
            result,n_cnt = self._merge(result,self.indexer.get_index()[query],skip)
            cnt+=n_cnt
        nodes = result.traverse_list()
        if sort:
            nodes = sorted(nodes,key=lambda a:a.tf_idf,reverse=True)
        return [node.value for node in result.traverse_list()],cnt

    def _get_postings(self,tern):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        self.indexer.get_index()[tern]
        

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            for line in tqdm(sorted(fp.readlines(),key = lambda line:int(line.split()[0]))):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                # print('tokenized_document',tokenized_document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        print("Adding skips")
        self.indexer.add_skip_connections()
        print("Calculating tf_idf")
        self.indexer.calculate_tf_idf()
        

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}
        
        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            

            input_term_arr = [term for term,_ in self.preprocessor.tokenizer(query)]  # Tokenized query. To be implemented.                        
            for term in input_term_arr:
                postings, skip_postings = None, None
                
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                postings = self.indexer.get_index()[term].traverse_list()
                skip_postings = self.indexer.get_index()[term].traverse_skips()
                
                output_dict['postingsList'][term] = list(map(lambda a:a.value,postings))
                output_dict['postingsListSkip'][term] = list(map(lambda a:a.value,skip_postings))
            
            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            and_op_no_skip,and_comparisons_no_skip = self._daat_and(input_term_arr)
            and_op_skip ,and_comparisons_skip = self._daat_and(input_term_arr,True)
            and_op_no_skip_sorted,and_comparisons_no_skip_sorted = self._daat_and(input_term_arr,False,True)
            and_op_skip_sorted,and_comparisons_skip_sorted =self._daat_and(input_term_arr,True,True)
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()
    
    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)
    print('dumped the dict')
    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.",default="./data/input_corpus.txt")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here",default="ajagtap")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)
    # print("started application")
    # print(runner.run_queries(["year"],"random"))
    app.run(host="0.0.0.0", port=9999,debug=False)
