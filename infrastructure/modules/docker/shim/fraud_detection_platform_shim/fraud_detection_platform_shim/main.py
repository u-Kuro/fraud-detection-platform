from contextlib import asynccontextmanager

from fastapi import FastAPI
from fraud_detection_platform_shim.controllers.routers import act

@asynccontextmanager
async def lifespan(_):
    yield

app = FastAPI(
    title="fraud_detection_platform_shim",
    lifespan=lifespan
)

# Routers
app.include_router(act.router)