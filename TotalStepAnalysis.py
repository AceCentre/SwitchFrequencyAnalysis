import click
import csv
import os.path
import re

def mstotime(miliseconds):
	hours, milliseconds = divmod(miliseconds, 3600000)
	minutes, milliseconds = divmod(miliseconds, 60000)
	seconds = float(milliseconds) / 1000
	s = "%i:%02i:%06.3f" % (hours, minutes, seconds)
	return s


@click.command()
@click.option('--ssteps', type=click.Path(exists=True), default='scan-steps-lib/ssteps-eardu.csv', help='Path to a csv of your scan steps')
@click.option('--scanrate', default=1000, help='Scan rate in ms')
@click.option('--vocab-file', type=click.Path(exists=True), default='examples/test.txt', help='Path to your vocab file')
@click.option('--ignore-spaces', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')

def getTotalVocabTime(ssteps, scanrate, ignore_spaces , vocab_file):
	"""Takes a switch step count and a vocab file and display number of secs to get there"""
	letterfreq = dict()
	file = open(vocab_file, "r")
	lines = file.readlines()
	predicted_words = 1
	words_per_sentence = []
	pwords = dict()
	full_steps = 0
	switch_hits = 0
	damper_time = 0
	leshher_time = 0
	nohit_time = 0


	with open(ssteps, 'rt') as f:
		reader = csv.DictReader(f)
		for row in reader:
			letterfreq[row['Letter']]=row['Scan Steps']
	
	
	for sentence in lines:		
		# remove dodgy chars
		# Bad code. Could do this a lot better if I spent 5 minutes 
		s_filtered = re.sub(r"[0-9]+", '', sentence.lower())
		s_filtered = re.sub(r"#+", '', s_filtered)
		s_filtered = re.sub(r"'+", '', s_filtered)
		s_filtered = re.sub(r"\/+", '', s_filtered)
		s_filtered2 = re.sub(r"\s+", '', s_filtered)

		# ignore spaces?
		if ignore_spaces:
			strlen = len(s_filtered2)
		else:
			strlen = len(s_filtered)

		s_filtered = s_filtered2
			
		# Now we have the letter freq chart lets do our sums on this with our test sentences
		sum = 0
		for n in s_filtered:
			sum = sum + int(letterfreq[n])
				
		full_steps +=sum 
		# ss  100 (nb  na)/nb
		# nb - scan steps. na = augmented switch count.
		switch_hits += strlen*2
		# Damper: 1/2 per switch hit. Takes two hits per letter so just length of str
		damper_time = damper_time + ((sum+strlen)*scanrate)
		leshher_time = leshher_time + ((sum+(strlen*2))*scanrate)
		nohit_time = nohit_time + ((sum)*scanrate)

	print('Damper time (H:M:S.ms):'+mstotime(damper_time))
	print('Lesher time (H:M:S.ms):'+mstotime(leshher_time))
	print('No hit time (H:M:S.ms):'+mstotime(nohit_time))		
	

if __name__ == '__main__':
    getTotalVocabTime()
