import numpy as np

def create_onehot(t):
  t_onehot = []
  for i in range(t.shape[0]):
    temp = np.zeros((4, ), dtype=np.int32)
    temp[t[i]] = 1
    t_onehot.append(temp)
  t_onehot = np.array(t_onehot, dtype=np.int32)
  return t_onehot


