from flask import Flask, jsonify, request
from bcc import BPF

app = Flask(__name__)

bpf_code = """
BPF_PROGRAM
"""

bpf = BPF(text=bpf_code)

@app.route('/ebpf')
def get_ebpf_info():

    data = {
        "name": "My eBPF Module",
        "description": "This is a sample eBPF module.",
        "metrics": {
            "metric1": "value1",
            "metric2": "value2",
            # Adicione outras métricas aqui
        }
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
