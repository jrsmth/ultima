FROM python:3.9-slim
WORKDIR /code
COPY src/app/requirements.txt /code
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /code
ENV PYTHONUNBUFFERED=0
ENV FLASK_ENV=prod
EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--chdir", "src/app", "app:app"]

# Question :: when is the sass build going to happen?