## ethereum-load-test
Locust.io(https://locust.io) based load test for Ethereum JSON-RPC servers.

The current version of this test will make ethGetBalance requests against the
target JSON-RPC server.

## Quickstart with Docker
Build the docker image
```
docker build -t ethereum-load-test .
```
Run the docker container
```
docker run -e RPC_HOST=YOUR_RPC_SERVER:YOUR_RPC_PORT -p 8089:8089 ethereum-load-test
```

## Quickstart with virtualenv (Python2)
```
virtualenv venv-ethereum-load-test
. venv-ethereum-load-test/bin/activate
pip install -r requirements.txt
locust
```

## How to run a load test from a Web Browser
Access the Locust Web UI
```
http://localhost:8089 # Replace localhost with your DOCKER_HOST address
```
Enter the desired number of clients and spawn rate.

## How to run a load test from the command line
```
locust --host YOUR_RPC_SERVER:YOUR_RPC_PORT --print-stats --clients 100 --hatch-rate 2 --no-web
```
