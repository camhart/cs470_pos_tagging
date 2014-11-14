import random
ROOT = [' ', ' ']
data = None
with open('test.txt') as f:
	data = f.read()

bigram = {}
keyValue = ROOT
for word in data.split():
	bigram.setdefault(' '.join(keyValue), []).append(word)
	keyValue.append(word)
	keyValue = keyValue[1:]

print(bigram)
print(bigram.keys())

curWord = ' '.join(ROOT)
print(curWord)
output = ""

for i in range(100):
	if(curWord in bigram.keys()):
		nextWord = random.choice(bigram.get(curWord))
		output = ' '.join([output, nextWord])
		curWord = nextWord
	# else:
		# print("huh")

print(output)