FROM python:3.10-slim-buster
USER root
RUN pip install -U pip
RUN pip install websocket_server PyYAML

COPY ./src /src
CMD ["python3", "/src/chatroom.py"]
