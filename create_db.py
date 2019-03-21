# coding:utf-8
import sys
import requests
from bs4 import BeautifulSoup
import re
import pymysql
import urllib

args = sys.argv

### for login #################################### 
race_url = args[1]
ID_NETKEIBA = args[2]
PASS_NETKEIBA = args[3]
login_url = "https://regist.netkeiba.com/account/"
params = { \
	'pid': 'login', \
	'action': 'auth', \
	'login_id': ID_NETKEIBA, \
	'pswd': PASS_NETKEIBA \
}
url = "http://db.netkeiba.com"
##################################################


session = requests.Session()

try:
	s = session.post(login_url, data=params)
except urllib.error.HTTPError:
	print("HTTP Error:", sys.exc_info()[0])
	raise

s.cookies.get_dict()
#print(s.cookies.get_dict())
#print("-----------")


try:
	s = session.get(race_url)
except urllib.error.HTTPError as e:
	print(e)
except urllib.error.URLError as e:
	print("The server could not be found")
else:
	pass


s.encoding = s.apparent_encoding
#print(s.text)
soup = BeautifulSoup(s.content, "html.parser")
#print(soup)

title=soup.title.string
title=title.split(" / ")
#print(title)
date_temp = title[0].split("｜")
date = date_temp[1][0:4]+date_temp[1][5:7]+date_temp[1][8:10]

grade = "0"
h1 = soup.find_all("h1")
if( len(h1[1].contents[0].split("(G")) > 1):
	grade = h1[1].contents[0].split("(G")[1][0]

race_tmp = soup.find("p", class_="smalltxt").contents[0]
place = race_tmp.split("回")[1][0:2]
Race = soup.find("div", class_="race_num fc").find("a", class_="active").contents[0]
race_class = ""
if len(race_tmp.split("サラ系")) >1:
	race_class = race_tmp.split("サラ系")[1].split("\xa0")[0]
if len(race_tmp.split("障害")) >1:
	race_class = race_tmp.split("障害")[1].split("\xa0")[0]


if (grade=="1"):
	race_class += "(GI)"
if (grade=="2"):
	race_class += "(G2)"
if (grade=="3"):
	race_class += "(G3)"

print(date, place, Race, race_class)


total_number = 0
cancel_number = 0
list_data_horse = []
list_sex = []
list_age = []
list_basis_weight = []
list_weight = []
list_weight_diff = []
list_jockey = []
list_fin_odr = []
list_frame = []
list_horse_num = []
list_popu = []
list_odds = []
list_time = []
list_diff = []
list_speed = []
list_posi = []
list_time_3F = []
list_late = []
list_url = []
list_train_score = []

list_diff_time3F = []
min_3F = [999., 999., 999.]
id_min_3F = [-1, -1, -1]

racedata_fc = soup.find_all("dl", class_="racedata fc")
temp = racedata_fc[0].span.contents[0].split("/")
field = temp[0][0]
length = temp[0][-6:-2]
weather = temp[1].split(":")[1][1:-1]
field_cdt = ""
if len(temp[2].split(":")[1])<=5:
	field_cdt = temp[2].split(":")[1][1:-1]
else:
	field_cdt = temp[2].split(":")[1].split("ダ")[0][1:-1]
direction = ""
if (place=="東京" or place=="中京" or place=="新潟"):
	direction = "左"
else:
	direction = "右"
print(field, length, weather, field_cdt, direction)


dl=soup.find_all("dl", class_="pay_block") 
for pay in dl:
	tr_pay=pay.find_all("tr")
td_r_pay_0 = tr_pay[0].find_all("td", class_="txt_r")
td_r_pay_1 = tr_pay[1].find_all("td", class_="txt_r")
rst_odds_s  = 0.
rst_odds_m1 = 0.
rst_odds_m2 = 0.
rst_odds_m3 = 0.
if len(td_r_pay_0[0].contents) > 0:
	rst_odds_s  = td_r_pay_0[0].contents[0]
	if(len(rst_odds_s.split(","))>1):
		rst_odds_s = rst_odds_s.split(",")[0] + rst_odds_s.split(",")[1]
	rst_odds_s = float(rst_odds_s)/100.
if len(td_r_pay_1[0].contents) > 0:
	rst_odds_m1  = td_r_pay_1[0].contents[0]
	if(len(rst_odds_m1.split(","))>1):
		rst_odds_m1 = rst_odds_m1.split(",")[0] + rst_odds_m1.split(",")[1]
	rst_odds_m1 = float(rst_odds_m1)/100.
if len(td_r_pay_1[0].contents) > 2:
	rst_odds_m2  = td_r_pay_1[0].contents[2]
	if(len(rst_odds_m2.split(","))>1):
		rst_odds_m2 = rst_odds_m2.split(",")[0] + rst_odds_m2.split(",")[1]
	rst_odds_m2 = float(rst_odds_m2)/100.
