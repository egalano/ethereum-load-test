#!/usr/bin/env python

from functools import wraps
import random
from time import time
from ethjsonrpc import EthJsonRpc
from locust import Locust, TaskSet, events, task


def geth_locust_task(f):
    '''
    Simple timing wrapper which fires off the necessary
    success and failure events for locust.
    '''
    @wraps(f)
    def wrapped(*args, **kwargs):
        start_time = time()
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            print('Exception in {}'.format(f.__name__))
            total_time = int((time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                exception=e)
            return False
        else:
            total_time = int((time() - start_time) * 1000)
            events.request_success.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                response_length=0)
        return result
    return wrapped


class EthLocust(Locust):
    '''
    This is the abstract Locust class which should be subclassed.
    It provides an Ethereum JSON-RPC client that can be used for
    requests that will be tracked in Locust's statistics.
    '''
    def __init__(self, *args, **kwargs):
        super(EthLocust, self).__init__(*args, **kwargs)
        server, port = self.host.split(':')
        self.client = EthJsonRpc(server, port)
        print("Generating list of target addresses...")
        self.addresses = self.get_target_address_list()

    def get_target_address_list(self, count=100):
        '''
        As part of the initialization, we build up a list of 1k addresses
        which will be the targets of the getBal call. We do it as part of the
        initialization so that we dont slow down the concurrent tests.
        '''
        addrs = []
        block = self.client.eth_getBlockByNumber()
        while len(addrs) < count:
            block = self.client.eth_getBlockByHash(block['parentHash'])
            if block['transactions'] is not None:
                addrs += [
                    t['to']
                    for t in block['transactions']
                    if t['to'] is not None
                ]
        # Use a set to dedupe commonly used addresses (coinbase, poloniex, etc)
        return list(set(addrs))


class EthUser(EthLocust):
    host = 'localhost:8545'
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):
        @geth_locust_task
        @task
        def get_balance(self):
            target_addr = random.choice(self.locust.addresses)
            bal = self.client.eth_getBalance(target_addr)
            return bal
