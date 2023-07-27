FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y bpfcc-tools python3-bpfcc

WORKDIR /app

COPY metrics_ebpf.py .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
