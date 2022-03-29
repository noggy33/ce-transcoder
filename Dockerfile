FROM python:3.10.3-alpine3.15

# Install ffmpeg
RUN apk update && \
    apk add --upgrade ffmpeg && \
    rm -rf /var/cache/apk/*

WORKDIR app
RUN /usr/local/bin/python -m pip install --upgrade pip

ADD *.py ./
RUN /usr/local/bin/python -m pip install -e .

CMD ["python","app.py"]