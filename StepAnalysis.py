import click
import csv
import os.path
import re

@click.command()
@click.option('--ssteps', default='steps.csv', help='Path to a csv of your scan steps')
@click.option('--scanrate', default=1000, help='Scan rate in ms')
@click.option('--ignore-spaces', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--sentence', prompt='Test sentence:',
				help='Enter your test sentence here')

def stepcount(ssteps, scanrate, ignore_spaces ,sentence):
	"""Takes a switch step count and a sentence and display number of steps to get there"""
	letterfreq = dict()
	sum = 0
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
			
	if os.path.isfile(ssteps):
		with open(ssteps, 'rt') as f:
			reader = csv.DictReader(f)
			for row in reader:
				letterfreq[row['Letter']]=row['Scan Steps']
		# Now we have the letter freq chart lets do our sums on this with our test sentences
		for n in s_filtered:
			sum = sum + int(letterfreq[n])
				
		print('Full steps:'+str(sum))
		# ss  100 (nb  na)/nb
		# nb - scan steps. na = augmented switch count.
		print('Switch hits:'+str(strlen*2))
		# Damper: 1/2 per switch hit. Takes two hits per letter so just length of str
		print('Damper time (H:M:S.ms):'+mstotime((sum+strlen)*scanrate))
		print('Lesher time (H:M:S.ms):'+mstotime((sum+(strlen*2))*scanrate))
		print('No hit time (H:M:S.ms):'+mstotime((sum)*scanrate))		
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
