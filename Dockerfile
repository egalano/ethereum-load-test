FROM python:3-onbuild
ENV RPC_HOST "geth-load-testing.infura.io"
ENV RPC_PORT 80
CMD [ "locust", "--host", "${RPC_HOST}:${RPC_PORT}" ]
