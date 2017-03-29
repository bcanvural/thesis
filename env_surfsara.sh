#!/usr/bin/bash

export SPARK_HOME=/home/bcvural/spark-2.1.0-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON=python3
alias rr="spark-submit --master yarn --deploy-mode cluster spark.py"
