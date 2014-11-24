import signal
from confusion import ConfusionMatrix
from helpers import buildDataModels, getWordProbability, buildKeyProbs, getTagProbability

class PrintVals(object):
	mode = 0
	curPos = 0
	totalSize = -1

class Viterbi(object):

	def __init__(self, tag2tag, tagToWordDict):
		self.tag2tag = tag2tag	#transition
		self.tag2word = tagToWordDict	#emission
		self.keyProbs = buildKeyProbs(tag2tag)

	def getStateProb(self, state):
		return self.keyProbs[1][state] / self.keyProbs[0]

	def run(self, testData):

		path = {}

		tdSplit = testData.split()

		stateProbabilities = []
		for _ in range(len(tdSplit)):
			stateProbabilities.append({})

		# build start state probabilities
		for state in self.tag2tag.keys():

			if(state.strip() ==''):
				continue

			ss = state.split()
			state2 = state
			if(len(ss) > 1):
				state2 = ss[1]

			prob = self.getStateProb(state) * getWordProbability(self.tag2word, state2, tdSplit[0])

			stateProbabilities[0][state] = prob

			path[state] = [state]	#initial path

		c = 1
		PrintVals.mode+=1
		PrintVals.totalSize = len(tdSplit)
		while(c < len(tdSplit)):
			PrintVals.curPos+=1
			newPath = {}

			for endState in self.tag2tag.keys():
				if(endState.strip() == ''):
					continue

				maxPathProb = 0.0
				bestState = ""

				ess = endState.split()
				if(len(ess) > 1):
					ess = ess[1].strip()
				else:
					ess = ess[0]

				# oldcurPos = PrintVals.curPos
				# oldTotal = PrintVals.totalSize
				# PrintVals.curPos = 0
				# PrintVals.totalSize = len(self.tag2tag.keys())
				# PrintVals.mode+=1
				for startState in self.tag2tag.keys():
					# PrintVals.curPos+=1
					if(startState.strip() == ''):
						continue



					p = stateProbabilities[c-1][startState]
					p *= getTagProbability(self.tag2tag, startState, ess)
					p *= getWordProbability(self.tag2word, ess, tdSplit[c])

					if(maxPathProb < p):
						maxPathProb = p
						bestState = startState

				# PrintVals.mode-=1
				# PrintVals.curPos = oldcurPos
				# PrintVals.totalSize = oldTotal

				if(bestState.strip() == ''):
					stateProbabilities[c][endState] = 0.0
					continue

				stateProbabilities[c][endState] = maxPathProb
				newPath[endState] = path[bestState] + [endState]

			path = newPath
			c+=1

		maxProb = 0.0

		lastPath = len(tdSplit) - 1
		bestState = None

		for state in self.tag2tag.keys():
			if(state.strip() == ''):
				continue
			p = stateProbabilities[lastPath][state]
			if(maxProb < p):
				maxProb = p
				bestState = state

		if(bestState == None):
			return "No path found"

		if(' ' in path[bestState][0]):
			ret = [x.split()[1] for x in path[bestState]]
			return ret
		else:
			return path[bestState]