if len(td_r_pay_1[0].contents) > 4:
	rst_odds_m3  = td_r_pay_1[0].contents[4]
	if(len(rst_odds_m3.split(","))>1):
		rst_odds_m3 = rst_odds_m3.split(",")[0] + rst_odds_m3.split(",")[1]
	rst_odds_m3 = float(rst_odds_m3)/100.


tr=soup.find_all("tr")

for i in range(1, len(tr)):
	if tr[i].find("a")!=None:
		total_number = i
	else:
		break

cdt_rank = ""
flag = False
for i in range(total_number+1, len(tr)):
	if flag == True:
		break
	else:
		th = tr[i].find_all("th")
		for t in th:
			if t.contents[0][:4] == "馬場指数":
				flag = True
		if flag==True:
			cdt_rank = tr[i].find("td").contents[0].split("\xa0")[0]


win_time = 1000

for i in range(1, total_number+1):	
	name = tr[i].find("a").contents[0]
	list_data_horse.append(date+"_"+name)
	td_c = tr[i].find_all("td", class_="txt_c", nowrap="nowrap")
	list_sex.append(td_c[0].contents[0][0])	
	list_age.append(td_c[0].contents[0][1])	
	list_basis_weight.append(td_c[1].contents[0])
	
	if td_c[3].span.string!=None:
		list_time_3F.append(td_c[3].span.contents[0])	
		td = tr[i].find_all("td", class_="", nowrap="nowrap")
		if (place=="新潟" and length=="1000"):
			list_posi.append(None)
		else:
			posi_temp = td[0].contents[0]
			posi = posi_temp.split("-")[1]
			posi_ratio = round(float(posi)/float(total_number), 1)
			if ( (posi==1) or (posi_ratio<0.15) ):
				list_posi.append(str(posi)+"/"+str(total_number)+" (逃)")
			elif ( posi_ratio<0.45 ):
				list_posi.append(str(posi)+"/"+str(total_number)+" (先)")
			elif ( posi_ratio<0.8 ):
				list_posi.append(str(posi)+"/"+str(total_number)+" (差)")
			elif ( posi_ratio<=1.0 ):
				list_posi.append(str(posi)+"/"+str(total_number)+" (追)")
		list_weight.append(td[1].contents[0][0:3])
		list_url.append( url + td_c[4].find("a").attrs["href"] )
		if td[2].contents[0] == "\n":
			list_late.append("")
		else:
			list_late.append("遅")
		list_weight_diff.append(td[1].contents[0][4:-1])
		td_l = tr[i].find_all("td", class_="txt_l", nowrap="nowrap")
		list_jockey.append(td_l[1].find("a").contents[0])
		td_r = tr[i].find_all("td", class_="txt_r", nowrap="nowrap")
		list_fin_odr.append(td_r[0].contents[0])
		list_horse_num.append(td_r[1].contents[0])
		tr_speed = ""
		if len( tr[i].find_all("td", class_=re.compile("^(speed_index)"), nowrap="nowrap")[0].contents[0].split() ) >0:
			tr_speed = tr[i].find_all("td", class_=re.compile("^(speed_index)"), nowrap="nowrap")[0].contents[0].split()[0]
		else:
			tr_speed = 0
		list_speed.append(tr_speed)

		minute = float(td_r[2].contents[0][0])*60.
		sec    = float(td_r[2].contents[0][2:4])
		msec   = float(td_r[2].contents[0][5])*0.1
		time   = round(minute+sec+msec, 1)
		list_time.append(str(time))
		if time < win_time:
			win_time = time
		if i==1:
			list_diff.append(str(round(win_time-time, 1)))
		else:
			list_diff.append(str(round(time-win_time, 1)))
		list_odds.append(td_r[3].contents[0])
		td_align = tr[i].find_all("td", align="right", nowrap="nowrap")
		list_popu.append(td_align[1].span.contents[0]) 
		td_ml = tr[i].find_all("td", class_=re.compile("w.ml"), nowrap="nowrap")
		list_frame.append(td_ml[0].span.contents[0])

		if (float(list_time_3F[i-1])<min_3F[0]):
			min_3F[2] = min_3F[1]
			id_min_3F[2] = id_min_3F[1]
			min_3F[1] = min_3F[0]
			id_min_3F[1] = id_min_3F[0]
			min_3F[0] = float(list_time_3F[i-1])
			id_min_3F[0] = i - 1
		elif (float(list_time_3F[i-1])<min_3F[1]):
			min_3F[2] = min_3F[1]
			id_min_3F[2] = id_min_3F[1]
			min_3F[1] = float(list_time_3F[i-1])
			id_min_3F[1] = i - 1
		elif (float(list_time_3F[i-1])<min_3F[2]):
			min_3F[2] = float(list_time_3F[i-1])
			id_min_3F[2] = i - 1


	else:
		td = tr[i].find_all("td", class_="", nowrap="nowrap")
		list_time_3F.append(None)	
		list_posi.append(None)
		list_weight.append(td[1].contents[0][0:3])
		list_weight_diff.append(td[1].contents[0][4:-1])
		td_l = tr[i].find_all("td", class_="txt_l", nowrap="nowrap")
		list_jockey.append(td_l[1].find("a").contents[0])
		td_r = tr[i].find_all("td", class_="txt_r", nowrap="nowrap")
		list_fin_odr.append("消")
		list_horse_num.append(td_r[1].contents[0])
		list_time.append(None)
		list_diff.append(None)
		list_speed.append(None)
		list_odds.append(td_r[3].contents[0])
		list_popu.append(None) 
		td_ml = tr[i].find_all("td", class_=re.compile("w.ml"), nowrap="nowrap")
		list_frame.append(td_ml[0].span.contents[0])
		cancel_number+=1



