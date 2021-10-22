#!/usr/local/bin/python3
import re
import subprocess, os

### TO-D0
# Citation Parsing
# Appendix Parsing [four or five hash signs should denote an appendix and they should get custom page numbers in the class file with cover pages etc.]
# Create a conclusion item that gets automatically merged into the nonbreaking signature block environment.
# Parse question presented if present
# Be PDF/A compliant and add signatures for final filing

#os.chdir("/Users/brendanbernicker/Documents/GitHub/lawtex-1/Law_Typesetting_Program/")
os.chdir("L:\Github\lawtex-1\Law_Typesetting_Program/")

#Load Markdown File
file = open("Constitutional Litigation Brief.md", encoding="utf8")
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
    text = re.sub(r'\*{4}([^\n]+)\*{4}', r'\\textsc{\1}', text)
    text = re.sub(r'\*{2}([^\n]+)\*{2}', r'\\textbf{\1}', text)
    text = re.sub(r'\*([^\n\*]+)\*', r'\\textit{\1}', text)
    text = re.sub(r'\.\.\.', r'\\ldots ', text)
    return(text)

doc = list(map(Rich_Text_Formatting, doc))


# Replace Ordinals with Superscript
def Ordinal_Replace(text):
    text = re.sub(r'1st', r'1\\textsuperscript{st}', text)
    text = re.sub(r'2nd', r'2\\textsuperscript{nd}', text)
    text = re.sub(r'3rd', r'3\\textsuperscript{rd}', text)
    text = re.sub(r'4th', r'4\\textsuperscript{th}', text)
    text = re.sub(r'5th', r'5\\textsuperscript{th}', text)
    text = re.sub(r'6th', r'6\\textsuperscript{th}', text)
    text = re.sub(r'7th', r'7\\textsuperscript{th}', text)
    text = re.sub(r'8th', r'8\\textsuperscript{th}', text)
    text = re.sub(r'9th', r'9\\textsuperscript{th}', text)
    text = re.sub(r'0th', r'0\\textsuperscript{th}', text)
    return(text)

doc = list(map(Ordinal_Replace, doc))


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


# Citation Parser



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
with open('Base Latex Brief Which Python Adds To.tex','r', encoding = "utf8") as brief_base:
    brief_latex = brief_base.read()
    brief_base.close()


brief_latex = brief_latex.split('\n')
brief_latex = brief_latex + doc + ["\makeendmatter \n", "\end{document}"]

textfile = open("Brief to Compile.tex", "w", encoding = "utf8")
for element in brief_latex:
    textfile.write(element + "\n")
textfile.close()
