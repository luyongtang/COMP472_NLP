import numpy as np
from collections import Counter


def is_26_case_insensitive(character):
    return 97 <= ord(character) <= 122


def is_52_case_sensitive(character):
    return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122


def is_expanded_characters(character):
    return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or character.isalpha()


is_valid_char = [is_26_case_insensitive, is_52_case_sensitive, is_expanded_characters]


class NBCModel:
    def __init__(self, vocabulary_type, size, smooth_val):
        self.vocabulary = vocabulary_type
        self.size = size
        self.smooth_val = smooth_val
        self.is_in_vocabulary = is_valid_char[vocabulary_type]
        # create n-grams for all the six languages
        self.basque = Counter()
        self.catalan = Counter()
        self.galician = Counter()
        self.spanish = Counter()
        self.english = Counter()
        self.portuguess = Counter()

    def learn(self, tweets):

        pass
