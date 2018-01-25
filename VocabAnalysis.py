import sys
import csv
import click
import os.path
from operator import itemgetter



def word_stats(file_name, ignore_spaces, remove_predicted):

	import re
	# balladin core_word_list
	core_words = ["a", "can", "about", "cant", "actually", "car", "after", "catholic", "afternoon", "cause", "again", "close", "ago", "cold", "ah", "come", "all", "coming", "alright", "could", "always", "couldnt", "an", "couple", "and", "crew", "another", "day", "any", "days", "anything", "dear", "anyway", "did", "are", "didnt", "around", "different", "as", "do", "ask", "does", "at", "doesnt", "away", "doing", "back", "dollars", "bad", "done", "be", "dont", "beautiful", "down", "because", "dunno", "been", "eat", "before", "eight", "being", "either", "better", "eleven", "big", "else", "bit", "end", "bloody", "enough", "break", "er", "but", "even", "buy", "ever", "by", "every", "cake", "everyone", "came", "everything", "ey", "hour", "fair", "hours", "feel", "house", "find", "how", "finished", "hundred", "first", "i", "five", "if", "for", "in", "four", "into", "friday", "is", "from", "isnt", "fucking", "it", "get", "its", "gets", "its", "getting", "id", "give", "ill", "go", "im", "god", "ive", "goes", "job", "going", "just", "gone", "keep", "gonna", "kids", "good", "know", "got", "last", "gotta", "left", "had", "like", "half", "little", "happened", "live", "hard", "long", "has", "look", "have", "looking", "havent", "looks", "having", "lost", "he", "lot", "her", "love", "here", "lovely", "hell", "lunch", "hes", "made", "him", "make", "his", "many", "home", "married", "me", "people", "mean", "person", "might", "phone", "mind", "pick", "mine", "place", "minutes", "play", "mm", "pretty", "monday", "probably", "money", "put", "months", "quite", "more", "ready", "morning", "really", "much", "remember", "mum", "right", "must", "road", "my", "round", "name", "said", "need", "same", "never", "saturday", "new", "say", "next", "saying", "nice", "says", "night", "school", "no", "see", "not", "seen", "nothing", "seven", "now", "she", "of", "shell", "off", "shes", "oh", "shit", "ok", "shoes", "old", "should", "on", "sit", "once", "six", "one", "so", "ones", "some", "only", "someone", "or", "something", "other", "sorry", "our", "sort", "out", "start", "over", "started", "own", "still", "oclock", "straight", "past", "street", "pay", "stuff", "sure", "us", "take", "used", "talk", "very", "talking", "want", "tea", "wanted", "tell", "wants", "ten", "was", "than", "wasnt", "thanks", "way", "that", "we", "thats", "week", "the", "weekend", "their", "weeks", "them", "well", "then", "went", "there", "were", "theres", "were", "these", "weve", "they", "what", "theyre", "whats", "theyve", "when", "thing", "where", "things", "which", "think", "who", "thirty", "whos", "this", "why", "those", "will", "though", "with", "thought", "won", "three", "wont", "through", "work", "til", "working", "time", "would", "times", "wouldnt", "to", "wrong", "today", "yeah", "told", "year", "tomorrow", "years", "too", "yep", "try", "yes", "trying", "yesterday", "twelve", "you", "twenty", "your", "two", "youre", "um", "youve", "up"]
	file = open(file_name, "r")
	lines = file.readlines()
	predicted_words = 1
	words_per_sentence = []
	pwords = dict()
	in_core = dict()
	words = []
	for line in lines:
		if any(s.isupper() for s in line):
			wordss = re.findall('\w+', line)
			for worda in wordss:
				# Core words?
				if worda.lower() in core_words:
					if worda.lower() in in_core:
						in_core[worda.lower()]=in_core[worda.lower()]+1
					else:
						in_core[worda.lower()]=1
				# Predicted?
				if any(d.isupper() for d in worda):
					if worda.lower() in pwords:
						pwords[worda.lower()]=pwords[worda.lower()]+1
					else:
						pwords[worda.lower()]=1
					predicted_words = predicted_words+1
		# WPS
		words_per_sentence.append(len(re.findall('\w+', line.lower())))
	avg_wps = sum(words_per_sentence) / float(len(words_per_sentence))
	max_wps = max(words_per_sentence)
	file = open(file_name, "r")
	chars = file.read()
	# remove dodgy chars
	# Bad code. Could do this a lot better if I spent 5 minutes
	chars_filtered = re.sub(r"[0-9]+", '', chars)
	chars_filtered = re.sub(r"#+", '', chars_filtered)
	chars_filtered = re.sub(r"'+", '', chars_filtered)
	chars_filtered = re.sub(r"\/+", '', chars_filtered)

	if remove_predicted:
		chars_filtered = re.sub(r"[A-Z]+", '', chars_filtered)
	else:
		chars_filtered = chars_filtered.lower()

	#Lets deal with lines
	# We don't want to treat a linebreak as a space
	lines = chars_filtered.splitlines()
	
	for i, line in enumerate(lines):
		# Word count
		words.extend(re.findall("[\w'-]+", line))
		# ignore spaces?
		if ignore_spaces:
			lines[i] = re.sub(r"\s+", '', line)
		else:
			lines[i] = re.sub(r"\s+", '_', line)

	chars_filtered = ''.join(lines)
	avgWordLen = sum(map(len, words))/len(words)
	from collections import Counter
	charcount = Counter(chars_filtered).most_common()
	wordcount = Counter(words).most_common()	
	total_words = total_pred = totalin_core = total_chr = 0
	# Totals
	# All words	
	total_words = sum(n for _, n in wordcount)
	# Predicted words
	total_pred = sum(pwords.values())
	# In core
	totalin_core = sum(in_core.values())
	# All chars
	totalchr = sum(n for _, n in charcount)
	
	totals_list = {'total_words':total_words, 'total_pred':total_pred, 'totalin_core':totalin_core,'totalchr':totalchr}
	return float(avgWordLen), charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core, totals_list


