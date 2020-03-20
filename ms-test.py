import pprint
from NLP.countingtable import CountingTale

countingtable = CountingTale(0.5)

countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abc","en")
countingtable.addCount("abd","gl")
countingtable.addCount("hfg","en")
print("sample couting")
pprint.pprint(countingtable.vocabulary_count)
print()
print("total count based on training set (added smoothing if applied)")
pprint.pprint(countingtable.total_language_count)

print(countingtable.getCount("abc","en"))