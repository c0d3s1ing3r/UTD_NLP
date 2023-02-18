# coding=utf-8
# Author: Werner and Karl Dill

import logging
import requests
import json




class RestEndpoint:

    def __init__(self, url: str, method: str, timeout=10):
        self.method = method.upper()
        self.url = url
        self.timeout = timeout
        self.data = {}
        self.headers = {
            'Accept'        : 'application/json, text/javascript, */*',
            'User-Agent'    : 'Mozilla/5.0',
            'Content-Type'  : 'application/json'
        }
        # set log level to critical to suppress requests logging
        self.LOG = logging.getLogger(__name__)
        self.LOG.setLevel(logging.CRITICAL)
    
    def call(self) -> requests.Response:

        if self.method == 'POST':
            r = requests.post(self.url, data=json.dumps(self.data), headers=self.headers, timeout=self.timeout)
        elif self.method == 'GET':
            r = requests.get(self.url, data=json.dumps(self.data), headers=self.headers, timeout=self.timeout)
        else:
            logging.warning('Unsupported method {} called'.format(self.method))
        
        
        self.LOG.info('Request headers:')
        self.LOG.info(r.request.headers)
        self.LOG.info('Request data:')
        self.LOG.info(r.request.body)
        self.LOG.info('Response headers:')
        self.LOG.info(r.headers)
        self.LOG.info('----------------------------------------------------------------------------')
        self.LOG.info(r.text)
        return r
    
    def send(self):
        '''Just maps to call() method'''
        return self.call()
    
    def hit(self):
        # why are you hitting yourself?
        return self.call()