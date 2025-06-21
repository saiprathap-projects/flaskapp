FROM ubuntu:latest

RUN  apt update -y && apt install python3 python3-pip python3-venv python3-prometheus_client -y && \
     apt install gunicorn3 -y 
COPY requirements.txt requirements.txt

COPY flaskapp /opt/flaskapp

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN apt install python3-flask -y && apt install python3-requests -y

WORKDIR /opt/flaskapp

CMD [ "gunicorn3","-b","0.0.0.0:8000","app:app","--workers=5" ]
