class SentenceParser:
    def is_26_case_insensitive(character):
        return 97 <= ord(character) <= 122

    def is_52_case_sensitive(character):
        return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122

    def is_expanded_characters(character):
        return 65 <= ord(character) <= 90 or 97 <= ord(character) <= 122 or character.isalpha()
        
    is_valid_char_functions = [is_26_case_insensitive, is_52_case_sensitive, is_expanded_characters]

    def __init__(self, vocabulary_index, charCount):
        self.isValidChar = SentenceParser.is_valid_char_functions[vocabulary_index]
        self.charCount = charCount

    def parseSentence(self,sentence):
        return self.breakSentence([],sentence)

    def breakSentence(self,charsCollector,sentence):
        if (len(sentence)<self.charCount):
            return charsCollector
        index = 0
        validCharsSequence = True
        while(validCharsSequence and index<self.charCount):
            validCharsSequence = validCharsSequence and self.isValidChar( sentence[index])
            index+=1
        if validCharsSequence:
            charsCollector.append(sentence[:self.charCount])
        return self.breakSentence(charsCollector,sentence[1:])