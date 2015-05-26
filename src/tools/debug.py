from pysrc import pydevd
import logging

def start():
    pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True, suspend=False)        
    logging.basicConfig(level=logging.DEBUG)