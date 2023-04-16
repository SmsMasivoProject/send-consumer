# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV SMS_HOST_USER=10.90.13.170
ENV SMS_HOST_PORT=18013
ENV SMS_HOST_SYSTEM_ID=applista
ENV SMS_HOST_PASSWORD=Lista*21
ENV RABBIT_CREDENTIALS_USER=guest
ENV RABBIT_CREDENTIALS_PASSWORD=guest
ENV RABBIT_CREDENTIALS_HOST=rabbitmq
ENV RABBIT_CREDENTIALS_PORT=5672

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "consumer.py"]
