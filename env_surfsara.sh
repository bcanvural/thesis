#!/usr/bin/bash

export PATH=$PATH:/home/bcvural/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
alias rr="spark-submit --master yarn --deploy-mode-cluster spark.py"
