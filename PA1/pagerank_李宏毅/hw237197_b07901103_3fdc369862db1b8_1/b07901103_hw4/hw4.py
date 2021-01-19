import sys
import numpy as np
import pandas as pd

def load(fname):
  f = open(fname, 'r').readlines()
  n = len(f)
  ret = {}
  for l in f:
    l = l.split('\n')[0].split(',')
    i = int(l[0])
    ret[i] = {}
    for j in range(n):
      if str(j) in l[1:]:
        ret[i][j] = 1
      else:
        ret[i][j] = 0
  ret = pd.DataFrame(ret).values
  return ret

def get_tran(g):
	# TODO	
  temp = [[0.0]*len(g[0]) for i in range(len(g))]
	# count number of "1" in one row
  for i in range(len(g[0])):
    count = 0
    for j in range(len(g)):
      if (g[j][i] != 0):
        count += 1
	# transit the "1" to possibility]
    for k in range(len(g)):
      if (g[k][i] != 0):
        temp[k][i] = 1/count
  temp = np.reshape(temp, (len(g), len(g[0])))
  return temp

def cal_rank(t, d = 0.85, max_iterations = 1000, alpha = 0.001):
	# TODO
	# 1. initialize all pagerank in R0 with 1/N
  num_row = len(t)
  R0 = [[1.00]*1 for i in range(num_row)]
  for i in range(num_row):
    R0[i][0] = R0[i][0] / num_row
  R = np.reshape(R0, (num_row, 1))
  R_new = (1-d)*R + d*np.dot(t, R)

	# 2. iteratively calculate R(t+1)
  count = 0
  while ((dist(R_new, R) > alpha) and (count < max_iterations)):
    R_new = (1-d)*R + d*np.dot(t, R_new)
    count += 1
	# 3. sort the nodes according to the R and return the most important ten nodes
  dict = {}
  for i in range(len(R_new)):
    dict[R_new[i][0]] = i
  R_sort = np.reshape(R_new, (1, -1))
  R_sort.sort()
  R_sort = np.reshape(R_sort, (-1, 1))
  catch = np.zeros((10, 1))
  R10 = []
  for i in range(10):						# to test, use range(5), hw : range(10)
    R10.append(R_sort[-1-i][0])
  for i in range(10):
    catch[i][0] = dict[R10[i]]
  return catch

def save(t, r):
	# TODO
  t_m = np.savetxt('1.txt', t)
  rank = np.savetxt('2.txt', r, '%1.1d')
  return t_m, rank

def dist(a, b):
  return np.sum(np.abs(a-b))

def main():
  graph = load(sys.argv[1])
  transition_matrix = get_tran(graph)
  rank = cal_rank(transition_matrix)
  save(transition_matrix, rank)

if __name__ == '__main__':
	main()