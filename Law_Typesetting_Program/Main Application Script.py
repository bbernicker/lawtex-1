#!/usr/local/bin/python3
#### Python Script for Legal Typesetting Program ####
##   Brendan Bernicker    ##

# Define Workspace
import os
import subprocess
import re
import PyPDF2

#os.chdir("/Users/brendanbernicker/Documents/GitHub/lawtex-1/Law Typesetting Program")
os.chdir("L:\Github\lawtex-1\Law Typesetting Program/")

## Collect Information (UI: case details, brief type (for rules check), filing?)


## Create .tex file using case information and RTF2LateX
#Load Markdown File
file = open("Markdown Example.md")
file = file.read()
lines = file.split('\n')

# Remove Empty Lines
lines = [x for x in lines if x]

# Create Empty Lists to Store Text and Type for Each Line
doc = list(range(len(lines)))
type = list(range(len(lines)))

# MARKDOWN TO LATEX GENERAL
# Check whether each line is a heading and, if so, what level
def Ouline_Level_Parsing(i):
    try:
        doc[i] = re.search('^[^#]*$', lines[i]).group(0)
        type[i] = "body"
    except:
        if re.search('^# (.*)$', lines[i]):
            doc[i] = re.search('^# (.*)$', lines[i]).group(1)
            type[i] = "section"
        elif re.search('^## (.*)$', lines[i]):
            doc[i] = re.search('^## (.*)$', lines[i]).group(1)
            type[i] = "subsection"
        elif re.search('^### (.*)$', lines[i]):
            doc[i] = re.search('^### (.*)$', lines[i]).group(1)
            type[i] = "subsubsection"
        else:
            doc[i] = "ERROR: YOU CANNOT HAVE MORE THAN THREE LEVELS OF HEADINGS"
            type[i] = "ERROR"

for i in range(len(lines)):
    Ouline_Level_Parsing(i)

# Convert Italics and Bold from Markdown to LaTeX
def Rich_Text_Formatting(text):
    text = re.sub(r'\*{2}([^\n]+)\*{2}', r'\\textbf{\1}', text)
    text = re.sub(r'\*([^\n\*]+)\*', r'\\textit{\1}', text)
    return(text)

doc = list(map(Rich_Text_Formatting, doc))

# MARKDOWN TO LATEX FOOTNOTES
# Extract Footnotes and their Corresponding Labels
note_label = ["$$Labs"]
note_text = ["$$NoteText"]

for i in range(len(doc)):
    if re.search(r'^\[\^([^:\]]+)\]: (.+)$', doc[i]):
        note_label.append(re.search(r'^\[\^([^:\]]+)\]: (.+)$', doc[i]).group(1))
        note_text.append(re.search(r'^\[\^([^:\]]+)\]: (.+)$', doc[i]).group(2))
        type[i] = "footnote"
    else:
        continue

del note_label[0]
del note_text[0]

# Change Footnotes to LaTeX format and put labels in format that allows search and replace
note_label = ["[^" + s + "]" for s in note_label]
note_text = ["\\footnote{" + s + "}" for s in note_text]


# Remove Footnote Lines so that they are not mistaken for labels (and remove them from type file as well)
note_removal = []
for i in range(len(doc)):
    if type[i] == "footnote":
        note_removal.append(i)

doc = [v for i,v in enumerate(doc) if i not in note_removal]
type = [v for i,v in enumerate(type) if i not in note_removal]


# Search for Note Labels and Replace with LaTeX symbol and text
for note_num in range(len(note_label)):
    doc = [line.replace(str(note_label[note_num]), str(note_text[note_num])) for line in doc]

# Add Latex Syntax for Each Type of Line
for i in range(len(doc)):
    if type[i] == "section":
        doc[i] = "\\section{" + doc[i] + "}"
    elif type[i] == "subsection":
        doc[i] = "\\subsection{" + doc[i] + "}"
    elif type[i] == "subsubsection":
        doc[i] = "\\subsubsection{" + doc[i] + "}"
    else:
        continue

# Make Each Python Paragraph or Heading end with Newline for LaTeX
doc = [s + "\n" for s in doc]

# CREATE ACTUAL LATEX FILE

# Load Base File (later automate front page generation and citations)
with open('Base Latex Brief Which Python Adds To.tex','r') as brief_base:
    brief_latex = brief_base.read()
    brief_base.close()


brief_latex = brief_latex.split('\n')
brief_latex = brief_latex + doc + ["\makeendmatter \n", "\end{document}"]

textfile = open('Brief to Compile.tex', 'w')
for element in brief_latex:
    textfile.write(element + "\n")
textfile.close()

# Compile Using PDFLaTeX (remember to require two passes)
subprocess.check_call(['pdflatex', 'Brief to Compile.tex'])
subprocess.check_call(['pdflatex', 'Brief to Compile.tex'])

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
        pdf = PyPDF2.PdfFileReader(f)
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

## Open PDF in default program
subprocess.Popen([pdf_path], shell=True)



#### NOTES ####

# Citation engine: When user types \cite{X}, the program checks whether X is defined. If not, it opens a dialog box where the user can either choose from the defined citations or define a new citation
