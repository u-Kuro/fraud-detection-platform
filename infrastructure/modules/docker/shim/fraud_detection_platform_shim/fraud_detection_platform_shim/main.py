from contextlib import asynccontextmanager

from fastapi import FastAPI
from fraud_detection_platform_shim.controllers.routers import act
from fraud_detection_platform_shim.services.slack import start_socket_mode

@asynccontextmanager
async def lifespan(_):
    start_socket_mode()

    yield

app = FastAPI(
    title="fraud_detection_platform_shim",
    lifespan=lifespan
)

# Routers
app.include_router(act.router)