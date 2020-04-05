import sys
from decimal import Decimal
from NLP.bigramlanguagemodel import BigramLanguageModel


if len(sys.argv) <= 3:
    print("missing arguments!")
    exit()

vocabulary = sys.argv[1]
penalty_weight = sys.argv[2]
smoothing_value = sys.argv[3]

training_filepath = "data/training-tweets.txt"
testing_filepath = "data/test-tweets-given.txt"
model = BigramLanguageModel(int(vocabulary), float(penalty_weight), Decimal(smoothing_value))
print("\n--------Training Bi-gram Language Model--------")
model.learnFromFile(training_filepath)
print("\n--------Predicting From Test File--------")
model.predictFromFile(testing_filepath)
