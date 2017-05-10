# Thesis - Edison Competencies Evaluation and Term extraction

**Prerequisites**
  * Python3
  * Spark2.7
  * MongoDB
  * Check env.sh and change SPARK_HOME variable to where Spark is located
  * pip3 - python3 dependency manager (Install any missing python3 dependency using pip3)
  * Some python dependencies(not all needed all the time): scipy, numpy, pathlib, nltk(need to install wordnet in this), langdetect, flask, pymongo, flask_cors
  * Clone the repository and run:
 `source env.sh` for environment setup
  * Need mongodb running locally. `sudo service mongodb start`
  * To run server `python3 server.py` (Necessary for running the front-end app. This requires mongodb to be running)
  * Main spark jobs are listed in env.sh `rr1` runs the spark job with rr1 alias `rrall` runs them all (Check env.sh before running jobs)

**Notes**
  * Job ads are "jobs". Job ads go under jobs/ folder. Single job has single file in json. "description" field is where job ad text is located. Then run jobs4rdd.py script with `python3 jobs4rdd.py`
  * Folders under Categories/ are category names. .txt files listed under these category folders are called "skill" Add a particular skill by creating folders and files in the following format: Categories/\<new-category-name>/\<new-skill-name>.txt  Then run `python3 categories4rdd.py`
  * CVs are located under CVs/ Add a new CV under this folder as a single json file and run `python3 cvs4rdd.py`
  * *4rdd.py scripts prepares input for Spark to process
  * Spark job outputs go under Calculated/
  
