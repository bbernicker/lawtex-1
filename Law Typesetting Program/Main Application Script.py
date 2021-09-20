#### Python Script for Legal Typesetting Program ####
##   Brendan Bernicker    ##

# Define Workspace
import os
import subprocess
#import PyPDF2
import pdftotext
import re

os.chdir("/Users/brendanbernicker/Documents/GitHub/lawtex-1/Law Typesetting Program")

## Collect Information (UI: case details, brief type (for rules check), filing?)


## Create .tex file using case information and RTF2LateX

## Compile Using PDFLaTeX (remember to require two passes)
#subprocess.check_call(['pdflatex', 'Test_FRAP_Brief.tex'])
#subprocess.check_call(['pdflatex', 'Test_FRAP_Brief.tex'])

## [filing] Count Words for Certificate of Compliance {return message if cap is exceeded}

with open("Test_FRAP_Brief.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

with open('output.txt', 'w') as f:
    f.write("\n\n".join(pdf))

with open('output.txt', 'r') as text_file:
    brieftext = text_file.read()

brieftext = brieftext.lower()

index=brieftext.find("conclusion")
brieftext = brieftext[index:]

brieftext = brieftext.replace("s tatement of j urisdiction", "statement of jurisdiction")
brieftext = brieftext.replace("j urisdictional s tatement", "jurisdictional statement")
brieftext = brieftext.replace("s tatement of the i ssues", "statement of the issues")
brieftext = brieftext.replace("s tatement of the c ase", "statement of the case")
brieftext = brieftext.replace("s tatement of j urisdiction", "statement of jurisdiction")
brieftext = brieftext.replace("s ummary", "summary")
brieftext = brieftext.replace("a rgument", "argument")

if brieftext.find("statement of jurisdiction") !=-1 :
    count_start_key = "statement of jurisdiction"
elif brieftext.find("jurisdictional statement") !=-1 :
    count_start_key = "jurisdictional statement"
elif brieftext.find("statement of the issues") !=-1 :
    count_start_key = "statement of the issues"
elif brieftext.find("statement of the case") !=-1 :
    count_start_key = "statement of the case"
elif brieftext.find("summary of the argument") !=-1 :
    count_start_key = "summary of the argument"
else:
    raise Exception('No Phrase Detected to Start Word Count')

def slicer(my_str,sub):
    index=my_str.find(sub)
    if index !=-1 :
        remainder = my_str[index:]
    else :
        raise Exception('No Phrase Triggered Word Count')
    end = remainder.find("respectfully submitted")
    if end !=-1 :
        remainder = remainder[:end]
    else :
        raise Exception('No Phrase Terminated Word Count')
    return remainder

briefwords = slicer(brieftext, count_start_key)


briefwords = re.findall(r"[^\s|—_]+", briefwords, re.MULTILINE)
wordcount = (len(briefwords)) ## Figure Out How to Get this Back into LaTeX


## [filing] Create Certificate of Compliance


## [filing] Collect Information on Service

## [filing] Generate Certificate of Service

## [filing] Append Certificates of Compliance and Service

## Open PDF in default program
#path = 'Test_FRAP_Brief.pdf'
#subprocess.Popen([path], shell=True)



#### NOTES ####

# Citation engine: When user types \cite{X}, the program checks whether X is defined. If not, it opens a dialog box where the user can either choose from the defined citations or define a new citation
