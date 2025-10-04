# api/index.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from scipy.stats import scoreatpercentile

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/api/latency")
async def latency_metrics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 180)

    # Load telemetry CSV (you must have uploaded this to your project)
    telemetry = pd.read_csv("telemetry.csv")

    result = {}
    for region in regions:
        df = telemetry[telemetry["region"] == region]
        if df.empty:
            continue
        avg_latency = df["latency_ms"].mean()
        p95_latency = np.percentile(df["latency_ms"], 95)
        avg_uptime = df["uptime"].mean()
        breaches = (df["latency_ms"] > threshold).sum()
        result[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": int(breaches),
        }

    return result
