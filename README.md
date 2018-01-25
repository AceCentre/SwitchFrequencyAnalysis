# Switch Scanning Analysis

[![Build Status](https://travis-ci.org/ACECentre/SwitchFrequencyAnalysis.svg?branch=master)](https://travis-ci.org/ACECentre/SwitchFrequencyAnalysis)

## Scripts and code to analyse switch scanning layouts for clients and their vocabulary

More text to follow soon

Whats in here:

1. VocabAnalysis.py Pass in a clients vocabulary (see examples/vocab.txt for the kind of format of this) and will output a lot of statistcs on this data. NB: choose the right scan steps - right now hardcoded in the top of the file. 
2. StepAnalysis.py. Read in a scan step csv and provide a test sentence (and if you wish a scan rate) and will give estimates for time to take to write this message.
3. TotalStepAnalysis.py. Read in a scan step csv and provide a vocab file (and if you wish a scan rate) and will give estimates for time to take to write the entire vocab.
4. scan-steps-lib/ a library of scan steps for different layouts. 
5. Mapper/ - a funky script that tries to show you what a frequency list would like in a grid you make. NB: Very work in progress. Dont get your hopes up! 
6. AddSteps.py Takes in a scan step csv chart (letter/phrase|steps\n) and a frequency list (phrase|frequency(count)\n) and adds a new column to the frequency chart of the steps to the steps to write the phrase with this scan step layout.
7. MakeStepChart.py Makes a step chart in a block of n x n cols and rows. Outputs to a csv of phrase|step

### To run

NB: Requires Python 3!

`pip install -r requirements.txt`

then run whichever. e.g:

`python3 VocabAnalysis.py --vocab-file path-to-file.txt`

`python3 StepAnalysis.py --ssteps path-to-step-scanning-lib-file.txt --scanrate 1`

`python3 MakeStepChart.py --columns 6 --rows 6 --freqtable path-to-freqtable.csv --startat 2`

`python3 StepAnalysis.py --ssteps path-to-step-scanning-lib-file.txt --ignore-spaces False --ssteps-phrases scan-steps-lib/ssteps-phrase-6x6.csv `


## Common usages

1. You have a vocabulary file that you want to analyse. Run VocabAnalysis.py - it will output some csv files - that you can then use to analyse the frequency of word and letter use
2. You want to convert a ordered list of words or letters (in frequency order) and give a suggestion of the scan steps in a n x n block. Run MakeStepChart 
3. You want to Add these steps to your frequency list so you can compare different scan steps. Run AddSteps.py
4. You want to an estimation of time and efficiency between scan steps and a test sentences(s). Run StepAnalysis. If you want to do across a whole bunch of Scan Step layouts look at TotalStepAnalysis


### To-Do:

1. Provide some screenshots for each scan-steps-lib/ file
2. Clean up code to make more readable and usable (e.g. dont hardcode the scan steps in VocabAnalysis)
3. Right now code is designed to strip out non-Alpha characters. This is a bad idea if you want to analyse this in your code


### Thanks

- Massive thanks to Heidi Koester who we have pestered on a weekly basis about this stuff 
- The clients who we cant have done this without. 


