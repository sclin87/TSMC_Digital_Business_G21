FROM python:3.6.15-slim
COPY . /app
WORKDIR /app
RUN pip install flask
CMD ["python","-u","flask_server.py"]