import copy
class LanguageCountingTable:
    def __init__(self, smoothing):
        self.smoothing=smoothing
        # all characters
        self.init_characters_set_count = {}
        self.bigrams_list = []
        self.language_table = {}
    
    def addToCharSet(self, char):
        self.init_characters_set_count[char]=0

    def addToBigramList(self, bigram):
        self.bigrams_list.append(bigram)
    
    def createBigramTable(self):
        for bigram in self.bigrams_list:
            self.addToTable(bigram)

    def calculateProbabilityPerRow(self):
        # succ_chars is succeding set chars of char
        for char, succ_chars in self.language_table.items():
            total_count = 0
            #get the total of row
            for succ_char, succ_char_count in succ_chars.items():
                total_count += self.smoothing + succ_char_count
            #apply probability bigram_count/total_bigrams_count
            for succ_char, succ_char_count in succ_chars.items():
                self.language_table[char][succ_char] = (self.smoothing + succ_char_count)/total_count
    
    def addToTable(self, bigram):
        if (not self.charExists(bigram)):
            self.addNewBigram(bigram)
        current_char = bigram[0]
        succeeding_char = bigram[1]
        self.language_table[current_char][succeeding_char]+=1
    
    def charExists(self,bigram):
        return bigram[0] in self.language_table.keys()
    
    def bigramExists(self, bigram):
        try:
            self.language_table[bigram[0]][bigram[1]]
            return True
        except KeyError:
            return False
    
    def getProbability(self, bigram):
        return self.language_table[bigram[0]][bigram[1]]
    
    def addNewBigram(self, bigram):
        row = copy.deepcopy(self.init_characters_set_count)
        self.language_table[bigram[0]]=row
        

    