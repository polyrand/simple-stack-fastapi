FROM python:3.7.7-slim-buster

# run apt-get update/upgrade without caching and bloat
# source: https://pythonspeed.com/articles/system-packages-docker/
# hadolint ignore=DL3013
# RUN pip install --upgrade pip setuptools wheel && pip install -r main.txt && rm -rf /root/.cache/pip
# Now EVERYTHING is installed in the script below, including pip.
COPY ./requirements/main.txt .
RUN "pip install --no-cache-dir -r main.txt && && rm -rf /root/.cache/pip"


# moving to non-root: https://pythonspeed.com/articles/root-capabilities-docker-security/
# https://pythonspeed.com/articles/dockerizing-python-is-hard/
RUN addgroup --gid 1024 appgroup
RUN useradd --create-home --gid 1024 appuser
WORKDIR /home/appuser

# activate non-root user
USER appuser


COPY --chown=appuser:appgroup gunicorn_conf.py .

RUN mkdir /home/appuser/app

COPY --chown=appuser:appgroup ./main.py .


ENV PYTHONPATH=/home/appuser
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
# There is a command override in the file docker-compose.dev.command.yml
# that runs /start-reload.sh (included in the base image) instead of the default /start.sh
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "main:app"]
