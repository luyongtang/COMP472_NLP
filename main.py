import sys
from NLP.nbcmodel import NBCModel
from NLP.bigramlanguagemodel import BigramLanguageModel

# python main.py bl data/training-tweets.txt data/test-tweets-given.txt

# nb, naive bayes: V, n-gram size, smoothing
# bl, bigram language: V, penality weight, smoothing
models = {
    'nb': NBCModel(0,3,0.099),
    'bl': BigramLanguageModel(2,10,0.5)
}

if len(sys.argv) <= 3:
    print("missing arguemnts: main.py nb|bg training_filepath testing_filepath")
    exit()

if not sys.argv[1] in models:
    print("invalid model type")
    exit()
model_name = sys.argv[1]
training_filepath = sys.argv[2]
testing_filepath = sys.argv[3]

model = models[model_name]
print("\n--------Training", model_name,"Model--------")
model.learnFromFile(training_filepath)
print("\n--------Predicting From Test File--------")
model.predictFromFile(testing_filepath)

 
