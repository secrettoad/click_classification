FROM python:3.7
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
RUN chmod +x run_pipeline.sh
ENTRYPOINT ["./run_pipeline.sh"]