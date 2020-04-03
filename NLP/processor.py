from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
from decimal import Decimal
from math import pow
import math


class NBCModel:
    def __init__(self, vocabulary_type, ngram_size, smooth_val):
        self.vocabulary = vocabulary_type
        self.ngram_size = ngram_size
        self.smooth_val = smooth_val
        self.sentence_parser = SentenceParser(vocabulary_type, ngram_size)
        self.counting_table = CountingTable(smooth_val)
        self.vocabulary_size_factors = [26, 52, 116766]

    def learnfromfile(self, textfile):
        with open(textfile, 'r', encoding="utf8") as tweets_file:
            for tweet_line in tweets_file:
                formatted_tweet_line = tweet_line.lower() if self.vocabulary == 0 else tweet_line
                lang, tweet, tweet_id = self.extractLangAndTweet(formatted_tweet_line)
                self.counting_table.tweets_per_class[lang] += 1
                for charsSequence in self.sentence_parser.parseSentence(tweet):
                    self.counting_table.addCount(charsSequence, lang)
        # self.counting_table.addUnknownCount()
        self.counting_table.updateLanguageSumCount()
        self.calculate_prior()
        self.add_smoothing()
        pass

    def extractLangAndTweet(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        if 0 <= len(tweet_) < 4:
            return "", "", ""
        return tweet_[2], tweet_[3], tweet_[0]

    def extractID(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        if 0 <= len(tweet_) < 4:
            return ""
        return tweet_[0], tweet_[3]

    def classify(self, sentence):
        # print()
        # print("classify sentence:")
        # print(sentence)
        charsSequenceSet = self.sentence_parser.parseSentence(sentence)
        best_score = None
        best_score_lang = None
        # print("scores:")
        for key_lang in self.counting_table.init_languages:
            score_ = self.score(charsSequenceSet, key_lang)
            # print(key_lang, score_)
            if best_score is None or score_ > best_score:
                best_score = score_
                best_score_lang = key_lang
        return best_score_lang, '%.2E' % Decimal(best_score)

    # score(language)
    def score(self, charsSequenceSet, language):
        score_sum = math.log(self.languageProbability(language))
        for charsSequence in charsSequenceSet:
            conditional_probability_score = self.charSequenceLanguageCP(charsSequence, language)
            if conditional_probability_score == 0:
                print(charsSequence, "  's conditional is 0!")
                continue
            score_sum += math.log(conditional_probability_score)
        return score_sum

    # P(language)
    def languageProbability(self, language):
        # total_language_count = self.counting_table.total_language_count[language]
        # languages_sum_count = self.counting_table.languages_sum_count
        return self.counting_table.prior_probabilities[language]

    def calculate_prior(self):
        tweets_total = 0
        for lan in self.counting_table.tweets_per_class.keys():
            tweets_total += self.counting_table.tweets_per_class[lan]
        for lan in self.counting_table.tweets_per_class.keys():
            self.counting_table.prior_probabilities[lan] = self.counting_table.tweets_per_class[lan] / tweets_total
        print("prior: ", self.counting_table.prior_probabilities)
        pass

    def add_smoothing(self):
        adjust_number = pow(self.vocabulary_size_factors[self.vocabulary], self.ngram_size)
        for lan in self.counting_table.words_per_class.keys():
            self.counting_table.words_per_class[lan] = self.counting_table.total_language_count[lan] + adjust_number * self.smooth_val
        print("words_per_class(after smoothing): ", self.counting_table.words_per_class)
        pass


    # P(charsSequence|language) CL
    def charSequenceLanguageCP(self, charsSequence, language):
        # total_chars_sequence_count = self.counting_table.vocabulary_count[charsSequence][language]
        total_chars_sequence_count = self.counting_table.getCount(charsSequence, language)
        total_language_count = self.counting_table.words_per_class[language]
        return total_chars_sequence_count / total_language_count
        pass

    def predict(self, file):
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
                self.counting_table.process_eval_data(lang, res)
                if res == lang:
                    compare = "correct"
                    correct_count += 1
                trace_output = trace_output + tweet_id + double_space + res + double_space + score + double_space + lang + \
                               double_space + compare + "\n"
        accuracy = correct_count / tweet_count
        print("accuracy: ", accuracy)
        self.generate_trace(trace_output)
        self.counting_table.calculate_eval(tweet_count)
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
        for key in self.counting_table.precision_per_class.keys():
            precisions += str(self.counting_table.precision_per_class[key]) + "  "
            recalls += str(self.counting_table.recall_per_class[key]) + "  "
            f1_measures += str(self.counting_table.f1_measure[key]) + "  "
        pass
        eval_output += precisions.rstrip() + "\n" + recalls.rstrip() + "\n" + f1_measures.rstrip() + "\n" + str(
            self.counting_table.marco_f1) + "  " + str(self.counting_table.weighted_average_f1)
        # print(eval_output)
        file_name = "./output/eval_" + str(self.vocabulary) + "_" + str(self.ngram_size) + "_" + str(
            self.smooth_val) + ".txt"
        out_file = open(file_name, "w")
        out_file.writelines(eval_output)
        out_file.close()
