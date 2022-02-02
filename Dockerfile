FROM python:3.8-slim
WORKDIR /src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["./gunicorn.sh"]
EXPOSE 8000
