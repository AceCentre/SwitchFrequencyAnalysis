'''
	MakeStepChart.py --columns 6 --rows 6
	
	## What this  does?
	
	Makes a step chart in a block of n x n cols and rows.
	Then from frequency list and then applies this to finding the steps in this chart and writing the scan step lib
	
	Note: The provided list MUST be already sorted in frequency order
	
'''
import sys
import csv
import click
import os.path
import re

def makesteps(columns,rows,startat):
	cell_size = columns * rows
	table= [ [ 0 for i in range(columns) ] for j in range(rows) ]
	stepcounts = []
	for d1 in range(rows):
		for d2 in range(columns):
			stepcount = d1+d2+startat
			table[d1][d2]= stepcount
			stepcounts.append(stepcount)
	
	return table, cell_size, stepcounts


def hasNumbers(inputString):
	return bool(re.search(r'\d', inputString))

@click.command()
@click.option('--freqtable', type=click.Path(exists=True), default='output-all-words.csv', help='Path to a csv of your words|frequency csv')
@click.option('--columns', default=6, help='Columns')
@click.option('--rows', default=6, help='Rows')
@click.option('--startat', default=0, help='What should the first element start at? 0? 1? 2?')
@click.option('--newfile', default='scan-steps-lib/ssteps-phrase-nn.csv', help='Name the new file')
@click.option('--ignore-let-less', default=0, help='ignore letters less than n length')

def mapfreqtotable(freqtable,columns,rows,startat,newfile,ignore_let_less):

	table, cell_size, stepcounts = makesteps(columns,rows,startat)
	steprange = range(startat, max(int(num) for num in stepcounts))
	stepcounts = sorted(stepcounts)
	
	# now lets work out where it should be.. what steps it would be if optimised
	new_rows_list = new_row = old_rows_list = []

	if os.path.isfile(freqtable):
		with open(freqtable, "rt", encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile)
			alines = []
			for d, x in enumerate(reader):
				if (len(x[0]) >= ignore_let_less):
					alines.append(x)
					
			for i, line in enumerate(alines):
				print(line)
				# this is a bit naff. Gets the header names
				if (i == 0):
					fieldnames = ['Letter','Scan Steps']
				else:
					# Ok - now loop through the nice little step matrix we made from makesteps
					if (i<len(stepcounts)):
						new_row = [line[0],stepcounts[i-1]]
						new_rows_list.append(new_row)
				
		csvfile.close()
		
		# Now write the step count chart
		if (newfile == 'scan-steps-lib/ssteps-phrase-nn.csv'):
			newfile = newfile.replace('nn',str(columns)+'x'+str(rows)) 
		
		with open(newfile, 'w') as csvfile:
			writer = csv.writer(csvfile,delimiter=',', lineterminator='\n')
			writer.writerow(fieldnames)
			for row in new_rows_list:
				writer.writerow(row)
			csvfile.close()

		print ('Your scanning table will look like')	
		for rrow in table:
			print(' | '.join(str(e) for e in rrow))


if __name__ == '__main__':
	mapfreqtotable()
