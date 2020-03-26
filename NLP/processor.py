from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser
import math

class NBCModel:
    def __init__(self, vocabulary_type, ngram_size, smooth_val):
        self.vocabulary = vocabulary_type
        self.ngram_size = ngram_size
        self.smooth_val = smooth_val
        self.sentence_parser = SentenceParser(vocabulary_type,ngram_size)
        self.counting_table = CountingTable(smooth_val)

    def learnfromfile(self,textfile):
        with open(textfile,'r', encoding="utf8") as tweets_file:
            for tweet_line in tweets_file:
                lang, tweet = self.extractLangAndTweet(tweet_line)
                for charsSequence in self.sentence_parser.parseSentence(tweet):
                    self.counting_table.addCount(charsSequence,lang)
        self.counting_table.addUnknownCount()
        self.counting_table.updateLanguageSumCount()
        pass

    def extractLangAndTweet(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        return tweet_[2],tweet_[3]

    def classify(self, sentence):
        print()
        print("classify sentence:")
        print(sentence)
        charsSequenceSet = self.sentence_parser.parseSentence(sentence)
        best_score = None
        best_score_lang = None
        print("scores:")
        for key_lang in self.counting_table.init_languages:
            score_ = self.score(charsSequenceSet,key_lang)
            print(key_lang, score_)
            if best_score is None or score_ > best_score:
                best_score = score_
                best_score_lang = key_lang
        return best_score_lang

    # score(language)
    def score(self,charsSequenceSet,language):
        score_sum = math.log( self.languageProbability(language) )
        for charsSequence in charsSequenceSet:
            conditional_probability_score = self.charSequenceLanguageCP(charsSequence,language)
            if conditional_probability_score == 0: continue
            score_sum += math.log(conditional_probability_score)
        return score_sum

    # P(language)
    def languageProbability(self, language):
        total_languange_count = self.counting_table.total_language_count[language]
        languages_sum_count = self.counting_table.languages_sum_count
        return total_languange_count/languages_sum_count

    # P(charsSquence|language) CL
    def charSequenceLanguageCP(self, charsSequence, language):
        total_chars_sequence_count = self.counting_table.vocabulary_count[charsSequence][language]
        total_languange_count = self.counting_table.total_language_count[language]
        return total_chars_sequence_count/total_languange_count
        pass

    def learn(self, tweets):

        pass
