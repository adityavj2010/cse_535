'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

ps = PorterStemmer()


from collections import defaultdict
class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
    
        text = text.lower()
        text = re.sub('[^A-Za-z0-9]+', ' ', text)
        words = text.split()
        
        # words=[word.lower() for word in words if word.isalpha()]
        
        cnter = defaultdict(int)
        for w in words:
            if w not in self.stop_words:
                cnter[self.ps.stem(w)]+=1    
        return cnter.items()
        