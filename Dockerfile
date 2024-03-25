FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /usr/src/app/
EXPOSE 80
CMD ["uwsgi", "--http", ":8000", "--module", "PeerGrader.wsgi", "--master", "--processes", "4", "--threads", "2"]
