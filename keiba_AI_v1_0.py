import numpy as np
import sys
from read_dataset import read_database
from networks import NeuralNet
import chainer
from chainer import iterators
from chainer import optimizers
import chainer.links as L
import chainer.functions as F
from chainer.datasets import split_dataset_random
from chainer.dataset import concat_examples
from chainer import serializers
from chainer import training
from chainer.training import extensions
import matplotlib.pyplot as plt
import myFunctions as myF

varlist_file = "./var_list.txt"
var_name = []
with open(varlist_file, "r") as f:
	for line in f:
		if len(line.split("\n")[0]) > 0 and line.split("\n")[0][0] != "#":
			var_name.append(line.split("\n")[0])

print("using variables:", var_name)


args = sys.argv
PASS_MySQL = args[1]

##################################
AGE="201%"
RACE_CLASS="500万下"
FIELD="ダ"
#FIELD="芝"
##################################
NB_INPUT = len(var_name)
NB_EPOCH = 20
BATCH_SIZE  = 512
VALIDATION_SPLIT = 0.2
VERBOSE = 1
NB_CLASSES = 4
##################################
print("race class:", RACE_CLASS)


############### Reading Data ###################
dataset = read_database(var_name, AGE, PASS_MySQL)
train, test, nb_train, nb_test \
		= dataset.get_batch(NB_CLASSES, \
                        RACE_CLASS, \
												FIELD \
												)
train, valid = split_dataset_random(train, int(nb_train*0.8), seed=0)
print("nb_train:", len(train))
print("nb_valid:", len(valid))
print("nb_test:", len(test))
################################################

train_iter = iterators.SerialIterator(train, BATCH_SIZE)
valid_iter = iterators.SerialIterator(valid, BATCH_SIZE, repeat=False, shuffle=False)
test_iter  = iterators.SerialIterator(test, BATCH_SIZE, repeat=False, shuffle=False)

net = NeuralNet(var_name, NB_CLASSES)
optimizer = optimizers.Adam(alpha=0.001, beta1=0.9, beta2=0.999).setup(net)

plt_x = []
plt_y_train = []
plt_y_valid = []
while train_iter.epoch < NB_EPOCH:

	train_batch = train_iter.next()
	x, t = concat_examples(train_batch)

	### prediction value
	y = net(x)

	# loss
	t_onehot = myF.create_onehot(t)
	loss = F.sigmoid_cross_entropy(y, t_onehot)

	# gradient
	net.cleargrads()
	loss.backward() # start Back-Propagation

	# update parameters
	optimizer.update()

	
	# Validation
	if train_iter.is_new_epoch:
		print('epoch:{:02d} train_loss:{:.04f} '.format( \
						train_iter.epoch, loss.data), end='')
		plt_x.append(train_iter.epoch) 
		plt_y_train.append(loss.data)
		
		valid_losses = []
		valid_accuracies = []
		while True:
			valid_batch = valid_iter.next()
			x_valid, t_valid = concat_examples(valid_batch)
			with chainer.using_config("train", False), \
						chainer.using_config("enable_backprop", False):
				y_valid = net(x_valid)
			
			t_valid_onehot = myF.create_onehot(t_valid)
			loss_valid = F.sigmoid_cross_entropy(y_valid, t_valid_onehot)
			valid_losses.append(loss_valid.array)

			accuracy = F.accuracy(y_valid, t_valid)
			valid_accuracies.append(accuracy.array)

			if valid_iter.is_new_epoch:
				valid_iter.reset()
				break

		print('val_loss:{:.04f} val_accuracy:{:.04f}'.format( \
						np.mean(valid_losses), np.mean(valid_accuracies)))
		plt_y_valid.append(np.mean(valid_losses))

serializers.save_npz("result/my_model.model", net)

plt.plot(plt_x, plt_y_train, label="train")
plt.plot(plt_x, plt_y_valid, "r", label="valid")
plt.legend()
plt.title("Loss")
plt.show()

## Inferring
infer_net = NeuralNet(var_name, NB_CLASSES)
serializers.load_npz("result/my_model.model", infer_net)


x, t = concat_examples(test)
with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
	y = infer_net.predict(x[30:40])
print(x[30:40], t[30:40])
print(y)



