#!/usr/bin/zsh

export PATH=$PATH:/home/baris/Developer/thesis/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias rr="spark-submit --packages com.databricks:spark-csv_2.11:1.5.0 spark.py"
