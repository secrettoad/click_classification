FROM python:3.7
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN chmod +x gunicorn_entrypoint.sh
ENTRYPOINT ["./gunicorn_entrypoint.sh"]