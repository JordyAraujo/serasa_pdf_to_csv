FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./fileupload /app

RUN pip install -r requirements.txt