from NLP import sentenceparser

# processor = sentenceparser.SentenceParser()
#
# print(processor.is_in_vocabulary('a'))
# print(processor.is_in_vocabulary('A'))
# print(processor.is_in_vocabulary('é'))
# print(processor.is_in_vocabulary('ÿ'))

count = 0
count2 = 0
# unicode = 17 planes of 2**16 symbols
for codepoint in range(17 * 2**16):
    ch = chr(codepoint)
    if ch.isalpha():
        count = count + 1
    if sentenceparser.SentenceParser.is_52_case_sensitive(ch):
        count2 = count2 + 1
print(count, count2)
