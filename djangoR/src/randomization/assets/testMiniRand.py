import requests
import urllib
import random
import json
import time
from multiprocessing.dummy import Pool as ThreadPool 

input = {'K': 3, 'Alloratio': (1, 2, 1), 'nlevel': (2, 2, 3), 'seed': 1, 'MarkerOld': None, 'MarkerNew': {'PatientID': ['a', 'b'], 'F1': [1, 2], 'F2': [2, 1], 'F3': [2, 3], 'treatment': [None, None]}}
input = {'K': 3, 'Alloratio': (1, 2, 1), 'nlevel': (2, 2, 3), 'seed': 1, 'MarkerOld': None, 'MarkerNew': {'F1': [1, 2], 'PatientID': ['a', 'b'], 'F2': [2, 1], 'F3': [2, 3], 'treatment': [None, None]}}
url = 'http://127.0.0.1:8000/randomization/MinimizationRandomization'
r = requests.post(url, json=input)

for i in range(10):
	input = {'K': 3, 'Alloratio': (1, 2, 1), 'nlevel': (2, 2, 3), 'seed': random.randint(1, 100000), 'MarkerOld': None, 'MarkerNew': {'PatientID': ['a', 'b'], 'F1': [1, 2], 'F2': [2, 1], 'F3': [2, 3], 'treatment': [ None, None ]}}
	url = 'http://127.0.0.1:8000/randomization/MinimizationRandomization'
	#url = 'http://115.28.228.102:83/randomization/MinimizationRandomization'
	r = requests.post(url, json=input)
	print('run: %d --> %s' % (i, json.loads(r.content)['group']))
	#time.sleep(0.1)

def myMinimizationRandomization(seed):
	input = {'K': 3, 'Alloratio': (1, 2, 1), 'nlevel': (2, 2, 3), 'seed': seed, 'MarkerOld': None, 'MarkerNew': {'PatientID': ['a', 'b'], 'F1': [1, 2], 'F2': [2, 1], 'F3': [2, 3], 'treatment': [ None, None ]}}
	#url = 'http://127.0.0.1:8000/randomization/MinimizationRandomization'
	url = 'http://115.28.228.102:83/randomization/MinimizationRandomization'
	r = requests.post(url, json=input)
	print('seed: %d --> %s' % (seed, json.loads(r.content)['group']))


pool = ThreadPool(5) 
results = pool.map(myMinimizationRandomization, [ x for x in range(200) ])
pool.close() 
pool.join() 
