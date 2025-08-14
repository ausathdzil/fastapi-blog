FROM python:3.10-slim

WORKDIR /fastapi-blog

COPY ./requirements.txt /fastapi-blog/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fastapi-blog/requirements.txt

COPY ./app /fastapi-blog/app

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
