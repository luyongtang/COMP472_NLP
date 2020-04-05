import re
class SentenceParser:
    # isSpecialCharacter used for bigram language model, for NB model it will alway return false
    def is_26_case_insensitive(self, character):
        return 97 <= ord(character) <= 122 or self.isSpecialCharacter(character)

    def is_52_case_sensitive(self, character):
        return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or self.isSpecialCharacter(character)

    def is_expanded_characters(self, character):
        return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or character.isalpha() or self.isSpecialCharacter(character)

    def __init__(self, vocabulary_index, charCount, captureBegEnd):
        self.is_valid_char_functions = [self.is_26_case_insensitive, self.is_52_case_sensitive, self.is_expanded_characters]
        self.isValidChar = self.is_valid_char_functions[vocabulary_index]
        self.charCount = charCount
        self.captureBegEnd = captureBegEnd
        # include special characters, used for bigram language model
        self.specialCharacters = []

    def includeSpecialCharacter(self, char):
        self.specialCharacters.append(char)
    
    def isSpecialCharacter(self, char):
        return char in self.specialCharacters

    def parseSentence(self,sentence):
        sentence = self.preProcess(sentence)
        return self.breakSentence([],sentence)
    
    def preProcess(self, sentence):
        # remove tweet mentions
        sentence = re.sub(r'@(\w*|_)',"",sentence)
        # remove hashtag mentions
        sentence = re.sub(r'#(\w*|_)',"",sentence)
        # remove links
        sentence = re.sub(r'http(s)?://(\w|\.|/)*',"",sentence)
        # replace consecutive spaces by one space
        sentence = re.sub(r'\s{2,}'," ",sentence)
        # identify beginning and ending of sentence, used for bigram language model
        return "_"+sentence+"_" if self.captureBegEnd else sentence 

    #create the n-grams
    def breakSentence(self,charsCollector,sentence):
        if (len(sentence)<self.charCount):
            return charsCollector
        index = 0
        validCharsSequence = True
        while(validCharsSequence and index<self.charCount):
            validCharsSequence = validCharsSequence and self.isValidChar(sentence[index])
            index+=1
        if validCharsSequence:
            charsCollector.append(sentence[:self.charCount])
        return self.breakSentence(charsCollector,sentence[1:])