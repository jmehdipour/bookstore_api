FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY config.env /app/config.env
COPY ./app /app/app