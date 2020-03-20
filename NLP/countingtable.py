import copy
class CountingTable:
    def __init__(self,smoothing):
        self.init_languages = {"eu":0,"ca":0,"gl":0,"es":0,"en":0,"pt":0}
        self.smoothing=smoothing
        self.vocabulary_count = {}
        self.total_language_count = copy.deepcopy(self.init_languages)
    
    def addCount(self,chars,language):
        if (not self.charsCountExists(chars)):
            self.createNewEntryCount(chars,language)
        self.vocabulary_count[chars][language]+=1
        self.total_language_count[language]+=1
    
    def charsCountExists(self,chars):
        return chars in self.vocabulary_count.keys()
    
    def createNewEntryCount(self,chars,language):
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
            return self.smoothing
        return self.vocabulary_count[chars][language]