FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Установка netcat
RUN apt-get update && apt-get install -y netcat-openbsd

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=djangoProject.settings

EXPOSE 7000

RUN chmod a+x /app/docker/*.sh

CMD ["/app/docker/startup.sh"]
