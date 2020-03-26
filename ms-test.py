import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from NLP.processor import NBCModel

nbcModel = NBCModel(1,2,0.5)
print("training...")
nbcModel.learnfromfile("data/training-tweets.txt")
print("completed")
#pprint.pprint(nbcModel.counting_table.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(nbcModel.counting_table.total_language_count)
print("sum of all counts (all language):", nbcModel.counting_table.languages_sum_count)
print("classification:",nbcModel.classify("Ba dena aprobatzeko etxen geitubehar... ta eualdi honek re ezto launtzen... @AmaiaAuza"))