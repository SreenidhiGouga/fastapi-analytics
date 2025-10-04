from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/latency")   # 👈 this is the route you want
async def latency(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    with open("telemetry.json", "r") as f:
        telemetry = json.load(f)

    results = {}
    for region in regions:
        region_data = telemetry.get(region, [])
        if not region_data:
            continue

        latencies = [rec["latency_ms"] for rec in region_data]
        uptimes = [rec["uptime"] for rec in region_data]

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))
        breaches = int(np.sum(np.array(latencies) > threshold))

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return results
