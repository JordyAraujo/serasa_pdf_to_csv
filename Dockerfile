FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY ./fileupload /app

RUN pip install -r requirements.txt