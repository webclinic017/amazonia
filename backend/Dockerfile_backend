FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y bpfcc-tools python3-bpfcc

WORKDIR /app

COPY backend.py .
COPY requirements.txt .

RUN apt-get install -y python3-pip && \
    pip3 install -r requirements.txt

COPY ebpf/metrics_ebpf.py /app/metrics_ebpf.py

COPY ebpf/entrypoint.sh /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

CMD ["/app/backend/entrypoint.sh"]
