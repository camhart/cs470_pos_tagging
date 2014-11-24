

class ConfusionMatrix(object):

	def __init__(self, tag2tag):
		self.total = 0.0
		self.correctlyTagged = 0
		# if(isinstance(tag2tag, dict)):
		self.tag2tag = [] 
		for x in tag2tag.keys():
			xs = x.split()
			if(len(xs) > 1):
				self.tag2tag.append(xs[1])
			elif(xs):
				self.tag2tag.append(xs[0])
			else:
				self.tag2tag.append(" ")
		# else:
		# 	self.tag2tag = tag2tag
		self.matrix = []
		self.resultsMatrix = []
		for x in range(len(tag2tag)):
			self.matrix.append([])
			for _ in range(len(tag2tag)):
				self.matrix[x].append(0)

	def build(self, correctTagPath, resultingTagPath):
		for i in range(len(correctTagPath)):
			ctag = correctTagPath[i]
			rtag = resultingTagPath[i]
			self.total+=1
			if(ctag == rtag):
				self.correctlyTagged += 1
				self.resultsMatrix.append(' ')
			else:
				self.resultsMatrix.append('X')

			try:
				self.matrix[self.tag2tag.index(ctag)][self.tag2tag.index(rtag)]+=1
			except ValueError as e:
				print("%s or %s not in tag2tag" % (ctag, rtag))

	def getResults(self):
		ret = {}
		ret['accuracy'] = self.correctlyTagged / self.total
		ret['confusion_matrix'] = self.matrix
		ret['results_matrix'] = self.resultsMatrix
		return ret


