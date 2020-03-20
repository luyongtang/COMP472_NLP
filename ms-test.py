import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
sentence = "abédd"

print(SentenceParser.is_valid_char_functions[0]("a"))

sentenceParser = SentenceParser(1,2)

chars = sentenceParser.parseSentence(sentence)
print(chars)

exit(0)

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