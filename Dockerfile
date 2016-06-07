FROM python:2-onbuild
ENV RPC_HOST localhost:8545
EXPOSE 8089
CMD locust --host $RPC_HOST
