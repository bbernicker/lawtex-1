#!/usr/local/bin/python3
#### Python Script for Legal Typesetting Program ####
##   Brendan Bernicker    ##

# Define Workspace
import os
import subprocess
import re
import pdftotext

#os.chdir("/Users/brendanbernicker/Documents/GitHub/lawtex-1/Law_Typesetting_Program")
os.chdir("L:\Github\lawtex-1\Law_Typesetting_Program/")

## Collect Information (UI: case details, brief type (for rules check), filing?)


# Call Parse Markdown into LaTeX Here









# Compile Using PDFLaTeX (remember to require two passes)
subprocess.check_call(['xelatex', 'Brief to Compile.tex'])
subprocess.check_call(['xelatex', 'Brief to Compile.tex'])

## [filing] Count Words for Certificate of Compliance {return message if cap is exceeded}

pdf_path = "Brief to Compile.pdf"

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

def LawTex_WordCounter(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    with open('output.txt', 'w') as f:
        f.write("\n\n".join(pdf))
    with open('output.txt', 'r') as text_file:
        brieftext = text_file.read()
    brieftext = brieftext.lower()
    index=brieftext.find("conclusion") #should probably be changed to respectfully submitted
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
    briefwords = slicer(brieftext, count_start_key)
    briefwords = re.findall(r'[^-\s]+', briefwords, re.MULTILINE)
    wordcount = len(briefwords)
    return(wordcount)

str(LawTex_WordCounter(pdf_path))

# Read in LaTeX file to add word count
with open('Brief to Compile.tex', 'r') as file :
  filedata = file.read()
  file.close()

filedata = filedata.replace(str(LawTex_WordCounter(pdf_path)), 'PYTHON WILL INPUT THE WORD COUNT HERE')

# Overwrite LaTeX file with added word count
with open('Brief to Compile.tex', 'w') as file:
  file.write(filedata)
  file.close()

## RECOMPILE FINAL PDF
subprocess.check_call(['pdflatex', 'Brief to Compile.tex'])
subprocess.check_call(['pdflatex', 'Brief to Compile.tex'])




#### NOTES ####

# Citation engine: When user types \cite{X}, the program checks whether X is defined. If not, it opens a dialog box where the user can either choose from the defined citations or define a new citation
# If the short form or long form citation appears in the proceeding sentence, add the [n] flag to do reporter/page/year only citation.
# It looks like the current citation engine supresses spaces before punctuation, but that includes ( when it should not.
# Redo statute engine to save full name of statute source as topline, abbreviation as short form, and use both in ToA (and only break where there is more than one reference to a source)
