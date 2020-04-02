import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from NLP.processor import NBCModel

nbcModel = NBCModel(0,3,0.2)
print("training...")
nbcModel.learnfromfile("data/training-tweets.txt")
print("completed")
#pprint.pprint(nbcModel.counting_table.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(nbcModel.counting_table.total_language_count)
print("sum of all counts (all language):", nbcModel.counting_table.languages_sum_count)
# print("classification:",nbcModel.classify("Ba dena aprobatzeko etxen geitubehar... ta eualdi honek re ezto launtzen... @AmaiaAuza"))
# print("classification:",nbcModel.classify("Allen Iverson getting his number retired today! Just wish he could have got that ring in The Finals #TheAnswer #76ers http://t.co/vOgEnLfdKq"))
nbcModel.predict("data/test-tweets-given.txt")
