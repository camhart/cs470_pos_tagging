File descriptions

data/*.json	- trained data files.  Used by ngramparagraph.py and viterbi.py
viterbi.py - Viterbi algorithm implementation for both 1st and 2nd order hmm.  Depends on data/*.json.
				All values are hard coded (no input parameters).  Modify seed word, tag to word, and
				tag to tag files to change trained data.  Modify the "devtest.txt" string to change 
unigram.py - Builds paragraphs using unigram data.  Does NOT generate tags then words off the tags.  Just
				generates words based off previous words (does so at random).
t2.py - generates json data of tag to word transition table (rename output file and place in data/ folder)
t1_2.py - generates json data for 2nd order transition table (rename output file and place in data/ folder)
t1.py - generates json data for 1st order transition table (rename output file and place in data/ folder)
report.pdf - report file
ngramparagraph.py - generates a paragraph using values in data/at*.json
ngram.py - ignore, doesn't work (doesn't need to)
confusion.py - confusion matrix class
bigram.py - ignore, doesn't work (doesn't need to)
allTraining.txt - training data, required for t2.py, t1.py, t1_2.py