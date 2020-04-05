from NLP.countingtable import CountingTable
from NLP.evaluation import Evaluation
from NLP.sentenceparser import SentenceParser
from decimal import Decimal
from math import pow
import math


class NBCModel:
    def __init__(self, vocabulary_type, ngram_size, smooth_val):
        self.vocabulary = vocabulary_type
        self.is_vocab_0 = vocabulary_type is 0
        self.ngram_size = ngram_size
        self.smooth_val = smooth_val
        self.evaluator = Evaluation(vocabulary_type)
        # creating n-grams, (break tweet into chars)
        self.sentence_parser = SentenceParser(vocabulary_type, ngram_size, False)
        # couting n-grams per class with related functions
        self.counting_table = CountingTable(smooth_val)
        # for V=0,V=1,V=2
        self.vocabulary_size_factors = [26, 52, 116766]

    def learnFromFile(self, textfile):
        with open(textfile, 'r', encoding="utf8") as tweets_file:
            for tweet_line in tweets_file:
                lang, tweet, tweet_id = self.extractLangAndTweet(tweet_line)
                self.counting_table.addClassCount(lang)
                # to lower case when vocab is 0
                tweet = tweet.lower() if self.is_vocab_0 else tweet
                for charsSequence in self.sentence_parser.parseSentence(tweet):
                    self.counting_table.addNGramCount(charsSequence, lang)
        self.counting_table.calculatePrior()
        vocab_size = self.vocabulary_size_factors[self.vocabulary]
        self.counting_table.applySmoothingToClasses(vocab_size, self.ngram_size)
        pass

    def extractLangAndTweet(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        if 0 <= len(tweet_) < 4:
            return "", "", ""
        return tweet_[2], tweet_[3], tweet_[0]

    def classify(self, sentence):
        charsSequenceSet = self.sentence_parser.parseSentence(sentence)
        best_score = None
        best_score_lang = None
        for key_lang in self.counting_table.init_languages:
            score_ = self.score(charsSequenceSet, key_lang)
            if best_score is None or score_ > best_score:
                best_score = score_
                best_score_lang = key_lang
        return best_score_lang, '%.2E' % Decimal(best_score)

    # score of tweet in a given language
    def score(self, charsSequenceSet, language):
        score_sum = math.log(self.languageProbability(language))
        for charsSequence in charsSequenceSet:
            conditional_probability_score = self.charSequenceLanguageCP(charsSequence, language)
            if conditional_probability_score == 0:
                print(charsSequence, "  's conditional is 0!")
                continue
            score_sum += math.log(conditional_probability_score)
        return score_sum

    # P(language), P(class)
    def languageProbability(self, language):
        return self.counting_table.prior_probabilities[language]

    # P(charsSequence|language) CL, P(x|class)
    def charSequenceLanguageCP(self, charsSequence, language):
        ngram_count = self.counting_table.getNGramCount(charsSequence, language)
        class_count = self.counting_table.getClassCount(language)
        return ngram_count / class_count
        pass

    def predictFromFile(self, file):
        trace_output = ""
        double_space = "  "
        tweet_count = 0
        correct_count = 0
        with open(file, 'r', encoding="utf8") as tweets_file:
            for tweet_line in tweets_file:
                tweet_count += 1
                lang, tweet, tweet_id = self.extractLangAndTweet(tweet_line)
                res, score = self.classify(tweet)
                compare = "wrong"
                self.evaluator.process_eval_data(lang, res)
                if res == lang:
                    compare = "correct"
                    correct_count += 1
                trace_output = trace_output + tweet_id + double_space + res + double_space + score + double_space + lang + \
                               double_space + compare + "\n"
        accuracy = correct_count / tweet_count
        print("accuracy: ", accuracy)
        self.generate_trace(trace_output)
        self.evaluator.calculate_eval(tweet_count)
        self.generate_eval(accuracy)

    def generate_trace(self, contents):
        file_name = "./output/trace_" + str(self.vocabulary) + "_" + str(self.ngram_size) + "_" + str(
            self.smooth_val) + ".txt"
        out_file = open(file_name, "w")
        out_file.writelines(contents)
        out_file.close()

    def generate_eval(self, accuracy):
        eval_output = str(accuracy) + "\n"
        precisions = ""
        recalls = ""
        f1_measures = ""
        for key in self.evaluator.precision_per_class.keys():
            precisions += str(self.evaluator.precision_per_class[key]) + "  "
            recalls += str(self.evaluator.recall_per_class[key]) + "  "
            f1_measures += str(self.evaluator.f1_measure[key]) + "  "
        pass
        eval_output += precisions.rstrip() + "\n" + recalls.rstrip() + "\n" + f1_measures.rstrip() + "\n" + str(
            self.evaluator.marco_f1) + "  " + str(self.evaluator.weighted_average_f1)
        # print(eval_output)
        file_name = "./output/eval_" + str(self.vocabulary) + "_" + str(self.ngram_size) + "_" + str(
            self.smooth_val) + ".txt"
        out_file = open(file_name, "w")
        out_file.writelines(eval_output)
        out_file.close()
