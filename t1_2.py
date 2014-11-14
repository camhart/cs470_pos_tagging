import random, signal, json, time

def buildData():
	t0 = time.time()
	print("Start: %f" % (t0, ))

	totalSize = -1
	curPos = -1
	mode = 0

	def printStatus():
		print("mode=%d curPos=%d size=%d" % (mode, curPos, totalSize))

	def handler(signum, frame):
		printStatus()

	print('type ctrl+break or ctrl+pause to print current state')
	# register ctrl+break to print values
	signal.signal(signal.SIGBREAK, handler)  #windows only

	infilename = "allTraining.txt"
	trainingdata = open(infilename).read()

	contextconst = ["", ""]

	context = contextconst
	model = {}
	wordList = trainingdata.split()

	curPos = 0
	totalSize = len(wordList)
	for curPos in range(totalSize):
	# while curPos < len(wordList):
		word = wordList[curPos].split('_')[1]
		#print (word)
		akey = ' '.join(context)
		model[akey] = model.setdefault(akey,[]) + [word]
		context = (context+[word])[1:]
		curPos+=1

	# print(model)

	t1 = time.time()
	print("mode0 finished: %f" % (t1-t0, ))
	mode = 1
	print("creating new model...")

	newModel = {}
	totalSize = len(model.keys())
	curPos = 0
	for key in model.keys():
		valueList = model.get(key)
		newList = []



		while(len(valueList) > 0):
			val = valueList[0]
			count = 0
			i = 0
			while i < len(valueList):
				value = valueList[i]
				if(value == val):
					count+=1
					valueList.pop(i)
				else:
					i+=1

			#newList.append(' '.join([str(count), val]))
			newList.append((count, val))

		newModel[key] = newList
		curPos+=1

	mode=2

	t2 = time.time()
	print("mode1: %f (total: %f)" % (t2-t1, t2-t0))
	# for key, value in newModel.items():
	# 	print(' '.join([key, str(value)]))
	# 	break
	# print(newModel)

	with open('json_data_2.txt', 'w') as f:
		f.write(json.dumps(newModel))

def main():
	buildData()


if __name__ == '__main__':
	main()