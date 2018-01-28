import os, sys, ipdb, pdb, time
import json
import random
import math
from functools import reduce    # need this line if you're using Python3.x
from collections import OrderedDict
import pyRserve
from pyRserve import TaggedList
import numpy as np



def gcd(*numbers):
    """Return the greatest common divisor of the given integers"""
    return reduce(math.gcd, numbers)

def lcm_list(li):
    """
    computes the least common multiple from a list of integers
    """
    def lcm2(a, b):
        if a > b:
            greater = a
        else:
            greater = b
        while True:
            if greater % a == 0 and greater % b == 0:
                lcm = greater
                break
            greater += 1
        return lcm
    return reduce(lambda x, y: lcm2(x, y), li)
#ans = lcm_list([1, 2, 3, 4, 5, 6, 7, 8, 9])



def parseRandomizationResult(dat):
    """
    parse the result from R: in R it is a named list: list(assign=assign,summary=table(assign$group))
            assign itself is a dataframe
    in python, this becomes tagged list.  
    **WARNING**: THIS ASSUMES FIXED FORMAT FROM R SIDE; WILL BREAK IF THE R SIDE CHANGES!!!    
    In general, python numpy/list etc is not as very well designed / smoothed transition as R
    This makes below code ugly long!
    """
    # dummy case: no return from R due to error
    #ipdb.set_trace()
    if dat is None:
        return None
    lv1names = [ str(x) for x in dat.keys ]
    assign = dat[lv1names[0]] # this is the assign part, still tagged list
    summary = dat[lv1names[1]] # this is the summary part, attrArray
    assignnames = [ str(x) for x in assign.keys ]
    res = {}
    #ipdb.set_trace()
    # each column in assign dataframe become an element keyed by colname valued by list
    for aname in assignnames:
        res[aname] = assign[aname].tolist() if isinstance(assign[aname], np.ndarray) else [ assign[aname] ] # for 1 patient, it is not array
    #ipdb.set_trace()
    # summary becomes a list or list of list
    if isinstance(summary, pyRserve.taggedContainers.AttrArray):
        #ipdb.set_trace()
        res[lv1names[1]] = summary.tolist()
        if len(summary.attr['dimnames'])==2:
            if isinstance(summary.attr['dimnames'][0], str):
                res[lv1names[1]+'_rowname'] = [ summary.attr['dimnames'][0] ] # 1 row: rowname is str, np.array
            else:
                res[lv1names[1]+'_rowname'] = summary.attr['dimnames'][0].tolist()
            res[lv1names[1]+'_colname'] = summary.attr['dimnames'][1].tolist()
    if isinstance(summary, pyRserve.taggedContainers.TaggedList):
        res[lv1names[1]] = {}
        smrynames = [ str(x) for x in summary.keys ]
        for smrycol in smrynames:
            if isinstance(summary[smrycol], np.ndarray):
                res[lv1names[1]][smrycol] = summary[smrycol].tolist()
            else:
                res[lv1names[1]][smrycol] = [summary[smrycol]]
        #ipdb.set_trace()
        #res[lv1names[1]+'_colname'] = smrynames
        res[lv1names[1]+'_rowname'] = [ 'group '+str(x) for x in list(range(1, 1+len(summary[smrynames[0]].tolist()))) ]
    #ipdb.set_trace()
    res['status'] = 'success'
    return res

