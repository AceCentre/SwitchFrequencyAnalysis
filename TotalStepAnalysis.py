import subprocess, csv
import click
import os.path

def mstotime(ms):
	ms = float(ms)
	s=ms/1000
	m,s=divmod(s,60)
	h,m=divmod(m,60)
	d,h=divmod(h,24)

	return ("%d:%d:%d:%d" % (d, h, m, s))


@click.command()
@click.option('--text-file', default='', help='name of text file to input')
@click.option('--layouts', default='all', help='Which layouts do you want parsing? all, aeiou, abcd, db, eardu, qwerty, dbfreq')
@click.option('--text', default="""the quick brown fox jumped over the lazy dog""", help='a line of text to analyse. NB: ignored if text file provided')
@click.option('--scanrate', default=1000, help='Scan rate in ms')
@click.option('--ssteps-add', default=0, help='Want to increment the scan step amount?')
@click.option('--ignore-spaces', default=False, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--ignore-predicted', default=True, type=bool, help='Ignore predicted letters? i.e. anything uppercased gets lowercased')
@click.option('--remove-predicted', default=False, type=bool, help='Remove predicted letters? i.e. ignore anything uppercased')
@click.option('--prediction-time', default=500, help='How long does it take the person to select a prediction on average? in ms. NB: Ignored if ignored-predictions is True')


def textAnalyse(text_file, layouts, text, scanrate, ssteps_add, ignore_spaces , ignore_predicted, remove_predicted, prediction_time):
	python_bin = '/usr/local/bin/python3'
	base_cmd = python_bin + '  StepAnalysis.py --ssteps scan-steps-lib/ssteps-nnnn.csv --ssteps-add '+ str(ssteps_add)+' --ignore-spaces '+str(ignore_spaces)+' --ignore-predicted '+str(ignore_predicted)+' --remove-predicted '+str(remove_predicted)+' --prediction-time '+str(prediction_time)+' --output-type csv-all --sentence '

	if text_file != '':
		if os.path.exists(text_file):
			file = open(text_file, "r")
			text = file.read()
		else:
			print('!!! Sorry. File doesnt exist')

	lines = text.splitlines()
	if (layouts == 'csvns'):
		print('line, predicted words, predicted letters, wordcount, hits,  dbNS-steps,  dbNS-lesher (ms), dbNS-damper (ms), dbfreqNS-steps, dbfreqNS-lesher, dbfreqNS-damper (ms), qwerty-steps, qwerty-lesher (ms), qwerty-damper (ms),eardu-steps, eardu-lesher (ms), eardu-damper (ms), abcd-steps, abcd-lesher (ms), abcd-damper (ms), aeiou-steps, aeiou-lesher (ms), aeiou-damper (ms)')

	elif (layouts == 'csv'):
		print('line, predicted words, predicted letters, wordcount, hits,  abcd-steps,  abcd-lesher (ms), abcd-damper (ms), db-steps,  db-lesher (ms), db-damper (ms), dbNS-steps,  dbNS-lesher (ms), dbNS-damper (ms), dbfreq-steps, dbfreq-lesher (ms), dbfreq-damper (ms), dbfreqNS-steps, dbfreqNS-lesher, dbfreqNS-damper (ms), qwerty-steps, qwerty-lesher (ms), qwerty-damper (ms), qwertyNS-steps, qwertyNS-lesher (ms), qwertyNS-damper (ms), aeiou-steps, aeiou-lesher (ms), aeiou-damper (ms),eardu-steps, eardu-lesher (ms), eardu-damper (ms), earduNS-steps, earduNS-lesher (ms), earduNS-damper (ms)')
	else:
		print('line, layout, steps, hits, lesher (ms), damper (ms), no-hit (ms), predicted words, predicted letters, wordcount')


	for line in lines:
		# send
		# output a csv of the csv!
		if (layouts == 'csvns'):

			abcdns_cmd = base_cmd.replace("nnnn", "abcd-nospace")
			abcdns = subprocess.Popen(abcdns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			aeiouns_cmd = base_cmd.replace("nnnn", "aeiou-nospace")
			aeiouns = subprocess.Popen(aeiouns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			dbns_cmd = base_cmd.replace("nnnn", "db-nospace")
			dbns = subprocess.Popen(dbns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			dbfreqns_cmd = base_cmd.replace("nnnn", "dbfreq-nospace")
			dbfreqns = subprocess.Popen(dbfreqns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			qwertyns_cmd = base_cmd.replace("nnnn", "qwerty-nospace")
			qwertyns = subprocess.Popen(qwertyns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			earduns_cmd = base_cmd.replace("nnnn", "eardu-nospace")
			earduns = subprocess.Popen(earduns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			print(line+','+dbns[5]+','+dbns[6]+','+dbns[7]+','+dbns[1]
			+','+dbns[0]+','+dbns[2]+','+dbns[3]
			+','+dbfreqns[0]+','+dbfreqns[2]+','+dbfreqns[3]
			+','+qwertyns[0]+','+qwertyns[2]+','+qwertyns[3]
			+','+earduns[0]+','+earduns[2]+','+earduns[3]
			+','+abcdns[0]+','+abcdns[2]+','+abcdns[3]
			+','+aeiouns[0]+','+aeiouns[2]+','+aeiouns[3])

		if (layouts == 'csv'):

			abcd_cmd = base_cmd.replace("nnnn", "abcd")
			abcd = subprocess.Popen(abcd_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			db_cmd = base_cmd.replace("nnnn", "db")
			db = subprocess.Popen(db_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			dbns_cmd = base_cmd.replace("nnnn", "db-nospace")
			dbns = subprocess.Popen(dbns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			dbfreq_cmd = base_cmd.replace("nnnn", "dbfreq")
			dbfreq = subprocess.Popen(dbfreq_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			dbfreqns_cmd = base_cmd.replace("nnnn", "dbfreq-nospace")
			dbfreqns = subprocess.Popen(dbfreqns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			qwerty_cmd = base_cmd.replace("nnnn", "qwerty")
			qwerty = subprocess.Popen(qwerty_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			qwertyns_cmd = base_cmd.replace("nnnn", "qwerty-nospace")
			qwertyns = subprocess.Popen(qwertyns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			eardu_cmd = base_cmd.replace("nnnn", "eardu")
			eardu = subprocess.Popen(eardu_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			earduns_cmd = base_cmd.replace("nnnn", "eardu-nospace")
			earduns = subprocess.Popen(earduns_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')

			aeiou_cmd = base_cmd.replace("nnnn", "aeiou")
			aeiou = subprocess.Popen(aeiou_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip().split(',')


			#steps - 0, hits 1 , lesher (ms) 2, damper (ms) 3, no-hit (ms) 4, predicted words 5, predicted letters 6, wordcount 7
			#'line, predicted words, predicted letters, wordcount, hits,  abcd-steps,  abcd-lesher (ms), abcd-damper (ms), db-steps,  db-lesher (ms), db-damper (ms), dbfreq-steps, dbfreq-lesher (ms), dbfreq-damper (ms), dbfreqNS-steps, dbfreqNS-lesher (ms), dbfreqNS-damper (ms), qwerty-steps, qwerty-lesher (ms), qwerty-damper (ms),aeiou-steps, aeiou-lesher (ms), aeiou-damper (ms),eardu-steps, eardu-lesher (ms), eardu-damper (ms)'

			print(line+','+abcd[5]+','+abcd[6]+','+abcd[7]+','+abcd[1]
			+','+abcd[0]+','+abcd[2]+','+abcd[3]
			+','+db[0]+','+db[2]+','+db[3]
			+','+dbns[0]+','+dbns[2]+','+dbns[3]
			+','+dbfreq[0]+','+dbfreq[2]+','+dbfreq[3]
			+','+dbfreqns[0]+','+dbfreqns[2]+','+dbfreqns[3]
			+','+qwerty[0]+','+qwerty[2]+','+qwerty[3]
			+','+qwertyns[0]+','+qwertyns[2]+','+qwertyns[3]
			+','+aeiou[0]+','+aeiou[2]+','+aeiou[3]
			+','+eardu[0]+','+eardu[2]+','+eardu[3]
			+','+earduns[0]+','+earduns[2]+','+earduns[3])


			'''
			print(line+','+abcd[5]+','+abcd[6]+','+abcd[7]+','+abcd[1]
			+','+abcd[0]+','+mstotime(abcd[2])+','+mstotime(abcd[3])
			+','+db[0]+','+mstotime(db[2])+','+mstotime(db[3])
			+','+dbfreq[0]+','+mstotime(dbfreq[2])+','+mstotime(dbfreq[3])
			+','+dbfreqns[0]+','+mstotime(dbfreqns[2])+','+mstotime(dbfreqns[3])
			+','+qwerty[0]+','+mstotime(qwerty[2])+','+mstotime(qwerty[3])
			+','+aeiou[0]+','+mstotime(aeiou[2])+','+mstotime(aeiou[3])
			+','+eardu[0]+','+mstotime(eardu[2])+','+mstotime(eardu[3]))
			'''

		else:

			if (('abcd' in layouts) or (layouts == 'all')):
				abcd_cmd = base_cmd.replace("nnnn", "abcd")
				abcd = subprocess.Popen(abcd_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',abcd,'+abcd.strip())
			if (('eardu' in layouts) or (layouts == 'all')):
				eardu_cmd = base_cmd.replace("nnnn", "eardu")
				eardu = subprocess.Popen(eardu_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',eardu,'+eardu.strip())
			if (('aeiou' in layouts) or (layouts == 'all')):
				aeiou_cmd = base_cmd.replace("nnnn", "aeiou")
				aeiou = subprocess.Popen(aeiou_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',aeiou,'+aeiou.strip())
			if (('db' in layouts) or (layouts == 'all')):
				db_cmd = base_cmd.replace("nnnn", "db")
				db = subprocess.Popen(db_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',db,'+db.strip())
			if (('dbfreq' in layouts) or (layouts == 'all')):
				dbfreq_cmd = base_cmd.replace("nnnn", "dbfreq")
				dbfreq = subprocess.Popen(dbfreq_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',dbfreq,'+dbfreq.strip())
			if (('qwerty' in layouts) or (layouts == 'all')):
				qwerty_cmd = base_cmd.replace("nnnn", "qwerty")
				qwerty = subprocess.Popen(qwerty_cmd + '"'+line+'"', shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
				print(line+',qwerty,'+qwerty.strip())

if __name__ == '__main__':
    textAnalyse()
