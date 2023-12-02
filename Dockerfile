FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "application.py"]