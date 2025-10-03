from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 0)

    # Load telemetry file (place in repo root as telemetry.json)
    with open("telemetry.json", "r") as f:
        telemetry = json.load(f)

    result = {}
    for region in regions:
        if region not in telemetry:
            continue
        latencies = np.array([rec["latency_ms"] for rec in telemetry[region]])
        uptimes = np.array([rec["uptime"] for rec in telemetry[region]])

        breaches = int(np.sum(latencies > threshold))
        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))
        avg_uptime = float(np.mean(uptimes))

        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches,
        }

    return result
