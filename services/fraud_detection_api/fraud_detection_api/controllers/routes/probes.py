from fastapi import Depends, APIRouter

from fraud_detection_api.modules.schemas.status import StatusResponse
from fraud_detection_api.services.dependencies import get_model, check_postgres, get_executor

router = APIRouter()

@router.get(path="/health", include_in_schema=False)
async def health(): return StatusResponse(status="ok")

@router.get(
    path="/ready",
    include_in_schema=False,
    dependencies=[
        Depends(get_executor),
        Depends(get_model),
        Depends(check_postgres),
    ]
)
def ready(): return StatusResponse(status="ok")
