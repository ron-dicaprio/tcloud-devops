# Dockerfile
from python:3.13.5-bookworm
COPY ./PyQuickBIApi.py  /
RUN pip3 install requests fastapi uvicorn uvloop httptools -i https://mirrors.aliyun.com/pypi/simple/ --root-user-action ignore
CMD ["python3","/PyQuickBIApi.py"]
