import copy
from collections import Counter
class CountingTable:

    def __init__(self,smoothing):
        self.init_languages = {"eu":0,"ca":0,"gl":0,"es":0,"en":0,"pt":0}
        self.smoothing=smoothing
        self.ngram_dictionary = {}
        # counting of ngrams per class
        self.ngram_count_per_class = copy.deepcopy(self.init_languages)
        self.tweets_per_class = copy.deepcopy(self.init_languages)
        self.prior_probabilities = copy.deepcopy(self.init_languages)
        self.smoothed_ngram_per_class = copy.deepcopy(self.init_languages)

    def addNGramCount(self,chars,language):
        if (not self.charsCountExists(chars)):
            self.createNewEntryCount(chars)
        self.ngram_dictionary[chars][language]+=1
        self.ngram_count_per_class[language]+=1

    def addClassCount(self, lang):
        self.tweets_per_class[lang] += 1
    
    def calculatePrior(self):
        tweets_total = 0
        for lan in self.tweets_per_class.keys():
            tweets_total += self.tweets_per_class[lan]
        for lan in self.tweets_per_class.keys():
            self.prior_probabilities[lan] = self.tweets_per_class[lan] / tweets_total
        print("prior: ", self.prior_probabilities)
        pass

    def charsCountExists(self,chars):
        return chars in self.ngram_dictionary.keys()

    def createNewEntryCount(self,chars):
        #apply smoothing
        init_count = copy.deepcopy(self.init_languages)
        self.addSmoothingToNGram(init_count)
        # self.addSmoothing(self.ngram_count_per_class)
        self.ngram_dictionary[chars] = init_count
        pass
    # smoothing for individual ngram
    def addSmoothingToNGram(self,language_dict):
        for key in language_dict:
            language_dict[key]+=self.smoothing

    # smoothing for overrall classes, total count of n-grams
    def applySmoothingToClasses(self, vocab_size, ngram_size):
        combinations_count = pow(vocab_size, ngram_size)
        for lan in self.smoothed_ngram_per_class.keys():
            self.smoothed_ngram_per_class[lan] = self.ngram_count_per_class[lan] + combinations_count * self.smoothing
        print("smoothed_ngram_per_class(after smoothing): ", self.smoothed_ngram_per_class)
        pass

    def getNGramCount(self, chars, language):
        if (not self.charsCountExists(chars)):
            return self.smoothing
        return self.ngram_dictionary[chars][language]

    def getClassCount(self, language):
        return self.smoothed_ngram_per_class[language]