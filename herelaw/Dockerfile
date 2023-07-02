# FROM python:3.9.16-bullseye AS builder

# WORKDIR /backend

# COPY . /backend

# RUN pip3 install pip --upgrade
# RUN pip3 install -r requirements.txt

# # 환경변수
# ENV FLASK_APP app.py
# ENV FLASK_RUN_PORT 443
# ENV FLASK_RUN_HOST 0.0.0.0

# EXPOSE 443

# # 구동 명령
# ENTRYPOINT ["flask", "run" ,"--cert=cert.pem", "--key=key.pem" ]


FROM python:3.9.16-bullseye AS builder

WORKDIR /backend

COPY . /backend

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt

# 환경변수
ENV FLASK_APP app.py
ENV FLASK_RUN_PORT 2222
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 2222

# 구동 명령
ENTRYPOINT ["flask", "run"]