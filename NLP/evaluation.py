import copy
class Evaluation:
    def __init__(self, vocabulary_type):
        self.init_languages = {"eu":0,"ca":0,"gl":0,"es":0,"en":0,"pt":0}
        self.vocabulary = vocabulary_type
        # for evaluation, fp false positive, fn false negative...
        self.fp_count = copy.deepcopy(self.init_languages)
        self.fn_count = copy.deepcopy(self.init_languages)
        self.tp_count = copy.deepcopy(self.init_languages)
        self.total_per_class = copy.deepcopy(self.init_languages)
        self.precision_per_class = copy.deepcopy(self.init_languages)
        self.recall_per_class = copy.deepcopy(self.init_languages)
        self.f1_measure = copy.deepcopy(self.init_languages)
        self.marco_f1 = 0
        self.weighted_average_f1 = 0

    def process_eval_data(self, actual_lan, predict_lan):
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
            if labelled[key] == 0:
                print("labelled is 0: ", key)
        for key in self.precision_per_class.keys():
            # self.precision_per_class[key] = self.tp_count[key] / labelled[key]
            self.precision_per_class[key] = 0 if labelled[key] == 0 else self.tp_count[key] / labelled[key]
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