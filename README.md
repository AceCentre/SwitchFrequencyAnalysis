# Switch Scanning Analysis
## Scripts and code to analyse switch scanning layouts for clients and their vocabulary

More text to follow soon

Whats in here:

1. VocabAnalysis.py Pass in a clients vocabulary (see examples/vocab.txt for the kind of format of this) and will output a lot of statistcs on this data. NB: choose the right scan steps - right now hardcoded in the top of the file. 
2. StepAnalysis.py. Read in a scan step csv and provide a test sentence (and if you wish a scan rate) and will give estimates for time to take to write this message.
3. TotalStepAnalysis.py. Read in a scan step csv and provide a vocab file (and if you wish a scan rate) and will give estimates for time to take to write the entire vocab.
4. scan-steps-lib/ a library of scan steps for different layouts. 
5. Mapper/ - a funky script that tries to show you what a frequency list would like in a grid you make. 


### To run

NB: Requires Python 3!

`pip install -r requirements.txt`

then run whichever. e.g:

`python VocabAnalysis.py --vocab-file path-to-file.txt`

`python StepAnalysis.py --ssteps path-to-step-scanning-lib-file.txt --scanrate 1`


### To-Do:

1. Provide some screenshots for each scan-steps-lib/ file
2. Clean up code to make more readable and usable (e.g. dont hardcode the scan steps in VocabAnalysis)
3. Right now code is designed to strip out non-Alpha characters. This is a bad idea if you want to analyse this in your code


### Thanks

- Massive thanks to Heidi Koester who we have pestered on a weekly basis about this stuff 
- The clients who we cant have done this without. 


