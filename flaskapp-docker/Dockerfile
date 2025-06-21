FROM ubuntu:latest

RUN apt update -y
RUN apt install python3 -y
RUN apt install python3-pip -y 
RUN apt install gunicorn3 -y
RUN apt install python3-venv -y

COPY requirements.txt requirements.txt

COPY flaskapp /opt/flaskapp

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install prometheus_client
RUN apt install python3-flask -y
RUN apt install python3-requests -y

WORKDIR /opt/flaskapp

CMD [ "gunicorn3","-b","0.0.0.0:8000","app:app","--workers=5" ]
