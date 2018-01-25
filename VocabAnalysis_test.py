import VocabAnalysis as va
import CleanText 
import StepAnalysis as sa 

def test_word_stats():
	avgWordLen, charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core, totals = va.word_stats('examples/vocab-cleaned.txt', False, True)
	lines, totalFreqScan = va.getScanxFreqChart(charcount, 'scan-steps-lib/ssteps-qwerty.csv', 0)
	assert avgWordLen == 3.3846153846153846
	assert avg_wps == 5.777777777777778
	assert max_wps == 8
	assert predicted_words == 4
	assert round(totalFreqScan, 3) == round(4.333333333333331, 3)

def test_step_stats():
	# Our Vars to test
	sentence = 'the quick brown fox jumps over the lazy dog'
	ssteps='scan-steps-lib/ssteps-abcd.csv'
	ssteps_add=0
	ssteps_phrases=''
	scanrate=1000
	ignore_spaces=True
	ignore_predicted=False
	remove_predicted=False
	prediction_time=0 
	output_type='code'
	steps, hits, lesher, damper, no_hit, predicted_words, predicted_letters, wordcount, phrase_hits, show_workings = sa.stepcountCalc(ssteps, ssteps_add, ssteps_phrases, scanrate, ignore_spaces , ignore_predicted, remove_predicted, prediction_time, sentence)
	#print(steps, hits, lesher, damper, no_hit, predicted_words, predicted_letters, wordcount, show_workings)
	assert steps == 143.0
	assert hits == 70 
	assert lesher == 213000.0
	assert damper == 178000.0
	assert no_hit == 143000.0 
	assert predicted_words == 0 
	assert predicted_letters == 0 
	assert wordcount == 9

if __name__ == '__main__':
	test_step_stats()
