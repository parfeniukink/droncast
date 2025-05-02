FROM python:3.12-slim

ARG PIPENV_EXTRAS=${PIPENV_EXTRAS}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000"


RUN : \
    && apt-get update -y \
    # dependencies for building Python packages && cleaning up unused files
    && apt-get install -y build-essential libcurl4-openssl-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN : \
    && pip install --upgrade pip setuptools \
    && pip install pipenv 

# Copy the dependencies file to the working directory
COPY Pipfile* ./
RUN pipenv sync ${PIPENV_EXTRAS} --system  && rm Pipfile*


# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /code
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn src.config.wsgi:application"]
