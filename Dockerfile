FROM python:3.10-alpine

# Install ffmpeg
RUN apk update && \
    apk add --upgrade ffmpeg && \
    rm -rf /var/cache/apk/*

WORKDIR app
RUN /usr/local/bin/python -m pip install --upgrade pip

ADD *.py ./
RUN /usr/local/bin/python -m pip install -e .

CMD ["python","app.py"]
