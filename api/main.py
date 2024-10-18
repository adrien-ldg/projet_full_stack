from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from routers import router_film, router_cast
from models.database import engine, BaseSQL


async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(router_film.router)
app.include_router(router_cast.router)


@app.get("/")
async def launch():
    return {"app": "V1"}