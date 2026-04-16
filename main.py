"""Auto-generated Chain Executor for Customer_Pipeline."""
import asyncio
import httpx
from fastapi import FastAPI

app = FastAPI(title="Customer_Pipeline")

TOKEN = ""
AGENTS = [
    {"id": "node-91a1fd8c", "agent_id": "6af174ec-9ccb-40e9-b678-1e17249ffd9f", "endpoint": "", "timeout": 30},
    {"id": "node-853ecf0d", "agent_id": "ab1d1617-a20c-4764-b3cf-3b643e917aa5", "endpoint": "", "timeout": 30},
    {"id": "node-c68d1270", "agent_id": "f019e7c3-3552-4d37-8da4-24647c81b3d0", "endpoint": "", "timeout": 30},
]

EDGES = [
    {"id": "", "source": "node-91a1fd8c", "target": "node-853ecf0d", "transform": "passthrough"},
    {"id": "", "source": "node-853ecf0d", "target": "node-c68d1270", "transform": "passthrough"},
]


async def call_agent(endpoint: str, input_data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(endpoint, json={"input": input_data}, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=300)
        resp.raise_for_status()
        return resp.json()


@app.post("/invoke")
async def invoke(input: dict):
    current = input.get("input", input)
    trace = []
    for agent in AGENTS:
        try:
            result = await call_agent(agent["endpoint"], current)
            trace.append({"agent": agent["id"], "status": "completed", "output": result})
            current = result.get("output", result)
        except Exception as e:
            trace.append({"agent": agent["id"], "status": "failed", "error": str(e)})
    return {"output": current, "trace": trace, "status": "completed"}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "chain_executor", "agents": len(AGENTS)}