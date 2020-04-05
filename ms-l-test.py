import pprint
from NLP.bigramlanguagemodel import BigramLanguageLodel

bigram = BigramLanguageLodel(2,10,0.5)

bigram.learnFromFile("data/training-tweets.txt")
print(len(bigram.counting_tables["en"].init_characters_set_count))
print(len(bigram.counting_tables["gl"].init_characters_set_count))
print(bigram.counting_tables["es"].init_characters_set_count)
#pprint.pprint(bigram.counting_tables["en"].language_table['i']['n'])
#pprint.pprint(bigram.counting_tables["es"].language_table['i']['n'])
#print(bigram.score(["Va","ya","go","la","zo","de","Ga","it","an","de","be","nf","ic","Ma","dr","mí"],"en"))
#print(bigram.score(["Va","ya","go","la","zo","de","Ga","it","an","de","be","nf","ic","Ma","dr","mí"],"es"))
#lang, score = bigram.classify("Bona nit des de #Donosti! @ Playa de La Concha / Kontxa Hondartza")
bigram.predictFromFile("data/test-tweets-given.txt")
print("cool")