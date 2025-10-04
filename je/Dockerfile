FROM python:3.13.7-slim-bookworm

WORKDIR /je

RUN apt-get update && apt-get install -y --no-install-recommends \
        git make g++ pkg-config libcap-dev libseccomp-dev libsystemd-dev && \
    git clone https://github.com/ioi/isolate.git /tmp/isolate && \
    cd /tmp/isolate && make install && \
    rm -rf /tmp/isolate /var/lib/apt/lists/*

CMD ["bash"]
