from preprocessor import Preprocessor
from run_project import ProjectRunner

E_44588 = "Should Patients Receiving ACE Inhibitors or Angiotensin Receptor Blockers be Switched to Other Antihypertensive Drugs to Prevent or Improve Prognosis of Novel Coronavirus Disease 2019 (COVID-19)?"
E_89636 = "In Silico assessment of the impact of 2019 novel coronavirus (2019-nCoV) genomic variation on published real-time quantitative polymerase chain reaction detection assays"


E_81760 = "COVID-19 (Novel Coronavirus 2019) - recent trends"
E_69375 = "A novel human coronavirus: Middle East respiratory syndrome human coronavirus"

a = Preprocessor().tokenizer(E_81760)
b = Preprocessor().tokenizer(E_69375)

sum_a = sum(list(map(lambda s:s[1],a)))
sum_b = sum(list(map(lambda s:s[1],b)))

print('E_81760',1/len(a),1/sum_a)
print('E_69375',1/len(b),1/sum_b)

# pr = ProjectRunner()

# pr.run_indexer('./data/input_corpus.txt')
# pr._daat_and(['coronaviru','novel'],skip=True,sort=True)


# 81760 4.464285714285714

# 69375 4.464285714285714