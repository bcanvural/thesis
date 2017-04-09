#!/usr/bin/zsh

export PATH=$PATH:/home/baris/Developer/thesis/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias rr1="spark-submit tfidf.py"
alias cc1="rm -rf cosine-calculated category-cosine-calculated"
alias rr2="spark-submit tfidf2.py"
alias cc2="rm -rf cosine-calculated-tfidf2 category-cosine-calculated-tfidf2"
alias rr3="spark-submit countvectorizer.py"
alias cc3="rm -rf cosine-calculated-countvectorizer category-cosine-calculated-countvectorizer"
alias rr4="spark-submit word2vec.py"
alias cc4="rm -rf word2vec-calculated category-word2vec-calculated"
