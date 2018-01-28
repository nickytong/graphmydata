from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape

from .models import SimpleRandomization
from .serializers import SimpleRandomizationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import os, sys, ipdb
import json
import pyRserve
from pyRserve import TaggedList
import time
from .utils import validateInput, parseRandomizationResult
PORT = 6000
# connectR(port=PORT)
# conn = pyRserve.connect(host='localhost', port=PORT)
nTryConnect = 5    
def reconnect():
    "During remote access, Rserve connection may be lost; thus need reconnect"
    try:
        conn.close()
    except:
        pass
    try:
        conn.connect()
    except:
        pass
    time.sleep(0.5)
    

# if 'conn' not in locals():
#     conn = connectR(port = 6000)
###
# need to source script for setup; this can be done in Rserve config; however, it becomes difficult on windows
# here we run the Rscript file using absolute path
###
#conn = pyRserve.connect(host='localhost', port=6311)
#conn.eval('1+1')
#conn.eval("source('../assets/Rscript/randomizeFunction.R')")
# does not work: need to source this in R: 
#conn.eval('source("randomizeFunction.R")')
# def loadRscript(file):
#     with open(file, 'r') as f:
#         src=f.read()
#     conn.eval(src)


#loadRscript(file='D:\\Projects\\RServe\\DjangoR\\src\\randomization\\assets\\randomizeFunction.R')        
# loadRscript(file='randomization\\assets\\randomizeFunction.R')        


# Create your views here.
# this view decoupled from model and serializer, always recompute the result
class CompleteRandomizationView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    #renderer_classes = (JSONRenderer, )
    # def get(self, request, format=None):
    #     # N = request.GET.get('N')
    #     # if N is None:
    #     # 	N = 10
    #     #result = conn.r.rnorm(N)
    #     result = conn.eval('CompleteRandomization(N=60,K=2,alloRatio=c(1,1),seed=4)')
    #     content = {'allocation': result[0].tolist(), 'summary': result[1].tolist()}
    #     return Response(content)
    def post(self, request, format=None):
        """
        implements post method: assumes input is in json format
        """
        input = validateInput(request.body, isStratified=False, isBlocked=False)
        if not input['valid']:
            return Response(input)
        #return Response(request.body)
        #return HttpResponse(request.body)
        # this is ugly: Rserver lost connection with no feedback, even cannot check if it is still connected
        #   So when we do not receive result, the first thing is try reconnect; then it is something else that gives no result
        content, nTryConnect = None, 0
        while content is None and nTryConnect<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                result = conn.r.CompleteRandomization(N=input['N'], K=input['K'],Alloratio=input['alloRatio'],seed=input['seed'])
                content = parseRandomizationResult(result)
                content['seed'] = input['seed']
            except:
                e = sys.exc_info()
                #reconnect()
            conn.close()
            nTryConnect += 1
        if nTryConnect==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
            #ipdb.set_trace()
        return Response(content)

class BlockRandomizationView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    def post(self, request, format=None):
        """
        implements post method: assumes input is in json format
        """
        #return Response(request.body)
        #return HttpResponse(request.body)
        input = validateInput(request.body, isStratified=False, isBlocked=True)
        if not input['valid']:
            return Response(input)
        content, nTryConnect = None, 0
        while content is None and nTryConnect<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                result = conn.r.BlockRandomization(N=input['N'], K=input['K'],Alloratio=input['alloRatio'], blocksize=input['blockSize'], seed=input['seed'])
                content = parseRandomizationResult(result)
                content['seed'] = input['seed']
            except:
                e = sys.exc_info()
            conn.close()
            nTryConnect += 1
        if nTryConnect==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
            #ipdb.set_trace()
        return Response(content)


