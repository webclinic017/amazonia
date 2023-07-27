#!/bin/bash

DURATION_MINUTES=10

while true; do
    python3 metrics_ebpf.py
    sleep $((DURATION_MINUTES * 60))
done
