'''
	AddSteps.py --ssteps scan-steps-lib/ssteps-db.csv --freqtable output-all-words.csv --write-to-col 'spell:db orig' --addspace True
	
	AddSteps.py --ssteps scan-steps-lib/ssteps-phrase-6x6.csv --sstep-type Phrases --freqtable output-all-words.csv --write-to-col 'phrase:6x6'
	
	## What this  does?
	
	Takes in a scan step csv chart (letter/phrase|steps\n) and a frequency list (phrase|frequency(count)\n) and adds a new column to the frequency chart of the steps to the steps to write the phrase with this scan step layout.
	
	Note use add space to emulate adding a space at the end of each phrase. Your scan step chart will need to have a _ character in it however
	
	
'''
import sys
import csv
import click
import os.path
import re
from collections import OrderedDict

def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

@click.command()
@click.option('--ssteps', type=click.Path(exists=True), default='scan-steps-lib/ssteps-eardu.csv', help='Path to a csv of your scan steps')
@click.option('--ssteps-add', default=0, help='Want to increment the scan step amount?')
@click.option('--freqtable', type=click.Path(exists=True), default='output-all-words.csv', help='Path to a csv of your words|frequency csv')
@click.option('--sstep-type', default='Letters', help='Letters or Phrases')
@click.option('--write-to-col', default='', help='Wamt to write the scan steps in a new column? Provide the string of the title here ')
@click.option('--addspace', default=False, help='Add a space at the end of each phrase?')

def stepcalc(ssteps,ssteps_add,freqtable,sstep_type,write_to_col,addspace):
	# Get Scan Steps
	letterfreq = freqlist = dict()
	if os.path.isfile(ssteps):
		with open(ssteps, 'rt') as f:
			reader = csv.DictReader(f)
			for row in reader:
				letterfreq[row['Letter']]=str(int(row['Scan Steps'])+ssteps_add)

	# Now get each word
	# We cant read and write at same time 
	new_rows_list = []
	indexPhrase = 0
	indexFreq = 1
	
	if os.path.isfile(freqtable):
		with open(freqtable, "rt", encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile)
			for i, row in enumerate(reader):
				if (i == 0):
					fieldnames = row
					fieldnames.append(write_to_col)
					if ('phrase' in fieldnames):
						indexPhrase = fieldnames.index('phrase')
					if ('freq' in fieldnames):
						indexFreq = fieldnames.index('freq')						
				r = 1
				sum = 0
				if (hasNumbers(row[indexPhrase])==False):
					if sstep_type == 'Letters':
						if (addspace):
							row[indexPhrase] = row[indexPhrase] + '_'
						for letter in row[indexPhrase]:
							sum = sum + float(letterfreq[letter])
					else:
						if (row[indexPhrase] in letterfreq):
							sum = float(letterfreq[row[indexPhrase]])
				new_row = [row[indexPhrase], row[indexFreq], str(sum)]
				new_rows_list.append(new_row)
			csvfile.close()

		# Now write it
		with open(freqtable, 'w') as csvfile:
			writer = csv.writer(csvfile,delimiter=',', lineterminator='\n')
			for row in new_rows_list:
				writer.writerow(row)
			csvfile.close()
	else:
		return None


if __name__ == '__main__':
	stepcalc()
