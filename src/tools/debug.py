from pysrc import pydevd
import logging

def start():
    pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True, suspend=False)
    #pydevd.settrace('192.168.1.10', stdoutToServer=True, stderrToServer=True, suspend=False)
    #pydevd.settrace('192.168.1.10')        
    
    logging.basicConfig(level=logging.DEBUG)