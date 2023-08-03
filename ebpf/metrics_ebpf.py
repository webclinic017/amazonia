from bcc import BPF
import socket

# Endereço e porta do backend para onde as métricas serão enviadas
BACKEND_HOST = "localhost"
BACKEND_PORT = 8080

bpf_code_processes = """
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

int trace_process(struct pt_regs *ctx) {
    // Implemente o código para monitorar processos e coletar os dados relevantes
    // Exemplo:
    struct data_t data = {};
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    data.pid = task->tgid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    data.cpu_usage = bpf_ktime_get_ns();
    data.memory_usage = task->mm ? task->mm->total_vm << (PAGE_SHIFT - 10) : 0;

    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""

bpf_code_ports = """
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <uapi/linux/ptrace.h>

struct data_t {
    u64 pid;
    u16 dport;
    int ret;
};

BPF_PERF_OUTPUT(events);

int trace_socket(struct pt_regs *ctx, struct socket *sock) {
    // Implemente o código para monitorar portas e coletar os dados relevantes
    // Exemplo:
    struct data_t data = {};
    data.pid = bpf_get_current_pid_tgid();

    struct sockaddr_in *addr = (struct sockaddr_in *)PT_REGS_PARM2(ctx);
    data.dport = addr->sin_port;
    
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}
"""

def process_event(cpu, data, size):
    # Processa o evento e coleta os dados
    event = b["events"].event(data)
    # ... (seu código para coletar os dados relevantes) ...

    # Envia os dados coletados para o backend via socket
    message = f"{data.pid},{data.comm},{data.cpu_usage},{data.memory_usage},{data.rx_bytes},{data.tx_bytes},{data.local_port}\n"
    sock.sendall(message.encode())

def ports_event(cpu, data, size):
    # Processa o evento e coleta os dados
    event = b_ports["events"].event(data)
    # ... (seu código para coletar os dados relevantes) ...

    # Envia os dados coletados para o backend via socket
    message = f"{data.pid},{data.dport},{data.ret}\n"
    sock.sendall(message.encode())

b = BPF(text=bpf_code_processes)
b.attach_kprobe(event=b.get_syscall_fnname("execve"), fn_name="trace_process")

b_ports = BPF(text=bpf_code_ports)
b_ports.attach_kprobe(event=b_ports.get_syscall_fnname("sys_connect"), fn_name="trace_socket")

# Cria o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao backend
server_address = (BACKEND_HOST, BACKEND_PORT)
sock.connect(server_address)

# Infinite loop para manter o programa eBPF em execução
try:
    while True:
        b.perf_buffer_poll()
        b_ports.perf_buffer_poll()

except KeyboardInterrupt:
    pass

finally:
    # Fecha o socket ao sair do loop
    sock.close()
