#!/usr/bin/zsh

export PATH=$PATH:/home/baris/Developer/thesis/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias rr1="spark-submit tfidf.py"
alias rr2="spark-submit word2vec.py"
