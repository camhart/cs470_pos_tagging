import string, json

punctuationSet = set(string.punctuation)

def cleanUpWord(word):
	''' Removes punctuation and makes it all lower case.
	'''
	return word #hmm
	if(isinstance(word, list)):
		l = []
		for w in word:
			l.append(''.join(c for c in w if c not in punctuationSet))
	else:
		word = word.lower()
		return ''.join(c for c in word if c not in punctuationSet)

def addProbability(dataDict):
	for tagList in dataDict.values():
		totalSum = 0
		for tag in tagList:
			totalSum+=tag[0]
		for tag in tagList:
			tag.append(float(tag[0] / totalSum))
	# print(dataDict)

def testProbabilities(dataDict):
	for tagList in dataDict.values():
		amt = 0
		for tag in tagList:
			amt+=tag[2]
		if abs(amt - 1) > 0.0000001:	#should be accurate enough
			print("%s = %f" % (tag[1], amt))

def getProbableTag(randomVal, tagList):
	val = 0.0
	for tag in tagList:
		val+=tag[2]
		if(randomVal <= val):
			return tag
	print("Never returned!?")

def buildDataModels(ngram, tag2word, seed):
	dataDict = {}
	with open(ngram, 'r') as f:
		dataDict = json.loads(f.read())
	addProbability(dataDict)
	testProbabilities(dataDict)

	tagToWordDict = {}
	with open(tag2word, 'r') as f:
		tagToWordDict = json.loads(f.read())
	addProbability(tagToWordDict)
	testProbabilities(tagToWordDict)

	return (dataDict, tagToWordDict)

def getWordProbability(tag2word, tag, word):
	if(len(tag.split()) > 1):
		# print(tag)
		tag = tag.split()[1]
		# print(tag)
	wlist = tag2word[tag.strip()]
	for count, curWord, prob in wlist:
		if(curWord == word):
			return prob
	return 0.0

def getTagProbability(tag2tag, tag_cur, tag_next):
	tlist = tag2tag[tag_cur]
	for count, curTag, prob in tlist:
		if(curTag == tag_next):
			return prob
	return 0.0

def buildKeyProbs(tag2tag):
	ret = {}
	runningTotal = 0
	for key in tag2tag.keys():
		total = 0
		for k,v in tag2tag.items():

			for count, tag, _ in v:
				total += count

		ret[key] = total
		runningTotal+=total
	return (runningTotal, ret)
