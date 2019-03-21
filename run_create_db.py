import subprocess
from time import sleep

##########################################
ID_NETKEIBA = "e-mail_address"
PASS_NETKEIBA = "password"
PASS_MySQL = "password"
NAME_DB = "test_db"
NAME_TABLE = "test_table"
year="2018"
##########################################

args_list = [ \
	ID_NETKEIBA, \
	PASS_NETKEIBA, \
	PASS_MySQL, \
	NAME_DB, \
	NAME_TABLE \
]

place = []
place.append("sapporo")
place.append("hakodate")
place.append("fukushima")
place.append("nigata")
place.append("tokyo")
place.append("nakayama")
place.append("chukyo")
place.append("kyoto")
place.append("hanshin")
place.append("kokura")

url_sapporo   = "http://db.netkeiba.com/race/" +year +"010"
url_sapporo_n = [6, 6]
url_hakodate  = "http://db.netkeiba.com/race/" +year +"020"
url_hakodate_n = [6, 6]
url_fukushima = "http://db.netkeiba.com/race/" +year +"030"
url_fukushima_n = [6, 8, 6]
url_nigata    = "http://db.netkeiba.com/race/" +year +"040"
url_nigata_n = [8, 12, 6]
url_tokyo     = "http://db.netkeiba.com/race/" +year +"050"
url_tokyo_n = [8, 12, 8, 9, 8]
url_nakayama  = "http://db.netkeiba.com/race/" +year +"060"
url_nakayama_n = [7, 8, 8, 9, 9]
url_chukyo    = "http://db.netkeiba.com/race/" +year +"070"
url_chukyo_n = [6, 6, 8, 6]
url_kyoto     = "http://db.netkeiba.com/race/" +year +"080"
url_kyoto_n = [7, 8, 12, 9, 8]
url_hanshin   = "http://db.netkeiba.com/race/" +year +"090"
url_hanshin_n = [8, 8, 8, 9, 9]
url_kokura    = "http://db.netkeiba.com/race/" +year +"100"
url_kokura_n = [8, 12]

list_url = []
list_url.append(url_sapporo)
list_url.append(url_hakodate)
list_url.append(url_fukushima)
list_url.append(url_nigata)
list_url.append(url_tokyo)
list_url.append(url_nakayama)
list_url.append(url_chukyo)
list_url.append(url_kyoto)
list_url.append(url_hanshin)
list_url.append(url_kokura)
list_url_n = []
list_url_n.append(url_sapporo_n)
list_url_n.append(url_hakodate_n)
list_url_n.append(url_fukushima_n)
list_url_n.append(url_nigata_n)
list_url_n.append(url_tokyo_n)
list_url_n.append(url_nakayama_n)
list_url_n.append(url_chukyo_n)
list_url_n.append(url_kyoto_n)
list_url_n.append(url_hanshin_n)
list_url_n.append(url_kokura_n)


##### for TEST ######################################
#url=["http://db.netkeiba.com/race/201801010403/"]
#####################################################
url=[]
for i in range(0, len(list_url)):
	for j in range(1, len(list_url_n[i])+1):
		url_tmp0 = list_url[i] + str(j)
		for k in range(1, list_url_n[i][j-1]+1 ):
			if k<10:
				url_tmp1 = url_tmp0 +"0" +str(k)
			else:
				url_tmp1 = url_tmp0 +str(k)
			for l in range(1, 13):
				if l<10:
					url_tmp2 = url_tmp1 +"0" +str(l) +"/"
				else:
					url_tmp2 = url_tmp1 +str(l) +"/"
				url.append(url_tmp2)


for i in range(0, len(url)):
	cmd = ["python3", "create_db.py"]
	cmd.append(url[i])
	for arg in args_list:
		cmd.append(arg)
	sleep(0.1)
	subprocess.run(cmd)
