from locust import HttpLocust, TaskSet, task
import json
import random
import pdb
import requests
import logging
# logging.basicConfig(filename="locust.log", level=logging.INFO)
# logger = logging.getLogger()
# logger.info('Start locust load testing')

pool_N = [ 120, 240, 480, 600 ]
class UserBehavior(TaskSet):
    # @task
    # def test(self):
    #     self.client.get("randomization/test")
    
    # @task
    # def CompleteRandomization(self):
    #     input = {'N': random.choice(pool_N), 'K': 2, 'Alloratio': (1, 1), 'seed': random.randint(1, 100000)}
    #     #pdb.set_trace()
    #     response = self.client.post("randomization/CompleteRandomization", json=input)
    #     #print("Response content: %s" % (response.content))
    #     try:
    #         res = json.loads(response.content)
    #         if res['status']=='failure':
    #             print('|CompleteRandomization| Response failure: %s' % response.content)
    #         else:
    #             pass
    #             #print("Response success: %s" % (res['status']))
    #     except:
    #         print('|CompleteRandomization| Error: %s' % response.content)
    # @task
    # def BlockRandomization(self):
    #     input = {'N': random.choice(pool_N), 'K': 3, 'Alloratio': (2, 2, 2), 'blocksize': 3, 'seed': random.randint(1, 100000)}
    #     #pdb.set_trace()
    #     response = self.client.post("randomization/BlockRandomization", json=input)
    #     #print("Response content: %s" % (response.content))
    #     try:
    #         res = json.loads(response.content)
    #         if res['status']=='failure':
    #             print('|BlockRandomization| Response failure: %s' % response.content)
    #         else:
    #             pass
    #             #print("|BlockRandomization| Response success: %s" % (res['status']))
    #     except:
    #         print('|BlockRandomization| Error: %s' % response.content)

    # @task
    # def StratifiedCompleteRandomization(self):
    #     input = {'N': [200,300,200], 'K': 2, 'Alloratio': (1, 1), 'seed': random.randint(1, 100000)}
    #     #pdb.set_trace()
    #     response = self.client.post("randomization/StratifiedCompleteRandomization", json=input)
    #     #print("Response content: %s" % (response.content))
    #     try:
    #         res = json.loads(response.content)
    #         if res['status']=='failure':
    #             print('|StratifiedCompleteRandomization| Response failure: %s' % response.content)
    #         else:
    #             pass
    #             #print("|StratifiedCompleteRandomization| Response: %s" % (res['status']))
    #     except:
    #         print('|StratifiedCompleteRandomization| Error: %s' % response.content)

    # @task
    # def StratifiedBlockRandomization(self):
    #     input = {'N': [200,300,200], 'K': 2, 'Alloratio': (1, 1), 'blocksize': 2, 'seed': random.randint(1, 100000)}
    #     #pdb.set_trace()
    #     response = self.client.post("randomization/StratifiedBlockRandomization", json=input)
    #     #print("Response content: %s" % (response.content))
    #     try:
    #         res = json.loads(response.content)
    #         if res['status']=='failure':
    #             print('|StratifiedBlockRandomization| Response failure: %s' % response.content)
    #         else:
    #             pass
    #             #print("|StratifiedBlockRandomization| Response success: %s" % (res['status']))
    #     except:
    #         print('|StratifiedBlockRandomization| Error: %s' % response.content)

    @task
    def MinimizationRandomization_independent(self):
        input = {'K': 3, 'Alloratio': (1, 2, 1), 'nlevel': (2, 2, 3), 'seed': random.randint(1, 200), 'MarkerOld': None, 'MarkerNew': {'PatientID': ['a', 'b'], 'F1': [1, 2], 'F2': [2, 1], 'F3': [2, 3], 'treatment': [ None, None ]}}
        #pdb.set_trace()
        response = self.client.post("randomization/MinimizationRandomization", json=input)
        #print("Response content: %s" % (response.content))
        try:
            res = json.loads(response.content)
            #pdb.set_trace()
            if res['status']=='failure':
                print('|MinimizationRandomization_independent| Response failure: %s' % response.content)
            else:
                #pass
                print("|MinimizationRandomization_independent| Response: %s" % (res))
        except:
            print('|MinimizationRandomization_independent| Error: %s' % response.content)
 
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000
# source activate py27
#locust -H http://115.28.228.102:83/ -f loadtest.py 
#locust -H http://115.28.228.102:83/ -f loadtest.py --logfile /media/data/Projects/youge/locust.log
