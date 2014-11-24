import json, random

from helpers import addProbability, testProbabilities, getProbableTag, buildDataModels


def buildTagParagraph(dataDict, wordCount, seedWord):
	curKey = seedWord

	def toKey(keyTuple):
		return ' '.join(keyTuple)

	# print("seed='%s'" % (toKey(curKey), ))
	
	tagParagraph = []
	while(len(tagParagraph) < wordCount):
		# print("curKey='%s'" % (toKey(curKey), ))
		wordList = dataDict[toKey(curKey)]
		# print(wordList)
		# print(':' + str(wordList))
		# curKey = random.choice(wordList)[1]
		val = random.random()
		curKey.append(getProbableTag(val, wordList)[1])
		curKey = curKey[1:]
		tagParagraph.append(toKey(curKey))

	return tagParagraph

def buildParagraph(tagParagraph, tagToWordDict):
	paragraph = []
	for tags in tagParagraph:
		# for tag in tags.split():
		tagssplit = tags.split()
		tag = ""
		if(len(tagssplit) > 1):
			tag = tagssplit[1]
		else:
			tag = tagssplit[0]
		val = random.random()
		word = getProbableTag(val, tagToWordDict[tag])
		paragraph.append(word[1])
	return paragraph

def run(ngram, tag2word, seed):
	(dataDict, tagToWordDict) = buildDataModels(ngram, tag2word, seed)

	tagParagraph = buildTagParagraph(dataDict, 100, seedWord=seed)



	paragraph = buildParagraph(tagParagraph, tagToWordDict)
	print(' '.join(paragraph))

def main():
	# run('data/poem_unigram.json', 'data/poem_tag_to_word.json', [""])
	run('data/at_bigram.json', 'data/at_tag_to_word.json', ["", ""])

if __name__ == '__main__':
	main()