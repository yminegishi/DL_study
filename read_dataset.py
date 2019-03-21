import pymysql
import numpy as np
from jockey_library import create_jocker_vector

################
################
AGE0="2歳"
AGE1="3歳"
AGE2="3歳以上"
AGE3="4歳以上"
################

class read_database():
	def __init__(self, var_name, age, pass_MySQL):
		self.nb_var = len(var_name)
		
		conn = pymysql.connect(host="127.0.0.1", unix_socket="/tmp/mysql.sock", user="root", passwd=pass_MySQL, db="mysql")
		cur = conn.cursor()
		cur.execute("USE keiba_db")
		
		cur.execute("SELECT field from race_tb_v2 where date_horse like \"%s\"" % age)
		self.field = cur.fetchall()
		
		cur.execute("SELECT length from race_tb_v2 where date_horse like \"%s\"" % age)
		self.length = cur.fetchall()
		
		cur.execute("SELECT race_class from race_tb_v2 where date_horse like \"%s\"" % age)
		self.race_class = cur.fetchall()
		
		cur.execute("SELECT date_horse from race_tb_v2 where date_horse like \"%s\"" % age)
		self.date_horse = cur.fetchall()
		
		cur.execute("SELECT place from race_tb_v2 where date_horse like \"%s\"" % age)
		self.place = cur.fetchall()
		
		cur.execute("SELECT R from race_tb_v2 where date_horse like \"%s\"" % age)
		self.R = cur.fetchall()
		
		cur.execute("SELECT horse_num from race_tb_v2 where date_horse like \"%s\"" % age)
		self.horse_num = cur.fetchall()
		
		cur.execute("SELECT fin_odr from race_tb_v2 where date_horse like \"%s\"" % age)
		self.fin_odr = cur.fetchall()
		
		cur.execute("SELECT rst_odds_m1 from race_tb_v2 where date_horse like \"%s\"" % age)
		self.rst_odds_m1 = cur.fetchall()
		cur.execute("SELECT rst_odds_m2 from race_tb_v2 where date_horse like \"%s\"" % age)
		self.rst_odds_m2 = cur.fetchall()
		cur.execute("SELECT rst_odds_m3 from race_tb_v2 where date_horse like \"%s\"" % age)
		self.rst_odds_m3 = cur.fetchall()
		
		self.optvar = []
		self.nb_optvar = 0
		for i in range(0, len(var_name)):
			if var_name[i] == "jockey":
				self.nb_optvar += 1
				cur.execute("SELECT jockey from race_tb_v2 where date_horse like \"%s\"" % age)
				jockey_tuple = cur.fetchall()
				jockey = []
				for var in jockey_tuple:
					if var[0] == None:
						jockey.append(None)
					else:
						j_vector_class = create_jocker_vector()
						jockey.append( j_vector_class.get_vector(var[0]) + 1 )
				self.optvar.append(jockey)

			elif var_name[i] == "frame":
				self.nb_optvar += 1
				cur.execute("SELECT frame from race_tb_v2 where date_horse like \"%s\"" % age)
				frame_tuple = cur.fetchall()
				frame = []
				for var in frame_tuple:
					if var[0] == None:
						frame.append(None)
					else:
						frame.append(int(var[0]))
				self.optvar.append(frame)
		
			elif var_name[i] == "train_score":
				self.nb_optvar += 1
				cur.execute("SELECT train_score from race_tb_v2 where date_horse like \"%s\"" % age)
				train_score_tuple = cur.fetchall()
				train_score = []
				for var in train_score_tuple:
					if var[0] == None:
						train_score.append(None)
					else:
						if var[0] == "A":
							train_score.append(1)
						elif var[0] == "B":
							train_score.append(2)
						elif var[0] == "C":
							train_score.append(3)
						else:
							train_score.append(4)
				self.optvar.append(train_score)
			
			elif var_name[i] == "popu":
				self.nb_optvar += 1
				cur.execute("SELECT popu from race_tb_v2 where date_horse like \"%s\"" % age)
				popu_tuple = cur.fetchall()
				popu = []
				for var in popu_tuple:
					if var[0] == None:
						popu.append(None)
					else:
						popu.append(int(var[0]))
				self.optvar.append(popu)
		
			elif var_name[i] == "length":
				self.nb_optvar += 1
				length = []
				for var in self.length:
					if var[0] == None:
						length.append(None)
					else:
						if int(var[0]) <=1200:
							length.append(1)
						elif int(var[0]) <=1400:
							length.append(2)
						elif int(var[0]) <=1600:
							length.append(3)
						elif int(var[0]) <=1800:
							length.append(4)
						elif int(var[0]) <=2000:
							length.append(5)
						elif int(var[0]) <=2200:
							length.append(6)
						elif int(var[0]) <=2500:
							length.append(7)
						else:
							length.append(8)
				self.optvar.append(length)
		
    
		self.optvar_prev = []
		self.nb_optvar_prev = 0
		for i in range(0, len(var_name)):
			if var_name[i] == "speed":
				self.nb_optvar_prev += 1
				cur.execute("SELECT speed from race_tb_v2 where date_horse like \"%s\"" % age)
				speed_tuple = cur.fetchall()
				speed = []
				for var in speed_tuple:
					if var[0] == None:
						speed.append(None)
					else:
						speed.append(max(int(float(var[0])/2.)-20, 1))
				self.optvar_prev.append(speed)
		
			elif var_name[i] == "diff":
				self.nb_optvar_prev += 1
				cur.execute("SELECT diff from race_tb_v2 where date_horse like \"%s\"" % age)
				diff_tuple = cur.fetchall()
				diff = []
				for var in diff_tuple:
					if var[0] == None:
						diff.append(None)
					else:
						diff.append(min(int(float(var[0])*10) +1, 30))
				self.optvar_prev.append(diff)

			elif var_name[i] == "posi":
				self.nb_optvar_prev += 1
				cur.execute("SELECT posi from race_tb_v2 where date_horse like \"%s\"" % age)
				posi_tuple = cur.fetchall()
				posi = []
				for var in posi_tuple:
					if var[0] == None:
						posi.append(None)
					else:
						if var[0].split("(")[1][0] == "逃":
							posi.append(1)
						elif var[0].split("(")[1][0] == "先":
							posi.append(2)
						elif var[0].split("(")[1][0] == "差":
							posi.append(3)
						elif var[0].split("(")[1][0] == "追":
							posi.append(4)
				self.optvar_prev.append(posi)


	def get_batch(self, nb_classes, race_class, field):
		
		################################################################################################
		########################### create horse information ###########################################
		horse_info = {}
		horses_inRace = {}
		
		n = 0
		for i in range(0, len(self.fin_odr)):
			if self.field[i][0] != field:
				continue
			if self.length[i][0] == "1000":
				continue

			date_P_R = self.date_horse[i][0].split("_")[0] +"_" +self.place[i][0] +"_" +self.R[i][0]
			horse_name = self.date_horse[i][0].split("_")[1]

			if self.nb_optvar ==0:
				optvar = [None]
			else:
				optvar      = [0] * self.nb_optvar
			if self.nb_optvar_prev ==0:
				optvar_prev = [None]
			else:
				optvar_prev = [0] * self.nb_optvar_prev

			if( (self.nb_optvar >0 and self.optvar[0][i] ==None) \
					or (self.nb_optvar_prev >0 and self.optvar_prev[0][i] ==None) \
			):
				continue
			else:
				for l in range(0, self.nb_optvar):
					optvar[l] = self.optvar[l][i]
				for l in range(0, self.nb_optvar_prev):
					optvar_prev[l] = self.optvar_prev[l][i]

				###############################################
				# [Date,Horse,Place,R,RaceClass,              #
				#  HorseNum,FinOrder,Odds_m1,Odds_m2,Odds_m3, #
				#  OptVar,Optvar_prev]                        #
				###############################################
				info = []
				info.append(self.date_horse[i][0].split("_")[0])
				info.append(self.date_horse[i][0].split("_")[1])
				info.append(self.place[i][0]) 
				info.append(self.R[i][0])
				info.append(self.race_class[i][0])
				info.append(self.horse_num[i][0])
				info.append(int(self.fin_odr[i][0].split("(")[0]))
				info.append(float(self.rst_odds_m1[i][0]))
				info.append(float(self.rst_odds_m2[i][0]))
				info.append(float(self.rst_odds_m3[i][0]))
				for l in range(0, self.nb_optvar):
					info.append(self.optvar[l][i])
				for l in range(0, self.nb_optvar_prev):
					info.append(self.optvar_prev[l][i])
					
				if date_P_R not in horses_inRace.keys():
					horses_inRace[date_P_R] = [horse_name]
				else:
					horses_inRace[date_P_R] = horses_inRace[date_P_R] + [horse_name]

				if horse_name not in horse_info.keys():
					horse_info[horse_name] = info
				else:
					horse_info[horse_name] += info
		################################################################################################
		
		################################################################################################
		for key in horse_info.keys():
			matrix = np.array(horse_info[key])
			if self.nb_optvar >0 and self.nb_optvar_prev >0:
				matrix = matrix.reshape(int(len(horse_info[key])/(10+self.nb_var)), 10+self.nb_var)
			horse_info[key] = matrix
		

		loop = 0
		#rst_odds_m = []
		#nb_horses = []
		fin_odr = []
		optvar = []
		optvar_prev = []
		for key in horse_info.keys():
			for i in reversed(range(1, horse_info[key].shape[0])):
				if ( \
      		horse_info[key][i][4] == AGE0+race_class or \
      		horse_info[key][i][4] == AGE1+race_class or \
      		horse_info[key][i][4] == AGE2+race_class or \
      		horse_info[key][i][4] == AGE3+race_class \
    		):
					
					date_P_R = horse_info[key][i][0] +"_" + horse_info[key][i][2] +"_" + horse_info[key][i][3]
					date = horse_info[key][i][0]
					
					if date_P_R not in horses_inRace.keys():
						continue

					fin_odr_temp = []
					optvar_temp = []
					
					blank_list = []

					for name in horses_inRace[date_P_R]:
						blank_flag = True
						for j in range(1, len(horse_info[name])):
							if date == horse_info[name][j][0]:
								blank_flag = False
								fin_odr_temp.append(horse_info[name][j][6])
								
								optvar_temp_temp = []
								for l in range(0, self.nb_optvar):
									optvar_temp_temp.append(horse_info[name][j][10+l])
								for l in range(0, self.nb_optvar_prev):
									optvar_temp_temp.append(horse_info[name][j-1][10+self.nb_optvar+l])
								optvar_temp.append(optvar_temp_temp)
						blank_list.append(blank_flag)

					
					full_flag = True
					for flag in blank_list:
						if flag == True:
							full_flag = False

					if full_flag == False:
						del horses_inRace[date_P_R]
						continue
					

					fin_odr.append(fin_odr_temp)
					optvar.append(optvar_temp)
					
					del horses_inRace[date_P_R]
					loop += 1

		optvar_new = []
		fin_odr_new = []
		loop_2 = 0
		for i in range(0, loop):
			for hh in range(0, len(optvar[i])):
				optvar_new_temp = []
				for h in range(0, len(optvar[i])):
					optvar_new_temp.append(optvar[i][h])
				optvar_new.append(optvar_new_temp)
				fin_odr_new.append(fin_odr[i][hh])
				loop_2 += 1
				temp = optvar[i][0]
				for j in range(1, len(optvar[i])):
					optvar[i][j-1] = optvar[i][j]
				optvar[i][len(optvar[i])-1] = temp


		nb_train = int(loop_2*0.8-1)
		nb_test  = int(loop_2*0.2-1)
		fin_odr_train = fin_odr_new[:nb_train]
		fin_odr_test = fin_odr_new[nb_train:nb_train+nb_test]
		optvar_train = optvar_new[:nb_train]
		optvar_test = optvar_new[nb_train:nb_train+nb_test]
		for i in range(0, len(optvar_train)):
			for j in range(0, 18 - len(optvar_train[i])):
				optvar_train[i].append(["0"] * self.nb_var)
		for i in range(0, len(optvar_test)):
			for j in range(0, 18 - len(optvar_test[i])):
				optvar_test[i].append(["0"] * self.nb_var)
		x_train      = np.array(optvar_train, dtype=np.int32)
		x_test       = np.array(optvar_test, dtype=np.int32)
		t_train = np.array(fin_odr_train, dtype=np.int32)
		t_test  = np.array(fin_odr_test, dtype=np.int32)

		train = []
		for i in range(0, nb_train):
			temp = (x_train[i], int(t_train[i]>=1 and t_train[i]<=3))
			train.append(temp)
		test = []
		for i in range(0, nb_test):
			temp = (x_test[i], int(t_test[i]>=1 and t_test[i]<=3))
			test.append(temp)

		return train, test, nb_train, nb_test


