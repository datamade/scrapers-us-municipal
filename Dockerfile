FROM ubuntu:18.04 as builder

# Clone and build Blackbox
RUN apt-get update && apt-get install -y build-essential git-core && \
    git clone https://github.com/StackExchange/blackbox.git && \
    cd blackbox && \
    make copy-install

FROM python:3.6-slim-stretch
LABEL maintainer "DataMade <info@datamade.us>"

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libxml2-dev libxslt1-dev gdal-bin gnupg && \
    apt-get clean && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

# Copy Blackbox executables from builder stage
COPY --from=builder /usr/local/bin/blackbox* /usr/local/bin/
COPY --from=builder /usr/local/bin/_blackbox* /usr/local/bin/
COPY --from=builder /usr/local/bin/_stack_lib.sh /usr/local/bin/

ENTRYPOINT ["/app/docker-entrypoint.sh"]
