import pprint
from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from NLP.processor import NBCModel

nbcModel = NBCModel(1,2,0.5)

nbcModel.learnfromfile("data/training-tweets.txt")

print("sample couting")
#pprint.pprint(nbcModel.counting_table.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(nbcModel.counting_table.total_language_count)
print(nbcModel.counting_table.languages_sum_count)
#print(nbcModel.counting_table.vocabulary_count["zue"])
#print("eu",nbcModel.charSequenceLanguageCP("zue","eu"))
#print("ca",nbcModel.charSequenceLanguageCP("zue","ca"))
#print("gl",nbcModel.charSequenceLanguageCP("zue","gl"))
#print("es",nbcModel.charSequenceLanguageCP("zue","es"))
#print("en",nbcModel.charSequenceLanguageCP("zue","en"))
#print("pt",nbcModel.charSequenceLanguageCP("zue","pt"))
print(nbcModel.languageProbability("eu"))
print(nbcModel.languageProbability("ca"))
print(nbcModel.languageProbability("gl"))
print(nbcModel.languageProbability("es"))
print(nbcModel.languageProbability("en"))
print(nbcModel.languageProbability("pt"))

total = 0

total+=nbcModel.languageProbability("eu")
total+=nbcModel.languageProbability("ca")
total+=nbcModel.languageProbability("gl")
total+=nbcModel.languageProbability("es")
total+=nbcModel.languageProbability("en")
total+=nbcModel.languageProbability("pt")

print(nbcModel.classify("Ba dena aprobatzeko etxen geitubehar... ta eualdi honek re ezto launtzen... @AmaiaAuza"))

#print(total)
#print("score for language")
#print("eu",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","eu"))
#print("ca",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","ca"))
#print("gl",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","gl"))
#print("es",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","es"))
#print("en",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","en"))
#print("pt",nbcModel.score("Porque estoy raro? Porque no te digo cosas bonitas?","pt"))

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