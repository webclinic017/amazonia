import time
from bcc import BPF
from bcc.utils import printb


def process_event(cpu, data, size):

def ports_event(cpu, data, size):

b = BPF(text=ebpf_code_processes)
b.attach_kprobe(event=b.get_syscall_fnname("execve"), fn_name="trace_process")

b_ports = BPF(text=ebpf_code_ports)
b_ports.attach_kprobe(event=b_ports.get_syscall_fnname("sys_connect"), fn_name="trace_socket")

def monitor_processes_and_ports(duration_minutes):
    iterations = 0
    duration_seconds = duration_minutes * 60

    print("%-6s %-16s %-6s" % ("PID", "COMMAND", "TGID"))
    b["events"].open_perf_buffer(process_event)
    
    print("\nPortas em uso:")
    print("%-6s %-6s %-6s" % ("PID", "DPORT", "RET"))
    b_ports["events"].open_perf_buffer(ports_event)

    while True:
        try:
            b.perf_buffer_poll()
            b_ports.perf_buffer_poll()

            iterations += 1
            if iterations * 10 >= duration_seconds:
                break
            
            time.sleep(10)  

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    monitor_processes_and_ports(duration_minutes=10)
