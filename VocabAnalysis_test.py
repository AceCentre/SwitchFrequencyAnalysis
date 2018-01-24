import VocabAnalysis as va
import CleanText 

def test_word_stats():
	avgWordLen, charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core, totals = va.word_stats('examples/vocab-cleaned.txt', False, True)
	lines, totalFreqScan = va.getScanxFreqChart(charcount, 'scan-steps-lib/ssteps-qwerty.csv', 0)
	assert avgWordLen == 3.3846153846153846
	assert avg_wps == 5.777777777777778
	assert max_wps == 8
	assert predicted_words == 4
	assert totalFreqScan == 4.333333333333331


if __name__ == '__main__':
	test_word_stats()
