from NLP import processor

processor = processor.NBCModel(0, 2, 1)

print(processor.is_in_vocabulary('a'))
print(processor.is_in_vocabulary('A'))
print(processor.is_in_vocabulary('é'))
print(processor.is_in_vocabulary('ÿ'))
