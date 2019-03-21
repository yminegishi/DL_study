# DL_study
The project to study deep learning for analysis of horse races 

## Required
-pymysql<br>-BeautifulSoup(bs4)

The data was scraped from "netkeiba.com". If you want to use all data, you must register this site.

## Tutorial
1) create database and table
Use "create_mysql.py", but you must set name of database and table, and password for mysql.
After setting, run "create_mysql.py".

python create_mysql.py

2) insert data into table 
Use "run_create_db.py", but you must set ID and password of "netkeiba.com"(If you have), and password of MySQL.
If you want data for other years, you must change "year" to other year.
After setting, run "run_create_db.py"

python run_create_db.py

3) checkout a branch you'd like to try on

git checkout v1_0_with_chainer

4) run Neural Network
read_dataset.py : read input values from database
<br>networks.py : models of Neural Network

python keiba_AI_v1_0.py [password_of_MySQL]


