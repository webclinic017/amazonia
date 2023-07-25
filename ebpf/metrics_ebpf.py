<!-- Arquivo: index.html -->
<html>
<head>
    <title>Server Metrics</title>
</head>
<body>
    <h1>Server Metrics</h1>
    <button onclick="fetchMetrics()">Fetch Metrics</button>
    <ul id="metricsList"></ul>

    <script>
        async function fetchMetrics() {
            try {
                const response = await fetch('/metrics');
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                const metricsData = await response.json();
                displayMetrics(metricsData);
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        function displayMetrics(metricsData) {
            const metricsList = document.getElementById('metricsList');
            metricsList.innerHTML = '';

            for (const metric of metricsData) {
                const cpuUsage = (metric.cpu_usage / 1e6).toFixed(2); // Convert ns to ms
                const memoryUsage = (metric.memory_usage / (1024 * 1024)).toFixed(2); // Convert bytes to MB
                const rxBytes = metric.rx_bytes;
                const txBytes = metric.tx_bytes;
                const localPorts = Array.from(metric.local_ports).join(', ');

                const metricInfo = document.createElement('li');
                metricInfo.textContent = `Process ${metric.comm} (PID ${metric.pid}): CPU Usage: ${cpuUsage} ms, Memory Usage: ${memoryUsage} MB, Rx Bytes: ${rxBytes}, Tx Bytes: ${txBytes}, Local Ports: ${localPorts}`;
                metricsList.appendChild(metricInfo);
            }
        }
    </script>
</body>
</html>
