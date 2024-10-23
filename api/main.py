from fastapi import FastAPI, Depends
from starlette_exporter import PrometheusMiddleware, handle_metrics
from routers import router_film, router_cast, router_user, router_authentification
from models.database import engine, BaseSQL
from services.oauth2 import get_current_active_user
from shemas.shema import User


async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(router_film.router)
app.include_router(router_cast.router)
app.include_router(router_user.router)
app.include_router(router_authentification.router)


@app.get("/")
async def launch(current_user: User = Depends(get_current_active_user)):
    return {"app": "V1"}


