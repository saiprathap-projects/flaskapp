FROM ubuntu:latest

RUN  apt update -y && apt install -y \
     python3 \
     python3-pip \
     python3-venv \
     && rm -rf /var/lib/apt/lists/*
     
COPY requirements.txt requirements.txt

COPY flaskapp /opt/flaskapp

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install prometheus_client
RUN pip install flask requests
RUN pip install gunicorn

WORKDIR /opt/flaskapp

CMD [ "/venv/bin/gunicorn","-b","0.0.0.0:8000","app:app","--workers=5" ]
