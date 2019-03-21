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
NB_EPOCH = 10
BATCH_SIZE  = 256
#OPTIMIZER =Adam()
VALIDATION_SPLIT = 0.2
VERBOSE = 1
NB_CLASSES = 2
##################################
print("race class:", RACE_CLASS)


############### Reading Data ###################
dataset = read_database(var_name, AGE, PASS_MySQL)
train, test, nb_train, nb_test = dataset.get_batch( \
	NB_CLASSES, \
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
net = L.Classifier(net, lossfun=F.softmax_cross_entropy)
optimizer = optimizers.Adam(alpha=0.001, beta1=0.9, beta2=0.999).setup(net)
updater = training.StandardUpdater(train_iter, optimizer)

trainer = training.Trainer(updater, (NB_EPOCH, "epoch"), out="result")
trainer.extend(extensions.LogReport())
trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
trainer.extend(extensions.Evaluator(valid_iter, net), name='val')
trainer.extend(extensions.PrintReport([ \
	'epoch', \
	'main/loss', \
	'main/accuracy', \
	'val/main/loss', \
	'val/main/accuracy', \
	'l1/W/data/std', \
	'elapsed_time' \
]))
trainer.extend(extensions.ParameterStatistics(net.predictor.l1, {'std': np.std}))
trainer.extend(extensions.PlotReport( \
	['l1/W/data/std'], \
	x_key='epoch', \
	file_name='std.png' \
))
trainer.extend(extensions.PlotReport( \
	['main/loss', 'val/main/loss'], \
	x_key='epoch', \
	file_name='loss.png' \
))
trainer.extend(extensions.PlotReport( \
	['main/accuracy', \
	'val/main/accuracy'], \
	x_key='epoch', \
	file_name='accuracy.png' \
))
trainer.extend(extensions.dump_graph('main/loss'))

trainer.run()

import subprocess
cmd = ["dot", "-Tpng", "result/cg.dot", "-o", "result/cg.png"]
subprocess.run(cmd)

serializers.save_npz("result/my_model.model", net)

## Evaluation for Test Data
test_evaluator = extensions.Evaluator(test_iter, net)
results = test_evaluator()
print('Test accuracy:', results['main/accuracy'])


## Inferring
infer_net = NeuralNet(var_name, NB_CLASSES)
infer_net = L.Classifier(infer_net)
serializers.load_npz("result/my_model.model", infer_net)

x = []
x.append(test[0][0])
x.append(test[1][0])
x.append(test[2][0])
x.append(test[3][0])
x.append(test[4][0])
x = np.array(x, dtype=np.int32)
print(x.shape)
with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
	y = infer_net.predictor(x=x)

y = y.array
print("y", y)
print(F.softmax(y))

