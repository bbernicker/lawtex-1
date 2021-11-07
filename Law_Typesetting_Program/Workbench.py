#!/usr/local/bin/python3
import re
import os
import subprocess as sp

def AddWordCount(text):
    pythonwordcount = str(LawTex_WordCounter("Brief_to_Compile.pdf"))
    text = re.sub(r'\\pythonwordcount{PYTHON WILL INPUT THE WORD COUNT HERE}', pythonwordcount, text)
    return(text)

brief_latex = list(map(AddWordCount, brief_latex))
