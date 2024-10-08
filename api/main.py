from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics




app = FastAPI()


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.get("/")
async def hello():
    return {"hello": "world"}