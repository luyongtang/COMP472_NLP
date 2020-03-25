from NLP.countingtable import CountingTable
from NLP.sentenceparser import SentenceParser

class NBCModel:
    def __init__(self, vocabulary_type, ngram_size, smooth_val):
        self.vocabulary = vocabulary_type
        self.ngram_size = ngram_size
        self.smooth_val = smooth_val
        self.sentence_parser = SentenceParser(vocabulary_type,ngram_size)
        self.counting_table = CountingTable(smooth_val)

    def learnfromfile(self,textfile):
        with open(textfile,'r') as tweets_file:
            for tweet_line in tweets_file:
                lang, tweet = self.extractLangAndTweet(tweet_line)
                for charsSequence in self.sentence_parser.parseSentence(tweet):
                    self.counting_table.addCount(charsSequence,lang)
        self.counting_table.addUnknownCount()
        pass

    def extractLangAndTweet(self, tweet_line):
        tweet_ = tweet_line.split("\t")
        return tweet_[2],tweet_[3]

    def learn(self, tweets):

        pass
