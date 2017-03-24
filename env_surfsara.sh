#!/usr/bin/bash

export PATH=$PATH:/home/bcvural/spark-2.1.0-bin-hadoop2.7/bin
export PYSPARK_PYTHON=python3
export RUN_COMMAND="spark-submit --master yarn --deploy-mode-cluster spark.py"
alias rr="echo $RUN_COMMAND && $($RUN_COMMAND)"
