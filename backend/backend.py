from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/ebpf', methods=['GET'])
def get_ebpf_info():

    open_ports = []
    for conn in psutil.net_connections():
        if conn.status == psutil.CONN_LISTEN:
            open_ports.append(conn.laddr.port)

    running_processes = []
    for process in psutil.process_iter(['pid', 'name']):
        running_processes.append({
            'pid': process.info['pid'],
            'name': process.info['name']
        })

    data = {
        'open_ports': open_ports,
        'running_processes': running_processes
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
