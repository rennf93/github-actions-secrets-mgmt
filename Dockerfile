FROM python:3.11-alpine3.18

WORKDIR /usr/src/app

# ENV OWNER
# ENV REPOSITORY
# ENV ACCESS_TOKEN
# ENV SECRET_NAME
# ENV SECRET_VALUE

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.pip ./requirements.pip
RUN pip install --upgrade pip && \
    pip install -r requirements.pip

COPY ./run.py ./run.py

ENTRYPOINT ["/usr/local/bin/python", "/usr/src/app/run.py"]