# This file is to be used with Scott Mackenzies SPC calculator. 
# http://www.yorku.ca/mack/icchp2012.html 
# Code: http://www.yorku.ca/mack/ScanningKeyboardSPC.zip

# DB space
java ScanningKeyboardSPC db-wordfreq.txt -ckeatsroin-lhmpgdu.-wckybfvj-qxz_.... -kl -spc
# QWERTY
java ScanningKeyboardSPC db-wordfreq.txt -ckqwertyuiop-asdfghjkl.-zxcvbnm...-_......... -kl -spc
# FREQ - EARDU
java ScanningKeyboardSPC db-wordfreq.txt -ck_eardu-toilgv-nsfyx.-hcpkj.-mbwqz. -kl -spc
# AEIOU 
java ScanningKeyboardSPC db-wordfreq.txt -ckabcd_.-efgh..-ijklmn-opqrst-uvwxyz -kl -spc
# DB Freq
java ScanningKeyboardSPC db-wordfreq.txt -ck_eoilm-tasdck-nrugvq-hwpx..-fbj...-yz.... -kl -spc

# Now Compare with other corpus. 

# DB space
java ScanningKeyboardSPC d1-wordfreq.txt -ckeatsroin-lhmpgdu.-wckybfvj-qxz_.... -kl -spc
java ScanningKeyboardSPC d2-wordfreq.txt -ckeatsroin-lhmpgdu.-wckybfvj-qxz_.... -kl -spc
java ScanningKeyboardSPC bc-wordfreq.txt -ckeatsroin-lhmpgdu.-wckybfvj-qxz_.... -kl -spc
# QWERTY
java ScanningKeyboardSPC d1-wordfreq.txt -ckqwertyuiop-asdfghjkl.-zxcvbnm...-_......... -kl -spc
java ScanningKeyboardSPC d2-wordfreq.txt -ckqwertyuiop-asdfghjkl.-zxcvbnm...-_......... -kl -spc
java ScanningKeyboardSPC bc-wordfreq.txt -ckqwertyuiop-asdfghjkl.-zxcvbnm...-_......... -kl -spc
# FREQ - EARDU
java ScanningKeyboardSPC d1-wordfreq.txt -ck_eardu-toilgv-nsfyx.-hcpkj.-mbwqz. -kl -spc
java ScanningKeyboardSPC d2-wordfreq.txt -ck_eardu-toilgv-nsfyx.-hcpkj.-mbwqz. -kl -spc
java ScanningKeyboardSPC bc-wordfreq.txt -ck_eardu-toilgv-nsfyx.-hcpkj.-mbwqz. -kl -spc
# AEIOU 
java ScanningKeyboardSPC d1-wordfreq.txt -ckabcd_.-efgh..-ijklmn-opqrst-uvwxyz -kl -spc
java ScanningKeyboardSPC d2-wordfreq.txt -ckabcd_.-efgh..-ijklmn-opqrst-uvwxyz -kl -spc
java ScanningKeyboardSPC bc-wordfreq.txt -ckabcd_.-efgh..-ijklmn-opqrst-uvwxyz -kl -spc
# DB Freq
java ScanningKeyboardSPC d1-wordfreq.txt -ck_eoilm-tasdck-nrugvq-hwpx..-fbj...-yz.... -kl -spc
java ScanningKeyboardSPC d2-wordfreq.txt -ck_eoilm-tasdck-nrugvq-hwpx..-fbj...-yz.... -kl -spc
java ScanningKeyboardSPC bc-wordfreq.txt -ck_eoilm-tasdck-nrugvq-hwpx..-fbj...-yz.... -kl -spc

