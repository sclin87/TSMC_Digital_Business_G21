FROM python:3.6.15-slim
COPY . /work
WORKDIR /work
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
CMD ["python","./URL_Gen.py"]