import sys
from decimal import Decimal
from NLP.nbcmodel import NBCModel

if len(sys.argv) <= 3:
    print("missing arguments!")
    exit()

vocabulary = sys.argv[1]
n = sys.argv[2]
smoothing_value = sys.argv[3]

training_filepath = "data/training-tweets.txt"
testing_filepath = "data/test-tweets-given.txt"
model = NBCModel(int(vocabulary), int(n), Decimal(smoothing_value))
print("\n--------Training NBC Model--------")
model.learnFromFile(training_filepath)
print("\n--------Predicting From Test File--------")
model.predictFromFile(testing_filepath)
