# scripts/cost-simulator.py
from prometheus_client import start_http_server, Gauge
import random, time

# Define two Gauges with a “resource” label
COST  = Gauge('cloudlens_resource_cost_dollars',   'Simulated resource cost in USD',  ['resource'])
USAGE = Gauge('cloudlens_resource_usage_percent',  'Simulated resource CPU usage %', ['resource'])

def simulate_metrics():
    resources = ['vm1', 'db1', 'storage1']
    while True:
        for r in resources:
            COST.labels(resource=r).set(random.uniform(0.5, 10.0))
            USAGE.labels(resource=r).set(random.uniform(10.0, 100.0))
        time.sleep(15)

if __name__ == '__main__':
    # Expose metrics at http://localhost:8000/metrics
    start_http_server(8000)
    print("🏷️  Serving metrics on http://0.0.0.0:8000/metrics")
    simulate_metrics()
