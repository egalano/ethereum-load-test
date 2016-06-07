#!/usr/bin/env python

from functools import wraps
import time
from ethjsonrpc import EthJsonRpc
from locust import Locust, TaskSet, task, events


def geth_locust_task(f):
    '''
    Simple timing wrapper which fires off the necessary
    success and failure events for locust.
    '''
    @wraps(f)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            raise
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="jsonrpc",
                name=f.__name__,
                response_time=total_time,
                response_length=0)
        return result
    return wrapped


class EthLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed.
    It provides an XML-RPC client that can be used to make XML-RPC
    requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(EthLocust, self).__init__(*args, **kwargs)
        server, port = self.host.split(':')
        self.client = EthJsonRpc(server, port)


class EthUser(EthLocust):
    host = 'geth-load-testing.infura.io:80'
    test_address = '0xea674fdde714fd979de3edf0f56aa9716b898ec8'
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):
        @geth_locust_task
        @task
        def get_balance(self):
            target_addr = test_address
            bal = self.client.eth_getBalance(target_addr)
            print(bal)