def validateInput(dat, isStratified=False, isBlocked=False, required0=[ 'N', 'alloRatio' ], required_int=['N', 'alloRatio', 'K', 'blockSize', 'seed', 'nfactor', 'nlevel' ], default_seed=1):
    """
    required0: required input variable name. this is passed by each view function
    required_int: require being integer for input variable. this is a default list. it may contain vars not in required; intersect is taken 
    """
    try:
        # test valid json format
        #pdb.set_trace()
        input = json.loads(dat, object_pairs_hook=OrderedDict)
    except:
        input = {'valid': False, 'status': 'failure', 'message': 'Input invalid: not valid JSON format for %s' % (dat) }
        return input
    input['valid'] = True
    input['message'] = 'Input is valid'
    required = required0[:] # now a copy, not interfer with each other
    def require_int(input, varnames):
        for vn in varnames:
            vv = input[vn]
            #ipdb.set_trace()
            # might be a list
            if type(vv) is list or type(vv) is tuple:
                for x in list(vv):
                    if not isinstance(x, int):
                        input['valid'] = False
                        input['message'] = 'Input invalid: %s (%s) not integer' % (vv, x)
                        return input
            else:
                if not isinstance(vv, int):
                    input['valid'] = False
                    input['message'] = 'Input invalid: %s (%s) not integer' % (vn, vv)
                    return input
        return input
    def append_status(input):
        input['status'] = 'success' if input['valid'] else 'failure'
        return dict(input) # Django REST does not work on orderedDict, only regular dict
    if isBlocked:
        #ipdb.set_trace()
        required.append('blockSize')
    # check for required variables
    for rv in required:
        if rv not in input:
            input['valid'] = False
            input['message'] = 'Input invalid: %s must be specified' % (rv)
            return append_status(input)
    # set default K: across all settings, alloRatio determines K
    if 'alloRatio' in required and 'K' not in input:
        input['K'] = len(input['alloRatio'])
    # set default nfactor: across all settings, nlevel determines nfactor
    if 'nlevel' in required and 'nfactor' not in input:
        input['nfactor'] = len(input['nlevel'])
    if 'seed' not in input:
        #input['seed'] = default_seed # default seed
        #input['seed'] = int(round(time.time()*1000)) # too long, R cannot receive
        input['seed'] = int(round(time.time()*1000)) % 100000000 # time in miliseconds
    input = require_int(input, varnames=[ val for val in required_int if val in required ])
    if not input['valid']:
        return input
    #ipdb.set_trace()
    if 'alloRatio' in required and input['K'] != len(input['alloRatio']):
        input['valid'] = False
        input['message'] = 'Input invalid: K should be equal to length of alloRatio'    
        return append_status(input)  
    if 'nlevel' in required and input['nfactor'] != len(input['nlevel']):
        input['valid'] = False
        input['message'] = 'Input invalid: nfactor should be equal to length of nlevel'    
        return append_status(input)  
    if 'alloRatio' in required:
        gcdr = gcd(*input['alloRatio'])
        if gcdr != 1:
            # auto-correct alloRation, e.g. [2, 4] ==> [1, 2]
            input['alloRatio'] = [ x // gcdr for x in input['alloRatio'] ]
    #ipdb.set_trace()
    if isStratified:
        #ipdb.set_trace()
        if isinstance(input['N'], int) or len(input['N'])<2:
            input['valid'] = False
            input['message'] = 'Input invalid: N (%s) must be a list with multiple values for stratified design' % (input['N'])
            return append_status(input)
    # check N is a multiple of several factors.
    if 'N' in required:
        lcm_elements = []
        if isBlocked:
            lcm_elements.append(input['blockSize'])
        lcm_elements.extend([ input['K'], sum(input['alloRatio']) ])
        min_N = lcm_list(lcm_elements)
        if isStratified:
            # multiple N case
            #ipdb.set_trace()
            for i in range(len(input['N'])):
                myn = input['N'][i]
                if myn % min_N != 0:
                    input['valid'] = False
                    input['message'] = 'Input invalid: N (%d) of strata %d must be a multiple of K, sum(alloRatio) and blockSize, which means a multiple of %d' % (myn, i+1, min_N)
                    return append_status(input)
        else:
            if input['N'] % min_N != 0:
                input['valid'] = False
                input['message'] = 'Input invalid: N (%d) must be a multiple of K, sum(alloRatio) and blockSize, which is a multiple of %d' % (input['N'], min_N)
                return append_status(input)
    if 'markerNew' in required:
        # orderedDict to TaggedList conversion: preserve user specified variable name. this can be passed to R as named list, easy for R data frame conversion
        def convertMarkerData(dat):
            # list to array
            if not isinstance(dat, OrderedDict):
                input['valid'] = False
                input['message'] = 'Input invalid: Marker (specified as %s) must be a (ordered) dictionary in python converted from JSON' % (mykeys[-1])
                return append_status(input)
            mykeys = [x for x in dat.keys()]
            #ipdb.set_trace()
            if mykeys[0] != 'patientID':
                input['valid'] = False
                input['message'] = 'Input invalid: First element of marker (specified as %s) must be keyed with patientID' % (mykeys[0])
                #ipdb.set_trace()
                return append_status(input)
            #ipdb.set_trace()
            if mykeys[-1] != 'treatment':
                input['valid'] = False
                input['message'] = 'Input invalid: Last element of marker (%s) must be keyed with treatment' % (dat)
                return append_status(input)    
            for k, v in dat.items():
                dat[k] = np.array([ x if x is not None else '' for x in v]) # None to ''
            res = TaggedList(list(dat.items())) 
            return res
        #ipdb.set_trace()
        input['markerNew'] = convertMarkerData(input['markerNew'])
        if input['markerOld'] is not None:
            input['markerOld'] = convertMarkerData(input['markerOld'])
        else:
            input['markerOld'] = ''
        if 'weight' in input:
            if len(input['weight']) != len(input['nlevel']):
                input['valid'] = False
                input['message'] = 'Input invalid: weight (%s) must be the same length as nlevel (%s)' % (input['weight'], input['nlevel'])
                return append_status(input)
        else:
            input['weight'] = ''
    return append_status(input)
