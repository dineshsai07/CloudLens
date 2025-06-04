#!/usr/bin/env python3
"""
scripts/cleanup-detector.py

Queries Prometheus for CloudLens metrics and prints a cleanup plan:
 - Resources with usage < USAGE_THRESHOLD → recommend “scale down / shutdown”
 - Resources with cost > COST_THRESHOLD      → recommend “investigate cost spike”
"""

import sys
import requests

# Defaults: adjust as you like
PROM_URL         = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:9090"
USAGE_THRESHOLD  = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0    # percent
COST_THRESHOLD   = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0     # dollars

def query_prometheus(expr):
    resp = requests.get(f"{PROM_URL}/api/v1/query", params={"query": expr})
    resp.raise_for_status()
    return resp.json()["data"]["result"]

def main():
    print(f"🔍 Connecting to Prometheus at {PROM_URL}")
    # 1) Low-usage resources
    usage_expr = f'cloudlens_resource_usage_percent < {USAGE_THRESHOLD}'
    low_usage = query_prometheus(usage_expr)

    # 2) High-cost resources
    cost_expr  = f'cloudlens_resource_cost_dollars > {COST_THRESHOLD}'
    high_cost  = query_prometheus(cost_expr)

    if not low_usage and not high_cost:
        print("✅ No immediate cleanup actions detected.")
        return 0

    print("\n🛠️  Cleanup Plan:")
    for item in low_usage:
        res = item["metric"]["resource"]
        val = item["value"][1]
        print(f" • [{res}] usage {val}% < {USAGE_THRESHOLD}% → consider scale-down or shutdown")

    for item in high_cost:
        res = item["metric"]["resource"]
        val = item["value"][1]
        print(f" • [{res}] cost ${val} > ${COST_THRESHOLD} → investigate cost anomaly")

    return 1

if __name__ == "__main__":
    sys.exit(main())
