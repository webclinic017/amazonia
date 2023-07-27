#!/bin/bash

bpftool prog load /app/metrics_ebpf.py /app/metrics_ebpf.o

bpftool cgroup attach /app/metrics_ebpf.o /sys/fs/cgroup/unified/ # Exemplo de anexar a cgroups

tail -f /dev/null
