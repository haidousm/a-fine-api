FROM python:3.8-slim as builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim
WORKDIR /src/app
COPY --from=builder /opt/venv /opt/venv
COPY . /src/app

ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000

ENTRYPOINT ["./gunicorn.sh"]
