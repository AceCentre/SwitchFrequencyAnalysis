#/bin/bash

curl -O http://ota.ox.ac.uk/text/2553.zip 
unzip 2553.zip
cd 2553/download/Texts
curl -O http://www.natcorp.ox.ac.uk/scripts/justTheWords.xsl
xsltproc justTheWords.xsl dem/*.xml -o bnc-baby.txt
mv bnc-baby.txt ../../../examples/
cd ../../../
python3 CleanText.py --text-file examples/bnc-baby.txt --save-file examples/bnc-baby-cleaned.txt
