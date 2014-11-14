import json


with open('bigram_json_data.txt', 'r') as f:
	dataDict = json.loads(f.read())

for key, value in dataDict.items():
	# print(' '.join([key, str(value)]))
	for ca in range(len(value)):
		a = value[ca]
		count = 0
		for cb in range(ca):
			b = value[cb]
			if(a[1] == b[1]):
				count+=1
		if(count > 1):
			print("invalid data: count > 1 on %s - %d in %s" % (a[1], count, key))