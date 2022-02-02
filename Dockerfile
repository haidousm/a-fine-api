FROM python:3.8-slim as builder
WORKDIR /src/app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim
WORKDIR /src/app
COPY --from=builder /src/app /usr/local
COPY . /src/app

EXPOSE 8000
ENTRYPOINT ["./gunicorn.sh"]
