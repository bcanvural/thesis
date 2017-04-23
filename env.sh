#!/usr/bin/zsh

export PATH=$PATH:/home/baris/Developer/thesis/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias ccall="rm -rf Calculated"
alias rr1="spark-submit tfidf.py"
alias cc1="rm -rf Calculated/tfidf"
alias rr2="spark-submit countvectorizer.py"
alias cc2="rm -rf Calculated/countvectorizer/"
alias rr3="spark-submit word2vec.py"
alias cc3="rm -rf Calculated/word2vec"
alias rr4="spark-submit word2vec2.py"
alias cc4="rm -rf Calculated/word2vec2"
alias rr5="spark-submit count-pca.py"
alias cc5="rm -rf Calculated/count-pca"
alias rrall="rr1 && rr2 && rr3 && rr4 && rr5"
