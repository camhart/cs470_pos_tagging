import json
from helpers import addProbability

with open('data/at_tag_to_word.json', 'r') as f:
	dataDict = json.loads(f.read())

addProbability(dataDict)
for key, lists in dataDict.items():
	if(len(lists) < 20):
		print(key)
		print(lists)
# print(dataDict['VBG'])
# print(dataDict)

# for key, value in dataDict.items():
# 	# print(' '.join([key, str(value)]))
# 	for ca in range(len(value)):
# 		a = value[ca]
# 		count = 0
# 		for cb in range(ca):
# 			b = value[cb]
# 			if(a[1] == b[1]):
# 				count+=1
# 		if(count > 1):
# 			print("invalid data: count > 1 on %s - %d in %s" % (a[1], count, key))