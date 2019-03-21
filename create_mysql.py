import pymysql

##############################
### params should be set #####
##############################
PASS_MySQL = "password"
NAME_DB = "test_db"
NAME_TABLE = "test_table"
##############################

conn = pymysql.connect(host="127.0.0.1", unix_socket="/tmp/mysql.sock", user="root", passwd=PASS_MySQL, db="mysql")

cur = conn.cursor()
comm_create_db = "CREATE DATABASE "
comm_create_db += NAME_DB
cur.execute(comm_create_db)
comm_use = "USE " + NAME_DB
cur.execute(comm_use)
comm_create_tb = "CREATE TABLE "
comm_create_tb += NAME_DB
comm_create_tb += "."
comm_create_tb += NAME_TABLE
comm_create_tb += " ( \
	date_horse CHAR(30) NOT NULL PRIMARY KEY, \
	place CHAR(5), \
	R CHAR(5), \
	sex CHAR(5), \
	age CHAR(5), \
	basis_weight CHAR(5), \
	weight CHAR(5), \
	weight_diff CHAR(5), \
	jockey CHAR(20), \
	fin_odr CHAR(5), \
	frame CHAR(5), \
	horse_num CHAR(5), \
	popu CHAR(5), \
	odds CHAR(10), \
	rst_odds_s CHAR(10), \
	rst_odds_m1 CHAR(10), \
	rst_odds_m2 CHAR(10), \
	rst_odds_m3 CHAR(10), \
	time CHAR(20), \
	diff CHAR(10), \
	posi CHAR(20), \
	time_3F CHAR(10), \
	field CHAR(5), \
	length CHAR(10), \
	field_cdt CHAR(10), \
	direction CHAR(5), \
	weather CHAR(10), \
	race_class CHAR(20), \
	cdt_rank CHAR(10), \
	speed CHAR(10), \
	late CHAR(10), \
	train_score CHAR(5) \
	)"
cur.execute(comm_create_tb)
conn.commit()

print("Done!!")