def runTwoWord():
	(tag2tag, tag2word) = buildDataModels('data/at_bigram.json', 'data/at_tag_to_word.json', ["", ""])

	devtestdata = ""
	with open('devtest.txt') as f:
		devtestdata = f.read()

	dataarray = []
	tagarray = []
	c = 0
	for word in devtestdata.split():
		ws = word.split('_')
		w = ws[0]
		t = ws[1]
		dataarray.append(w)
		tagarray.append(t)
		c+=1
		if(c > 5):
			break
	devtestdata = ' '.join(dataarray)

	v = Viterbi(tag2tag, tag2word)
	singlePath = v.run(devtestdata)

	# print(singlePath)

	confusionMatrix = ConfusionMatrix(tag2tag)
	confusionMatrix.build(tagarray, singlePath)
	results = confusionMatrix.getResults()

	def addFormatedMatrix(res):
		l = []
		# t2tkeys = [x.split()[1] if len(x.split()[1]) >  for x in tag2tag.keys()]
		t2tkeys = []
		for x in tag2tag.keys():
			xs = x.split()
			if(len(xs) > 1):
				t2tkeys.append(xs[1])
			elif(xs):
				t2tkeys.append(xs[0])
			else:
				t2tkeys.append(" ")
		l.append("".ljust(6))
		for key in t2tkeys:
			l.append(("%s" % (key, )).ljust(6))
		l.append('\n')
		c = 0
		for row in res['confusion_matrix']:
			l.append((t2tkeys[c]).ljust(6))
			for col in row:
				if(col > 0):
					l.append(("%d" % (col, )).ljust(6))
				else:
					l.append("".ljust(6))
			l.append("\n")
			c+=1
		res['formated_matrix'] = ''.join(l)
		return res

	results = addFormatedMatrix(results)

	with open('results_two.txt', 'w') as f:
		f.write("Path: %s" % (str([x.ljust(5) for x in singlePath]), ))
		f.write('\r\n')
		f.write("      %s" % (str([x.ljust(5) for x in results['results_matrix']]), ))
		f.write('\r\n')
		f.write("      %s" % (str([x.ljust(5) for x in tagarray]), ))
		f.write('\r\n')
		f.write("Tagging Accuracy: %f" % (results['accuracy'], ))
		f.write('\r\n')
		f.write(results['formated_matrix'])

def runOneWord():
	(tag2tag, tag2word) = buildDataModels('data/at_unigram.json', 'data/at_tag_to_word.json', ["", ""])

	devtestdata = ""
	with open('devtest.txt') as f:
		devtestdata = f.read()

	dataarray = []
	tagarray = []
	c = 0
	for word in devtestdata.split():
		ws = word.split('_')
		w = ws[0]
		t = ws[1]
		dataarray.append(w)
		tagarray.append(t)
		c+=1
		if(c > 5):
			break
	devtestdata = ' '.join(dataarray)

	v = Viterbi(tag2tag, tag2word)
	singlePath = v.run(devtestdata)

	confusionMatrix = ConfusionMatrix(tag2tag)
	confusionMatrix.build(tagarray, singlePath)
	results = confusionMatrix.getResults()

	def addFormatedMatrix(res):
		l = []
		t2tkeys = [x for x in tag2tag.keys()]
		l.append("".ljust(6))
		for key in t2tkeys:
			l.append(("%s" % (key, )).ljust(6))
		l.append('\n')
		c = 0
		for row in res['confusion_matrix']:
			l.append((t2tkeys[c]).ljust(6))
			for col in row:
				if(col > 0):
					l.append(("%d" % (col, )).ljust(6))
				else:
					l.append("".ljust(6))
			l.append("\n")
			c+=1
		res['formated_matrix'] = ''.join(l)
		return res

	results = addFormatedMatrix(results)

	with open('results_one.txt', 'w') as f:
		f.write("Path: %s" % (str([x.ljust(5) for x in singlePath]), ))
		f.write('\r\n')
		f.write("      %s" % (str([x.ljust(5) for x in results['results_matrix']]), ))
		f.write('\r\n')
		f.write("      %s" % (str([x.ljust(5) for x in tagarray]), ))
		f.write('\r\n')
		f.write("Tagging Accuracy: %f" % (results['accuracy'], ))
		f.write('\r\n')
		f.write(results['formated_matrix'])

if __name__ == '__main__':

	def printStatus():
		print("mode=%d curPos=%d size=%d" % (PrintVals.mode, PrintVals.curPos, PrintVals.totalSize))

	def handler(signum, frame):
		printStatus()

	print('type ctrl+break or ctrl+pause to print current state')
	# register ctrl+break to print values
	signal.signal(signal.SIGBREAK, handler)  #windows only
	runOneWord()
	runTwoWord()