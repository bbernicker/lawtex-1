



%% Load the required packages
\@ifundefined{SuppressClass}{%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{FRAP_Brief}
\LoadClassWithOptions{article}
}{}%

\PassOptionsToClass{casesupra}{bluebook}
\RequirePackage{bluebook}
\RequirePackage[margin=1in]{geometry}
\RequirePackage[T1]{fontenc}
\RequirePackage[pdftex]{graphicx}
\RequirePackage{indentfirst}
\RequirePackage{newcent, microtype}
\RequirePackage{array}
\RequirePackage{setspace,xcolor}
\RequirePackage[hyperindex=false,linkbordercolor=white,pdfborder={0 0 0}]{hyperref}
\RequirePackage{trace}



%% Retain symbols for & and @
\makeandletter
\makeatletter



%% Make a table of authorities with Case, Statute, and Other categories
\newcommand{\@RunMakeIndex}{%
	\clearpage%
	\immediate\closeout\Case@idxfile%
	\immediate\closeout\Statute@idxfile%
	\immediate\closeout\Other@idxfile%
	\immediate\write18{makeindex -r -s lawcitations.ist Case}%
	\immediate\write18{makeindex -L -r -s lawcitations.ist Statute}%
	\immediate\write18{makeindex -r -s lawcitations.ist Other}%
}
\AtEndDocument{%
	\@RunMakeIndex%
}





