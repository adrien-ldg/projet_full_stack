from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette_exporter import PrometheusMiddleware, handle_metrics
from routers import router_film, router_cast, router_user, router_authentification, other_router
from models.database import engine, BaseSQL



async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.templates = templates

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

app.include_router(router_film.router)
app.include_router(router_cast.router)
app.include_router(router_user.router)
app.include_router(router_authentification.router)
app.include_router(other_router.router)
