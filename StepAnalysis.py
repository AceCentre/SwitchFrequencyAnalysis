import click
import csv
import os.path
import re

@click.command()
@click.option('--ssteps', type=click.Path(exists=True), default='scan-steps-lib/ssteps-eardu.csv', help='Path to a csv of your scan steps')
@click.option('--ssteps-add', type=int, default=0, help='Increment the scan steps')
@click.option('--ssteps-phrases', type=click.Path(), default='', help='Path to a csv of a second scan steps file. Should be whole words')
@click.option('--scanrate', default=1000, help='Scan rate in ms')
@click.option('--output-type', default='all', help='All, Lesher, Damper, Steps, Hits, show-workings, show-predictions, csv-all')
@click.option('--ignore-spaces', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--ignore-predicted', default=True, type=bool, help='Ignore predicted letters? i.e. anything uppercased gets lowercased and assumed he spoke it')
@click.option('--remove-predicted', default=False, type=bool, help='Remove predicted letters? i.e. ignore anything uppercased')
@click.option('--prediction-time', default=0, help='How long does it take the person to select a prediction on average? in ms. NB: Ignored if ignored-predictions is True')
@click.option('--sentence', prompt='Test sentence:',help='Enter your test sentence here')

def stepcount(ssteps, ssteps_add, ssteps_phrases, scanrate, ignore_spaces , ignore_predicted, remove_predicted, prediction_time, sentence, output_type):
	"""Takes a switch step count and a sentence and display number of steps to get there"""
	letterfreq = dict()
	sum = t_lesher = t_damper = sum_pred_letters = sum_pred_words = sum_words = 0
	show_workings = ''
	# remove dodgy chars
	# Bad code. Could do this a lot better if I spent 5 minutes
	s_filtered = re.sub(r"[0-9]+", '', sentence)
	s_filtered = re.sub(r"#+", '', s_filtered)
	s_filtered = re.sub(r"'+", '', s_filtered)
	s_filtered = re.sub(r"\/+", '', s_filtered)
	

	# predictions?
	for word in s_filtered.split():
		len_ucase_str = len(re.findall(r'[A-Z]',word))
		sum_pred_letters = sum_pred_letters + len_ucase_str
		sum_pred_words = sum_pred_words +1 if len_ucase_str > 0  else sum_pred_words


	# Ignore  predictions?
	#  NB: Its critical it gets called here. 
	#   Note this doesnt really do anything. By this point we've dealt with all the stats - they are just that. remove-predicted is more useful 
	if ignore_predicted:
		s_filtered = s_filtered.lower()

	# remove predictions?
	if remove_predicted:
		s_filtered = re.sub(r"[A-Z]+", '', s_filtered)

	s_filtered = s_filtered.lower()

	#calc word count
	sum_words = len(re.findall("[\w'-]+",s_filtered))
	
	wordblock = {}
	# Second scan step file
	if os.path.isfile(ssteps_phrases):
		with open(ssteps_phrases, 'rt') as cw:
			reader = csv.DictReader(cw)
			for row in reader:
				wordblock[row['Letter']]=str(int(row['Scan Steps'])+ssteps_add)

	phrase_steps = phrase_hits = 0
	# Gotcha. What if there is a double space.? This wont work. Note: CleanText should be run first on any code. Then this would be ok. 
	all_words = s_filtered.split(' ')
	non_blockedwords = list()
	for word in all_words:
		if word in wordblock:
			# the phrases need to have _ to correctly measure space but we dont want it
			#   for this analysis
			if word.endswith('_'):
				word = word[:-1]
			# strip word from s_filtered and add the 
			phrase_steps = phrase_steps + int(wordblock[word])
			phrase_hits = phrase_hits + 2
		else:
			non_blockedwords.append(word)

	# Now turn non_blockedwords back into s_filtered
	# NB: this was causing a mess - ignore spaces was being - ironically ignored. 
	#if ignore_spaces == False:
	#	s_filtered = '_'.join(non_blockedwords)

	# ignore spaces?
	if ignore_spaces:
		s_filtered = re.sub(r"\s+", '', s_filtered)
	else:
		s_filtered = re.sub(r"\s+", '_', s_filtered)

	strlen = len(s_filtered)
	
	
	if os.path.isfile(ssteps):
		with open(ssteps, 'rt') as f:
			reader = csv.DictReader(f)
			for row in reader:
				letterfreq[row['Letter']]=row['Scan Steps']
		# Lets first get the phrase steps 
		if (phrase_steps>0):
			sum = float(phrase_steps)
			t_lesher = t_lesher + ((float(phrase_steps)+2)*scanrate)
			t_damper = t_damper + ((float(phrase_steps)+1)*scanrate)
			show_workings = str(phrase_steps)+ ' steps to say words in core block. '+'\n'

		# Now we have the letter freq chart lets do our sums on this with our test sentences
		for n in s_filtered:
			sum = sum + float(letterfreq[n])
			t_lesher = t_lesher + ((float(letterfreq[n])+2)*scanrate)
			t_damper = t_damper + ((float(letterfreq[n])+1)*scanrate)
			show_workings = show_workings + n +' ' + letterfreq[n] + ', '

		if remove_predicted == False :
			t_lesher = t_lesher + sum_pred_words * prediction_time
			t_damper = t_damper + sum_pred_words * prediction_time
			show_workings = show_workings +  ' AND add sum of predicted words ('+ str(+sum_pred_words)+') * prediction_time (' + str(prediction_time) + ')'

		if ('csv-all' in output_type):
			# print a csv of all data..
			# headers = 'steps, hits, lesher (ms), damper (ms), no-hit (ms), predicted words, predicted letters, wordcount
			csv_line = str(sum) + ',' + str(strlen*2) + ',' + str(t_lesher) + ',' + str(t_damper) + ',' + str((sum)*scanrate) + ',' + str(sum_pred_words) + ',' + str(sum_pred_letters) + ',' + str(sum_words)
			print(csv_line)

		if ('Stats' in output_type or output_type == 'all'):
			print('Full steps:'+str(sum))
			# ss  100 (nb  na)/nb
			# nb - scan steps. na = augmented switch count.
			# 2 hits per letter. Its always that way
			print('Switch hits (auto scan - auto start):'+str(strlen*2+phrase_hits))
		if (('Lesher' in output_type) or (output_type == 'all')):
			print('Lesher time (H:M:S.ms), '+mstotime(t_lesher))
		if ('Damper' in output_type or output_type == 'all'):
			print('Damper time (H:M:S.ms), '+mstotime(t_damper))
		if ('No-Hit' in output_type or output_type == 'all'):
			print('No hit time (H:M:S.ms), '+mstotime((sum)*scanrate))
		if ('show-predictions' in output_type or output_type == 'all'):
			print('No. of predicted words '+ str(sum_pred_words))
			print('No. of predicted letters '+ str(sum_pred_letters))
		if ('show-workings' in output_type or output_type == 'all'):
			show_workings = 'string: ' + s_filtered + ' -> ' + show_workings + ' = Total steps of '+ str(sum) + '.\n Lesher Time = Σ (each step + 2) * scanrate (i.e. '+ str(scanrate) + ')\n'
			if remove_predicted == False :
				show_workings = show_workings +  '               AND add sum of predicted words ('+ str(+sum_pred_words)+') * prediction_time (' + str(prediction_time) + ')'
			print('Show workings:'+show_workings)
	else:
		return None


def mstotime(miliseconds):
	hours, milliseconds = divmod(miliseconds, 3600000)
	minutes, milliseconds = divmod(miliseconds, 60000)
	seconds = float(milliseconds) / 1000
	s = "%i:%02i:%06.3f" % (hours, minutes, seconds)
	return s

if __name__ == '__main__':
    stepcount()
