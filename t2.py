import json, signal


def buildData():

	totalSize = -1
	curPos = -1

	def printStatus():
		print("%d / %d" % (curPos, totalSize))

	def handler(signum, frame):
		printStatus()

	print('type ctrl+break or ctrl+pause to print current state')
	# register ctrl+break to print values
	signal.signal(signal.SIGBREAK, handler)  #windows only

	text = ""
	with open('allTraining.txt') as f:
		text = f.read()

	totalSize = len(text.split())
	curPos = 0

	model = {}
	for word in text.split():
		wordChunks = word.split('_')
		tag = wordChunks[1]
		if(tag in model.keys()):
			# model[tag] = model.setdefault(tag,[]) + [(wordChunks[0])]
			tagList = model[tag]

			def getChunkFromList():		
				for c in range(len(tagList)):
					i = tagList[c]
					if(i[1] == wordChunks[0]):
						return (c, tagList[c][0])
				return (-1, -1)

			matchedOne = getChunkFromList()
			if(matchedOne[0] == -1):
				model[tag] = model[tag] + [(1, wordChunks[0])]
			else:
				model[tag] = model[tag] + [(tagList[matchedOne[0]][0] + 1, wordChunks[0])]
				del(model[tag][matchedOne[0]])
				# del(tagList[matchedOne])
				# tagList[matchedOne[0]][0]+=1
		else:
			model[tag] = [(1, wordChunks[0])]
		curPos+=1

	with open('t2_json_data.txt', 'w') as f:
		f.write(json.dumps(model))

if __name__ == '__main__':
	buildData()