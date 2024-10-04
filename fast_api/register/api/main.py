import base64
from fastapi import FastAPI, Request, Header, HTTPException
from .models.database import BaseSQL, engine

from .routers import router
from typing import Optional
import json
from fastapi.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics




async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(router)

@app.get("/")
async def hello():
    return {"hello": "world"}


@app.get("/api/headers")
def read_hello(request: Request, x_userinfo: Optional[str] = Header(None, convert_underscores=True), ):
    try:
        print(request["headers"])
        return {"Headers": json.loads(base64.b64decode(x_userinfo))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))