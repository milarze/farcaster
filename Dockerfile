FROM python:3.7

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./src /app/src
COPY ./farcaster /app
RUN chmod +x ./farcaster

ENTRYPOINT ["/app/farcaster"]