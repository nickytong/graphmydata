import requests
import urllib
import random
import json
import time
import pdb
import os, fnmatch
import re
from collections import OrderedDict

files_json = fnmatch.filter(os.listdir('.'), '*.json')

def submitJSON_minRand(file, input=None, outfile='myout.json'):
    """
    file: the json input file. if it is None, input will be specified
    input: OrderedDict as input
    outfile: output file in json format
    """
    #pdb.set_trace()
    if not file is None:
        outfile = file+'.output'
        with open(file, 'r') as f:
            data1 = json.load(f, object_pairs_hook=OrderedDict)
    else:
        data1 = input
    url = 'http://115.28.228.102:83/randomization/MinimizationRandomization'
    r = requests.post(url, json=data1)
    with open(outfile, 'w') as outf:
        outf.write(r.content.decode('utf-8'))



#submitJSON_minRand(files_json[0])

[ submitJSON_minRand(x) for x in files_json ]


#
# sequential request
#
def extractMarkerFromMiniRandOutput(file):
    """
    build markerNew from minimization randomization output in json file
    this returns an orderedDict that can be directly added to an OrderedDict of input before converted to JSON
    """
    with open(file, 'r') as f:
        data1 = json.load(f, object_pairs_hook=OrderedDict)
    regex = re.compile(r'^F\d+$')
    Fs = list(filter(regex.search, data1.keys())) # keys are in good order
    res = [ ('patientID', data1['patientID']) ]
    featureArray = [ (x, data1.get(x)) for x in Fs ]
    #pdb.set_trace()
    res.extend(featureArray)
    res.append(('treatment', data1['group']))
    return OrderedDict(res)


corePars = OrderedDict([('alloRatio', [1,2,1]), ('nlevel', [2,2,3]), ('weight', [2, 1, 3])])
# build marker-specific input
input = corePars.copy()
input['markerOld'] = extractMarkerFromMiniRandOutput(file='minimz_rand_N2.json.output')
input['markerNew'] = OrderedDict([('patientID', ['c', 'd', 'e']), ('F1', [2,1,1]), ('F2', [1,2,1]), ('F3', [2,3,1]), ('treatment', [None, None, None])])
submitJSON_minRand(file=None, input=input, outfile='minimz_rand_sequntial.json.output')
# # save the input as example of sequential call
with open('minimz_rand_sequntial.json', 'w') as outf:
    json.dump(input, outf)

def buildMarkerNew(N=1, nlevel=[2, 2], addPatientID=False, addNulltreatment=False):
    "build markerNew F1, F2, F3 from nlevel; Notice we can disable patientID and treatment for features only"
    res = OrderedDict()
    # patient ID using current time in milisec ++
    if addPatientID:
        tstart = int(round(time.time() * 1000))
        res['patientID'] = [ str(tstart+x) for x in range(N)]
    for j in range(len(nlevel)):
        # for 1~length(nlevel) features, generate feature array for all N samples, given eg. "F1":[1,2,1,1]
        Fcandidates = [ x for x in range(1, nlevel[j]+1) ] # this is integer
        Ftmp = []
        for i in range(N):
            Ftmp.append(random.choice(Fcandidates))
        res['F'+str(j+1)] = Ftmp
    if addNulltreatment:
        res['treatment'] = [ None for x in range(N) ]
    return res


buildMarkerNew(N=3, nlevel=[2, 2], addPatientID=True, addNulltreatment=True)

def submitJSON_minRand_sequential(file_init=None, corePars=None, file_sequential='autosequentialout.json'):
    myinput = corePars.copy()
    """
    file_init: either load markerOld or None and submit first request.
            init is needed since the first time, we need to specify markerOld 
            differently: for first, either load json input or None; for rest, 
            extract marker from previous output
    file_sequential: specify pattern of output. _0, _1, ... will be added
    """
    if file_init is None:
        myinput['markerOld'] = None
    else:
        myinput['markerOld'] = extractMarkerFromMiniRandOutput(file=file_init)
    myinput['markerNew'] = buildMarkerNew(N=1, nlevel=myinput['nlevel'], addPatientID=True, addNulltreatment=True)
    outbase = os.path.splitext(file_sequential)[0]
    myoutfile = outbase+'_0'+'.json.output'
    #pdb.set_trace()
    submitJSON_minRand(file=None, input=myinput, outfile=myoutfile)
    for r in range(1, 10):
        myinput = corePars.copy()
        #myinput['seed'] = int(round(time.time()*1000))
        myoutfileNew = outbase+'_'+str(r)+'.json.output'
        myinput['markerOld'] = extractMarkerFromMiniRandOutput(file=myoutfile)
        myinput['markerNew'] = buildMarkerNew(N=1, nlevel=myinput['nlevel'], addPatientID=True, addNulltreatment=True)
        #pdb.set_trace()
        submitJSON_minRand(file=None, input=myinput, outfile=myoutfileNew)
        myoutfile = myoutfileNew # now used next markerOld


corePars = OrderedDict([ ('K', 2), ('alloRatio', [1,1]), ('nlevel', [2,2]), ('weight', [1, 1])])
submitJSON_minRand_sequential(file_init=None, corePars=corePars, file_sequential='autosequentialout.json')


####### testing debugging
with open('minimz_rand_N1.json', 'r') as f:
    data1 = json.load(f , object_pairs_hook=OrderedDict) #

with open('minimz_rand_N2.json', 'r') as f:
    data2 = json.load(f , object_pairs_hook=OrderedDict) # 

#url = 'http://127.0.0.1:8000/randomization/MinimizationRandomization'
url = 'http://115.28.228.102:83/randomization/MinimizationRandomization'
r = requests.post(url, json=data1)
r = requests.post(url, json=data2)
json.dumps(r.content)

with open('myout.txt', 'w') as outf:
    outf.write(r.content.decode('utf-8'))
with open('myout.txt', 'r') as f:
    myout = json.load(f, object_pairs_hook=OrderedDict)

# r = requests.post(url, json=input)
# r.content.decode('utf-8')

