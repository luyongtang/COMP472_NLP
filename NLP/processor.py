#import numpy as np
#from collections import Counter

class NBCModel:
    def __init__(self, vocabulary_type, size, smooth_val):
        self.vocabulary = vocabulary_type
        self.size = size
        self.smooth_val = smooth_val
        # self.is_in_vocabulary = sentenceparser.SentenceParser.is_valid_char[vocabulary_type]
        # create n-grams for all the six languages
        #self.basque = Counter()
        #self.catalan = Counter()
        #self.galician = Counter()
        #self.spanish = Counter()
        #self.english = Counter()
        #self.portuguess = Counter()

    def learn(self, tweets):

        pass
