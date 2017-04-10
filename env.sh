#!/usr/bin/zsh

export PATH=$PATH:/home/baris/Developer/thesis/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias ccall="rm -rf Calculated"
alias rr1="spark-submit tfidf.py"
alias cc1="rm -rf Calculated/tfidf Calculated/tfidf"
alias rr2="spark-submit tfidf2.py"
alias cc2="rm -rf Calculated/tfidf2 Calculated/tfidf2"
alias rr3="spark-submit countvectorizer.py"
alias cc3="rm -rf Calculated/countvectorizer/ Calculated/countvectorizer"
alias rr4="spark-submit word2vec.py"
alias cc4="rm -rf Calculated/word2vec Calculated/countvectorizer"
