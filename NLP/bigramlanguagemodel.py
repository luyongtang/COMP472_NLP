from NLP.languagecountingtable import LanguageCountingTable
from NLP.sentenceparser import SentenceParser
from NLP.evaluation import Evaluation
from decimal import Decimal
import math
class BigramLanguageLodel:
    def __init__(self, vocabulary_type,smooth_val):
        self.vocabulary_type = vocabulary_type
        # characters only
        self.ngram_size = 1
        # creating n-grams, (break tweet into chars)
        self.character_parser = SentenceParser(vocabulary_type, 1)
        self.bigram_parser = SentenceParser(vocabulary_type, 2)
        self.smooth_val = smooth_val
        self.is_vocab_0 = vocabulary_type is 0
        self.evaluator = Evaluation(vocabulary_type)
        self.counting_tables = {
            "eu":LanguageCountingTable(smooth_val),
            "ca":LanguageCountingTable(smooth_val),
            "gl":LanguageCountingTable(smooth_val),
            "es":LanguageCountingTable(smooth_val),
            "en":LanguageCountingTable(smooth_val),
            "pt":LanguageCountingTable(smooth_val)
        }
    def learnFromFile(self, textfile):
        with open(textfile, 'r', encoding="utf8") as tweets_file:
            for tweet_line in tweets_file:
                lang, tweet, tweet_id = self.extractLangAndTweet(tweet_line)
                # to lower case when vocab is 0
                tweet = tweet.lower() if self.is_vocab_0 else tweet
                for char in self.character_parser.parseSentence(tweet, False):
                    self.counting_tables[lang].addToCharSet(char)
                self.counting_tables[lang].addToCharSet("_")
                for bigram in self.bigram_parser.parseSentence(tweet, True):
                    self.counting_tables[lang].addToBigramList(bigram)

        for lang in self.counting_tables:
            self.counting_tables[lang].createBigramTable()
            self.counting_tables[lang].calculateProbabilityPerRow()
    
    def classify(self, sentence):
        bigram_list = self.bigram_parser.parseSentence(sentence, True)
        best_score = None
        best_score_lang = None
        for lang in self.counting_tables:
            score_ = self.score(bigram_list, lang)
            #print(lang, score_)
            if best_score is None or score_ > best_score:
                best_score = score_
                best_score_lang = lang
        return best_score_lang, '%.2E' % Decimal(best_score)

    def score(self, bigram_list, lang):
        total_score = 0
        for bigram in bigram_list:
            # if bigram not part of bigram table, the score is zero
            if self.counting_tables[lang].bigramExists(bigram):
                bigram_prob = self.counting_tables[lang].getProbability(bigram)
                if bigram_prob != 0:
                    total_score += math.log( bigram_prob )
            else:
                #print("no exists in ", lang, bigram)
                total_score -=10

        return total_score

    def extractLangAndTweet(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        if 0 <= len(tweet_) < 4:
            return "", "", ""
        return tweet_[2], tweet_[3], tweet_[0]
    
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
        file_name = "./output/trace_" + str(self.vocabulary_type) + "_" + str(self.ngram_size) + "_" + str(
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
        file_name = "./output/eval_" + str(self.vocabulary_type) + "_" + str(self.ngram_size) + "_" + str(
            self.smooth_val) + ".txt"
        out_file = open(file_name, "w")
        out_file.writelines(eval_output)
        out_file.close()