# Ignore all letters after an uppercase character
def getCharsSpoken(wordlist):
	cl = list()
	for word in wordlist:
		for c in word:
			if c.islower():
				 cl.append(c)
	return cl

# Given a list of words, remove any that are
# in a list of stop words.

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

@click.command()
@click.option('--vocab-file', type=click.Path(exists=True), default='examples/vocab-cleaned.txt', help='Path to a vocab file. String on each line. ')
@click.option('--ignore-spaces', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--ssteps', type=click.Path(exists=True), default='scan-steps-lib/ssteps-eardu.csv', help='Path to a csv of your scan steps')
@click.option('--ssteps-add', type=int, default=0, help='Increment the scan steps')
@click.option('--stop-words', default=False, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--remove-predicted', default=False, type=bool, help='Remove predicted letters? i.e. ignore anything uppercased')
@click.option('--output', default='Print', type=str, help='Do you want to Print or Save the results or both?')

def mainHandler(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted, output):
	if output == 'Print':
		printStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted)
	elif output == 'Write':
		writeStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted)
	else:
		printStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted)
		writeStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted)
		

# Open file.
#  NB: Each line is a sentence. Only uppercase letters which have been predicted by a partner - INCLUDING first letters
def printStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted):
	
	avgWordLen, charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core, totals_list = word_stats(vocab_file, ignore_spaces, remove_predicted)
	print("all words:")
	print('\n'.join(str(x) + ',' + str(y) for x, y in wordcount))
	print("------")
	print("predicted words:")
	for itemp in sorted(pwords, key=pwords.get, reverse=True):
		print(itemp, pwords[itemp])
	print("------")
	print("in core:")
	for itemc in in_core:
		print(itemc+','+str(in_core[itemc]))
	print("------")
	print("total chars:")
	print('\n'.join(str(x) + ',' + str(y) for x, y in charcount))
	#{'total_words':total_words, 'total_pred':total_pred, 'totalin_core':totalin_core,'totalchr':totalchr}
	print("total words:" + str(totals_list['total_words']))
	print("total chars:" + str(totals_list['totalchr']))
	print("words in core:" + str(len(in_core)))
	print("total words (i.e. inc repeats) in core:" + str(totals_list['totalin_core']))
	print("avg word len:" +str(avgWordLen))
	print("avg wps:" + str(avg_wps))
	print("max wps:" + str(max_wps))
	print("predicted words:" + str(predicted_words))
	print("------")
	lines, totalFreqScan = getScanxFreqChart(charcount, ssteps, ssteps_add)
	print('Letter count,Frequency,Letter,Scan Steps,FreqXScanSteps')
	print(lines)
	print("Total Frequency X Scan Steps:", totalFreqScan)

def writeStats(vocab_file, ignore_spaces, ssteps, ssteps_add, stop_words, remove_predicted):
	
	avgWordLen, charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core, totals_list = word_stats(vocab_file, ignore_spaces, remove_predicted)
	with open('output-all-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['phrase','freq'])
		for x, y in wordcount:
			writer.writerow([str(x),str(y)])
	with open('output-pred-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for itemp in sorted(pwords, key=pwords.get, reverse=True):
			writer.writerow([itemp, pwords[itemp]])
	with open('output-incore-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for itemc in in_core:
			writer.writerow([itemc, in_core[itemc]])
	with open('output-all-chars.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for x, y in charcount:
			writer.writerow([str(x),str(y)])
	with open('output-freqfinal-words.csv', 'w') as txt_file:
		txt_file.write('Letter count,Frequency,Letter,Scan Steps,FreqXScanSteps\n')
		lines, totalFreqScan = getScanxFreqChart(charcount, ssteps, ssteps_add)
		txt_file.write(lines)
				
		
def getScanxFreqChart(charcount, ssteps, ssteps_add):
	#scan_steps = {'e':2,'t':4,'o':7,'a':3,'n':9,'i':8,'s':5,'r':6,'h':4,'l':3,'d':8,'u':9,'w':4,'f':9,'m':5,'c':5,'g':7,'p':6,'b':8,'y':7,'k':6,'v':10,'x':6,'j':11,'z':7,'q':5}
	# Heidis Scan steps - "Full" steps
	#scan_steps = { 'e':0,'t':2,'o':5,'a':1,'n':7,'i':6,'s':3,'r':4,'h':2,'l':1,'d':6,'u':7,'w':2,'f':7,'m':3,'c':3,'g':5,'p':4,'b':6,'y':5,'k':4,'v':8,'x':4,'j':9,'z':5,'q':3}
	scan_steps = dict()
	if os.path.isfile(ssteps):
		with open(ssteps, 'rt') as f:
			reader = csv.DictReader(f)
			for row in reader:
				scan_steps[row['Letter']]=str(int(row['Scan Steps'])+ssteps_add)
	
	totalchr = sum(n for _, n in charcount)
	charcount.sort(key=itemgetter(1), reverse=True)
	totalFreqScan = 0
	lines = ''
	for l,f in charcount:
		lines = lines + str(float(f))+','+str(float(f)/totalchr)+','+l+','+ scan_steps[l]+','+ str((float(f)/totalchr) * int(scan_steps[l]))+'\n' 
		totalFreqScan = totalFreqScan + ((float(f)/totalchr) * int(scan_steps[l]))
	return lines[:-3], totalFreqScan

if __name__ == '__main__':
	mainHandler()