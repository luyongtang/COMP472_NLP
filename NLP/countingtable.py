import copy
from collections import Counter
class CountingTable:

    def __init__(self,smoothing):
        self.init_languages = {"eu":0,"ca":0,"gl":0,"es":0,"en":0,"pt":0}
        self.smoothing=smoothing
        self.vocabulary_count = {}
        self.total_language_count = copy.deepcopy(self.init_languages)
        self.languages_sum_count = 0

        # for evaluation
        self.fp_count = copy.deepcopy(self.init_languages)
        self.fn_count = copy.deepcopy(self.init_languages)
        self.tp_count = copy.deepcopy(self.init_languages)
        self.total_per_class = {"eu": 0, "ca": 0, "gl": 0, "es": 0, "en": 0, "pt": 0}
        self.precision_per_class = {"eu": 0.0, "ca": 0.0, "gl": 0.0, "es": 0.0, "en": 0.0, "pt": 0.0}
        self.recall_per_class = {"eu": 0.0, "ca": 0.0, "gl": 0.0, "es": 0.0, "en": 0.0, "pt": 0.0}
        self.f1_measure = {"eu": 0.0, "ca": 0.0, "gl": 0.0, "es": 0.0, "en": 0.0, "pt": 0.0}
        self.marco_f1 = 0
        self.weighted_average_f1 = 0

    def addCount(self,chars,language):
        if (not self.charsCountExists(chars)):
            self.createNewEntryCount(chars)
        self.vocabulary_count[chars][language]+=1
        self.total_language_count[language]+=1

    #unknown count addition
    def addUnknownCount(self):
        self.createNewEntryCount("UNKNOWN")

    def charsCountExists(self,chars):
        return chars in self.vocabulary_count.keys()

    def updateLanguageSumCount(self):
        self.languages_sum_count = 0
        for key in self.total_language_count:
            self.languages_sum_count += self.total_language_count[key]

    def createNewEntryCount(self,chars):
        #apply smoothing
        init_count = copy.deepcopy(self.init_languages)
        self.addSmoothing(init_count)
        self.addSmoothing(self.total_language_count)
        self.vocabulary_count[chars] = init_count
        pass

    def addSmoothing(self,language_dict):
        for key in language_dict:
            language_dict[key]+=self.smoothing

    def getCount(self, chars, language):
        if (not self.charsCountExists(chars)):
            #return smoothing or we can also return "UNKNOWN" from dict count, it is the same value
            return self.smoothing
        return self.vocabulary_count[chars][language]

    def process_eval_data(self, actual_lan, predict_lan):
        pass
        result = "wrong"
        if actual_lan == predict_lan:
            result = "correct"
            self.tp_count[actual_lan] += 1
        else:
            self.fp_count[predict_lan] += 1
            self.fn_count[actual_lan] += 1
        return result

    def calculate_precision(self):
        labelled = copy.deepcopy(self.init_languages)
        for key in labelled.keys():
            labelled[key] = self.fp_count[key] + self.tp_count[key]
        for key in self.precision_per_class.keys():
            self.precision_per_class[key] = self.tp_count[key] / labelled[key]
        print("Labelled: ", labelled)
        print("Precision: ", self.precision_per_class)

    def calculate_recall(self):
        for key in self.total_per_class.keys():
            self.total_per_class[key] = self.tp_count[key] + self.fn_count[key]
        for key in self.recall_per_class.keys():
            self.recall_per_class[key] = self.tp_count[key] / self.total_per_class[key]
        print("Total_per_class: ", self.total_per_class)
        print("Recall: ", self.recall_per_class)

    def calculate_f1_measure(self, tweet_total):
        sum_f1 = 0
        sum_weighted_f1 = 0
        for key in self.f1_measure.keys():
            denominator = (self.precision_per_class[key] + self.recall_per_class[key])
            self.f1_measure[key] = 0.0 if denominator == 0 else ((2 * self.precision_per_class[key] * self.recall_per_class[key]) / denominator)
            # calculate marco F1
            sum_f1 += self.f1_measure[key]
            # calculate weighted average F1
            sum_weighted_f1 += self.f1_measure[key] * self.total_per_class[key]
        self.marco_f1 = sum_f1 / len(self.f1_measure)
        self.weighted_average_f1 = sum_weighted_f1 / tweet_total
        print("F1-Measure: ", self.f1_measure)
        print("Marco-F1: ", self.marco_f1)
        print("Weighted-average-F1: ", self.weighted_average_f1)

    def calculate_eval(self, tweet_total):
        self.print_evaluation()
        self.calculate_precision()
        self.calculate_recall()
        self.calculate_f1_measure(tweet_total)


    def print_evaluation(self):
        print("True Positive: ", self.tp_count)
        print("False Positive: ", self.fp_count)
        print("False Negative: ", self.fn_count)

