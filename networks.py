import chainer
import chainer.links as L
import chainer.functions as F
from chainer import Variable
import numpy as np
import myFunctions as myF

####################
OUTPUT_DIM = 5
HIDDEN_RATE = 1
DROPOUT_RATIO = 0.25
####################


class NeuralNet(chainer.Chain):
	def __init__(self, var_name, num_classes):
		super(NeuralNet, self).__init__()
		
		self.var_name = var_name
		self.nb_var = len(var_name)
		self.var_dim = {}
		self.s_end = np.zeros((self.nb_var, OUTPUT_DIM), dtype=np.float32)

		for i in range(0, len(self.var_name)):
			if self.var_name[i] == "jockey":
				self.var_dim["jockey"] = 17
			elif self.var_name[i] == "frame":
				self.var_dim["frame"] = 9
			elif self.var_name[i] == "train_score":
				self.var_dim["train_score"] = 5
			elif self.var_name[i] == "popu":
				self.var_dim["popu"] = 19
			elif self.var_name[i] == "length":
				self.var_dim["length"] = 9
			## for prev
			elif self.var_name[i] == "speed":
				self.var_dim["speed"] = 56
			elif self.var_name[i] == "diff":
				self.var_dim["diff"] = 32
			elif self.var_name[i] == "posi":
				self.var_dim["posi"] = 5

		with self.init_scope():
			self.l1 = L.Linear(18*self.nb_var*OUTPUT_DIM, 18*self.nb_var*OUTPUT_DIM*HIDDEN_RATE)
			self.l2 = L.Linear(18*self.nb_var*OUTPUT_DIM*HIDDEN_RATE, num_classes)
			
			###############################
			# self.embs.shape: (nb_var, ) #
			###############################
			self.embs = []
			for j in range(0, self.nb_var):
				emb = L.EmbedID(self.var_dim[self.var_name[j]], OUTPUT_DIM)
				self.embs.append(emb)

	#############################
	# x: (nb_batch, 18, nb_var) #
	# t: (nb_batch)             #
	#############################
	def __call__(self, x):

		########################################
		# inputs_horse: (18, nb_var, nb_batch) #
		########################################
		inputs_horse = []
		for h in range(0, x.shape[1]):
			data_var = []
			for v in range(0, x.shape[2]):
				data_batch = []
				for i in range(0, x.shape[0]):
					data = x[i][h][v]
					data_batch.append(np.array(data, dtype=np.int32))
				data_var.append(np.array(data_batch, dtype=np.int32))
			inputs_horse.append(np.array(data_var, dtype=np.int32))
		
		##################################################
		# embs_horse: (18, nb_var, nb_batch, OUTPUT_DIM) #
		##################################################
		embs_horse = []
		for h in range(0, 18):
			embs_var = []
			for v in range(0, self.nb_var):
				normalized = np.array(self.embs[v](inputs_horse[h][v]).data, dtype=np.float32)
				
				for i in range(0, x.shape[0]):
					normalized[i] = normalized[i] / np.linalg.norm(normalized[i])
				
				embs_var.append(normalized)
			embs_horse.append(np.array(embs_var, dtype=np.float32))
		embs_horse = np.array(embs_horse, dtype=np.float32)

		###################################################
		# embs_batch-> (nb_batch, 18, nb_var, OUTPUT_DIM) #
		###################################################
		embs_batch = []
		for i in range(0, x.shape[0]):
			data_horse = []
			for h in range(0, x.shape[1]):
				data_var = []
				for v in range(0, x.shape[2]):
					data_var.append(np.array(embs_horse[h][v][i], dtype=np.float32))
				data_horse.append(np.array(data_var, dtype=np.float32))
			embs_batch.append(np.array(data_horse, dtype=np.float32))
		
		################################################
		# embs_batch->(nb_batch, 18*nb_var*OUTPUT_DIM) #
		################################################
		for i in range(0, x.shape[0]):
			embs_batch[i]	= embs_batch[i].reshape((18, self.nb_var*OUTPUT_DIM))
			embs_batch[i]	= embs_batch[i].reshape((18*self.nb_var*OUTPUT_DIM, ))
		embs_batch = Variable(np.array(embs_batch, dtype=np.float32))
		
		
		dropout = F.dropout(self.l1(embs_batch), ratio=DROPOUT_RATIO)
		#h1 = F.relu(dropout)
		h1 = F.tanh(dropout)
		h2 = self.l2(h1)
		return h2


