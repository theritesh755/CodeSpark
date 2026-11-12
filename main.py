from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from database.postgres import init_db
from routes import trace_routes, graph_routes, risk_routes, security_routes, audit_routes, report_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Cybersecurity-driven blockchain transaction forensics API. Scores are heuristic leads, not proof of identity or criminality.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in (
    trace_routes.router, graph_routes.router, risk_routes.router,
    security_routes.router, audit_routes.router, report_routes.router,
):
    app.include_router(router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["system"])
def root():
    return {"service": settings.APP_NAME, "docs": "/docs", "mode": settings.DATA_MODE}

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "database": "configured", "mode": settings.DATA_MODE}
