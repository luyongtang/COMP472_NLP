import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from NLP.processor import NBCModel

nbcModel = NBCModel(1,3,0.5)

nbcModel.learnfromfile("data/training-tweets.txt")

print("sample couting")
pprint.pprint(nbcModel.counting_table.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(nbcModel.counting_table.total_language_count) 

exit(0)

sentence = "abédd"

print(SentenceParser.is_valid_char_functions[0]("a"))

sentenceParser = SentenceParser(1,2)

chars = sentenceParser.parseSentence(sentence)
print(chars)



countingtable = CountingTable(0)

countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abd","gl")
countingtable.addCount("hfg","en")
print("sample couting")
pprint.pprint(countingtable.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(countingtable.total_language_count)

print(countingtable.getCount("abc","en"))