class StratifiedCompleteRandomizationView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    def post(self, request, format=None):
        """
        implements post method: assumes input is in json format
        """
        input = validateInput(request.body, isStratified=True, isBlocked=False)
        #ipdb.set_trace()
        if not input['valid']:
            #ipdb.set_trace()
            return Response(input)
        content, nTryConnect = None, 0
        while content is None and nTryConnect<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                result = conn.r.StratifiedCompleteRandomization(N=input['N'], K=input['K'],Alloratio=input['alloRatio'], seed=input['seed'])
                content = parseRandomizationResult(result)
                content['seed'] = input['seed']
            except:
                e = sys.exc_info()
            conn.close()
            nTryConnect += 1
        if nTryConnect==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
        return Response(content)

class StratifiedBlockRandomizationView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    def post(self, request, format=None):
        """
        implements post method: assumes input is in json format
        """
        #ipdb.set_trace()
        #input = json.loads(request.body) # request.data is for form-submitted case
        input = validateInput(request.body, isStratified=True, isBlocked=True)
        if not input['valid']:
            return Response(input)
        #return Response(request.body)
        #return HttpResponse(request.body)
        content, nTryConnect = None, 0
        while content is None and nTryConnect<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                result = conn.r.StratifiedBlockRandomization(N=input['N'], K=input['K'],Alloratio=input['alloRatio'], blocksize=input['blockSize'], seed=input['seed'])
                content = parseRandomizationResult(result)
                content['seed'] = input['seed']
            except:
                e = sys.exc_info()
            conn.close()
            nTryConnect += 1
        if nTryConnect==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
            #ipdb.set_trace()
        return Response(content)

class MinimizationRandomizationView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    def post(self, request, format=None):
        """
        implements post method: assumes input is in json format
        """
        #input = json.loads(request.body) # request.data is for form-submitted case
        #ipdb.set_trace()
        # dict to R list get disordered and Bugged!
        # here input is too complicated, need try-catch
        try:
            input = validateInput(request.body, isStratified=False, isBlocked=False, required0=[ 'nlevel', 'alloRatio', 'markerNew' ])
            if not input['valid']:
                return Response(input)
        except:
            e = sys.exc_info()[0]
            input = {'valid': False, 'status': 'failure', 'message': 'Input invalid: error from parsing input (%s): %s' % (request.body, e)}                
            return Response(input)
        #return Response({'valid': True, 'status': 'failure', 'isDummy': True})
        #return Response(request.body)
        #return HttpResponse(request.body)
        # conn.r.markerNew = input['markerNew'] conn.eval('colnames(data.frame(markerNew))')
        #
        #ipdb.set_trace()
        content, result, nTry = None, None, 0
        while content is None and nTry<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                #ipdb.set_trace()
                result = conn.r.MinimizationRandomization(K=input['K'], nfactor=input['nfactor'], nlevel=input['nlevel'], Alloratio=input['alloRatio'], olddf=input['markerOld'], newdf=input['markerNew'], weight=input['weight'], seed=input['seed'])
                #return Response({'valid': True, 'status': 'success', 'isDummy': True})
                content = parseRandomizationResult(result)
                #ipdb.set_trace()
                content['seed'] = input['seed']
            except:
                e = sys.exc_info()[0]
            #ipdb.set_trace()
            conn.close()
            #print('try: %d' %(nTry))
            nTry = nTry+1
            #ipdb.set_trace()
        if nTry==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
            #ipdb.set_trace() 
        return Response(content)

class TestView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    #renderer_classes = (JSONRenderer, )
    # no such variable or function "rnorm" defined in Rserve
    def get(self, request, format=None):
        if 'N' in request.GET:
            N = request.GET.get('N')
        else: 
            N = 10
        #ipdb.set_trace()
        result, nTryConnect = None, 0
        while result is None and nTryConnect<3:
            try:
                conn = pyRserve.connect(host='localhost', port=PORT)
                result = conn.r.rnorm(N)
                content = {'N': N, 'result': result}
            except:
                e = sys.exc_info()[0]
            conn.close()
            nTryConnect += 1
        if nTryConnect==3:
            content = {'status': 'failure', 'error': 'error from computation engine (R): %s' % e}            
            #ipdb.set_trace()
        return Response(content)