### for appending training score ######################
for u in list_url:
	try:
		s2 = session.get(u)
	except HTTPError as e:
		print(e)
	except URLError as e:
		print("The server could not be found")
	else:
		pass

	s2.encoding = s2.apparent_encoding
	soup2 = BeautifulSoup(s2.content, "html.parser")

	tr2 = soup2.find_all("tr")
	td2 = tr2[1].find_all("td")
	list_train_score.append(td2[len(td2)-2].contents[0])
########################################################



##########################
### setting SQL params ###
##########################
PASS_MySQL = args[4]
NAME_DB = args[5]
NAME_TABLE = args[6]
##########################

conn = pymysql.connect(host="127.0.0.1", unix_socket="/tmp/mysql.sock", user="root", passwd=PASS_MySQL, db="mysql")

cur = conn.cursor()
comm_use = "USE " + NAME_DB
cur.execute(comm_use)
for i in range(0, len(list_data_horse)):
	if i < (len(list_data_horse) - cancel_number):
		##### for delete of data ##########################################################
		comm_del = "DELETE FROM " + NAME_TABLE + " WHERE date_horse = %s"
		cur.execute(comm_del, list_data_horse[i])
		################################################################################
		comm_ins = "INSERT INTO " + NAME_TABLE
		comm_ins += " (date_horse, place, R, sex, age, \
			basis_weight, weight, weight_diff, jockey, \
			fin_odr, frame, horse_num, popu, odds, \
			rst_odds_s, rst_odds_m1, rst_odds_m2, rst_odds_m3, \
			time, diff, posi, time_3F, \
			field, length, field_cdt, direction, weather, \
			race_class, cdt_rank, speed, late, train_score) \
			VALUES \
			(%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, \
			%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, \
			%s, %s, %s, %s, \
			%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, %s)"
		cur.execute(comm_ins, \
			(list_data_horse[i], place, Race, list_sex[i], list_age[i], \
			list_basis_weight[i], list_weight[i], list_weight_diff[i], list_jockey[i], \
			list_fin_odr[i], list_frame[i], list_horse_num[i], list_popu[i], list_odds[i], \
			rst_odds_s, rst_odds_m1, rst_odds_m2, rst_odds_m3, \
			list_time[i], list_diff[i], list_posi[i], list_time_3F[i], \
			field, length, field_cdt, direction, weather, \
			race_class, cdt_rank, list_speed[i], list_late[i], list_train_score[i]) \
		)
	else:
		##### for delete of data ##########################################################
		comm_del = "DELETE FROM " + NAME_TABLE + " WHERE date_horse = %s"
		cur.execute(comm_del, list_data_horse[i])
		################################################################################
		comm_ins = "INSERT INTO " + NAME_TABLE
		comm_ins += " (date_horse, place, R, sex, age, \
			basis_weight, weight, weight_diff, jockey, \
			fin_odr, frame, horse_num, popu, odds, \
			rst_odds_s, rst_odds_m1, rst_odds_m2, rst_odds_m3, \
			field, length, field_cdt, direction, weather, \
			race_class, cdt_rank) \
			VALUES \
			(%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, \
			%s, %s, %s, %s, %s, \
			%s, %s, %s, %s, \
			%s, %s, %s, %s, %s, \
			%s, %s)"
		cur.execute(comm_ins, \
			(list_data_horse[i], place, Race, list_sex[i], list_age[i], \
			list_basis_weight[i], list_weight[i], list_weight_diff[i], list_jockey[i], \
			list_fin_odr[i], list_frame[i], list_horse_num[i], list_popu[i], list_odds[i], \
			rst_odds_s, rst_odds_m1, rst_odds_m2, rst_odds_m3, \
			field, length, field_cdt, direction, weather, \
			race_class, cdt_rank) \
		)
conn.commit()

cur.close()
conn.close()

