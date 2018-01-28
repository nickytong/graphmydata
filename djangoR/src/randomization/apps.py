from django.apps import AppConfig
import io, os, json, subprocess
import pyRserve
import platform
# script here only run once
class RandomizationConfig(AppConfig):
    name = 'randomization'
    def ready(self, port=6000):
        # 1) somehow open Rserve fails in Django, succeeded in Python
        # cmd = "R CMD Rserve --RS-port %d" % (6000)
        # command_list = cmd.split()
        # p = subprocess.Popen(command_list) 
        # 2) source core code
        conn = pyRserve.connect(host='localhost', port=port)
        conn.eval('options(encoding = "utf-8")')
        if platform.system()=='Linux':
            file = 'randomization/assets/randomizeFunction.R'
        else:
            file = 'randomization\\assets\\randomizeFunction.R'
        with io.open(file, 'r', encoding='utf8') as f:
            src=f.read()
        conn.eval(src)
        conn.close() # windows only allow one connection for a given port; linux is ok for multiple

