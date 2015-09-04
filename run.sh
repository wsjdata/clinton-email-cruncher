#!/bin/bash
mkdir -p pdfs/
mkdir -p zips/
source virt-hrcemail/bin/activate
python downloadMetadata.py
python generatePDFList.py
if [ $1 = "no-pdf-download" ] 
then 
    echo "skipping PDF download"
else
    cd pdfs/
	wget --no-check-certificate --no-clobber --timeout=5 --tries=20 -i ../pdflist.txt
	cd ..
fi
python zipPDFs.py
python pdfTextToDatabase.py
deactivate
