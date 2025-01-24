FROM python:3.10.16-alpine AS builder
ARG REQUIREMENTS_FILE=requirements.txt

WORKDIR  /app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

COPY ${REQUIREMENTS_FILE} .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${REQUIREMENTS_FILE}

FROM python:3.10.16-alpine AS stage

RUN mkdir /app 

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERD 1

WORKDIR /app 

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

COPY --from=builder /usr/src/app/wheels /wheels/ 

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && \
    rm -rf /wheels/ 

COPY . .

EXPOSE 8000

CMD /app/bin/entrypoint.sh