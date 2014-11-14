import random
ROOT = ' '
data = None
with open('test.txt') as f:
	data = f.read()


unigram = {}
oldWord = ROOT
for word in data.split():
	unigram.setdefault(oldWord, []).append(word)
	oldWord = word

print(unigram)

curWord = ROOT
output = ""

for i in range(100):
	if(curWord in unigram.keys()):
		nextWord = random.choice(unigram.get(curWord))
		output = ' '.join([output, nextWord])
		curWord = nextWord

print(output)