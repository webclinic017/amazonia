# Arquivo: metrics_ebpf.py
from bcc import BPF
from time import sleep

bpf_code = """
#include <linux/bpf.h>
#include <linux/ptrace.h>
#include <linux/sched.h>
#include <linux/net.h>
#include <uapi/linux/ptrace.h>

struct data_t {
    u64 pid;
    char comm[TASK_COMM_LEN];
    u64 cpu_usage;
    u64 memory_usage;
    u64 rx_bytes;
    u64 tx_bytes;
    u32 local_port;
};

BPF_PERF_OUTPUT(events);

int monitor_process(struct pt_regs *ctx) {
    struct data_t data = {};

    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    data.pid = task->tgid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    data.cpu_usage = bpf_ktime_get_ns();
    data.memory_usage = task->mm ? task->mm->total_vm << (PAGE_SHIFT - 10) : 0;

    struct sk_buff *skb = (struct sk_buff *)PT_REGS_PARM2(ctx);
    struct iphdr *ip = bpf_hdr_pointer(skb, 0);
    data.rx_bytes = ip ? skb->len : 0;

    struct tcphdr *tcp = (struct tcphdr *)(ip + 1);
    data.tx_bytes = tcp ? skb->len - (ip->ihl << 2) - (tcp->doff << 2) : 0;
    data.local_port = tcp ? ntohs(tcp->source) : 0;

    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""

bpf = BPF(text=bpf_code)
bpf.attach_kprobe(event="finish_task_switch", fn_name="monitor_process")

# Infinite loop to keep the eBPF program running
try:
    while True:
        bpf.perf_buffer_poll()
except KeyboardInterrupt:
    pass
