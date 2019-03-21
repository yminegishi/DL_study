import chainer
import chainer.links as L
import chainer.functions as F
from chainer import Variable
import numpy as np
import myFunctions as myF

####################
OUTPUT_DIM = 10
HIDDEN_RATE = 1
DROPOUT_RATIO = 0.25
####################


class NeuralNet(chainer.Chain):
	def __init__(self, var_name, num_classes):
		super(NeuralNet, self).__init__()
		
		self.var_name = var_name
		self.nb_var = len(var_name)
		self.var_dim = {}
		self.loop = 0

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

		#########################################################
		# weights to update should be placed under init_scope() #
		#########################################################
		with self.init_scope():
			self.l1 = L.Linear(self.nb_var*OUTPUT_DIM, num_classes, nobias=True)

			###############################
			# self.embs.shape: (nb_var, ) #
			###############################
			self.embs = []
			for v in range(0, self.nb_var):
				emb = L.EmbedID(self.var_dim[self.var_name[v]], OUTPUT_DIM)
				self.embs.append(emb)

	##########################
	# x: (nb_batch, nb_var)  #
	# t: (nb_batch)          #
	##########################
	def __call__(self, x):

		#####################################
		# inputs_horse: (nb_var, nb_batch)  #
		#####################################
		inputs_var = []
		for v in range(0, x.shape[1]):
			data_batch = []
			for i in range(0, x.shape[0]):
				data = x[i][v]
				data_batch.append(np.array(data, dtype=np.int32))
			inputs_var.append(np.array(data_batch, dtype=np.int32))
		inputs_var = np.array(inputs_var, dtype=np.int32)
		
		##############################################
		# embs_horse: (nb_var, nb_batch, OUTPUT_DIM) #
		##############################################
		embs_var = []
		for v in range(0, self.nb_var):
			normalized = np.array(self.embs[v](inputs_var[v]).data, dtype=np.float32)
			for i in range(0, x.shape[0]):
				normalized[i] = normalized[i] / np.linalg.norm(normalized[i])
			embs_var.append(normalized)
		embs_var = np.array(embs_var, dtype=np.float32)
			
		###############################################
		# embs_batch-> (nb_batch, nb_var, OUTPUT_DIM) #
		###############################################
		embs_batch = []
		for i in range(0, x.shape[0]):
			data_var = []
			for v in range(0, x.shape[1]):
				data_var.append(np.array(embs_var[v][i], dtype=np.float32))
			embs_batch.append(np.array(data_var, dtype=np.float32))
		
		#############################################
		# embs_batch->(nb_batch, nb_var*OUTPUT_DIM) #
		#############################################
		for i in range(0, x.shape[0]):
			embs_batch[i]	= embs_batch[i].reshape((self.nb_var*OUTPUT_DIM, ))
		embs_batch = Variable(np.array(embs_batch, dtype=np.float32))
		
		self.loop += 1
		w_out = self.l1(embs_batch)
		return w_out

	def predict(self, x):
		#####################################
		# inputs_horse: (nb_var, nb_batch)  #
		#####################################
		inputs_var = []
		for v in range(0, x.shape[1]):
			data_batch = []
			for i in range(0, x.shape[0]):
				data = x[i][v]
				data_batch.append(np.array(data, dtype=np.int32))
			inputs_var.append(np.array(data_batch, dtype=np.int32))
		inputs_var = np.array(inputs_var, dtype=np.int32)
		
		##############################################
		# embs_horse: (nb_var, nb_batch, OUTPUT_DIM) #
		##############################################
		embs_var = []
		for v in range(0, self.nb_var):
			normalized = np.array(self.embs[v](inputs_var[v]).data, dtype=np.float32)
			for i in range(0, x.shape[0]):
				normalized[i] = normalized[i] / np.linalg.norm(normalized[i])
			embs_var.append(normalized)
		embs_var = np.array(embs_var, dtype=np.float32)

		###############################################
		# embs_batch-> (nb_batch, nb_var, OUTPUT_DIM) #
		###############################################
		embs_batch = []
		for i in range(0, x.shape[0]):
			data_var = []
			for v in range(0, x.shape[1]):
				data_var.append(np.array(embs_var[v][i], dtype=np.float32))
			embs_batch.append(np.array(data_var, dtype=np.float32))
		
		#############################################
		# embs_batch->(nb_batch, nb_var*OUTPUT_DIM) #
		#############################################
		for i in range(0, len(x)):
			embs_batch[i]	= embs_batch[i].reshape((self.nb_var*OUTPUT_DIM, ))
		embs_batch = np.array(embs_batch, dtype=np.float32)
	
		unit_matrix = np.eye(self.nb_var*OUTPUT_DIM, dtype=np.float32)
		w_out = self.l1(unit_matrix)

		dot = []
		for i in range(0, len(x)):
			dot.append(np.dot(embs_batch[i], w_out.data))
		dot = np.array(dot, dtype=np.float32)

		softmax = F.softmax(dot)
		return softmax


