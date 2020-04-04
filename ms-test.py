import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from NLP.nbcmodel import NBCModel

nbcModel = NBCModel(0,3,0.099)
print("training...")
nbcModel.learnFromFile("data/training-tweets.txt")
print("completed")
# pprint.pprint(nbcModel.counting_table.vocabulary_count)
print("tweets_per_class:")
pprint.pprint(nbcModel.counting_table.tweets_per_class)
print()
# print("classification:",nbcModel.classify("Ba dena aprobatzeko etxen geitubehar... ta eualdi honek re ezto launtzen... @AmaiaAuza"))
# print("classification:",nbcModel.classify("Allen Iverson getting his number retired today! Just wish he could have got that ring in The Finals #TheAnswer #76ers http://t.co/vOgEnLfdKq"))
nbcModel.predictFromFile("data/test-tweets-given.txt")
