#!/usr/bin/zsh
#Environment setup

export SPARK_HOME=/home/baris/Developer/spark-2.1.0-bin-hadoop2.7 #change this
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON=python3

alias ccall="rm -rf Calculated"

alias cc1="rm -rf Calculated/tfidf"
alias rr1="cc1 && spark-submit tfidf.py"

alias cc2="rm -rf Calculated/countvectorizer/"
alias rr2="cc2 && spark-submit countvectorizer.py"

alias cc3="rm -rf Calculated/word2vec"
alias rr3="cc3 && spark-submit word2vec.py"

alias cc4="rm -rf Calculated/word2vec2"
alias rr4="cc4 && spark-submit word2vec2.py"

alias cc5="rm -rf Calculated/count-pca"
alias rr5="cc5 && spark-submit count-pca.py"

alias rrall="rr1 && rr2 && rr3 && rr4 && rr5"
