import subprocess
from uuid import uuid4

from fastapi import APIRouter, Request, Response

from fraud_detection_platform_shim.modules.configs.shell import ShellConfig
from fraud_detection_platform_shim.modules.environment.docker import docker_environment

router = APIRouter(prefix="/repos", tags=["act"])

@router.post(
    "/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches",
    status_code=204,
)
async def workflow_dispatch(
    owner: str,
    repo: str,
    workflow_file: str,
    request: Request
):
    data = await request.json() if await request.body() else {}
    inputs = data.get("inputs", {})

    container_name = f"act-{owner}-{repo}-{workflow_file}-{uuid4()}"
    arguments = ["workflow_dispatch", "-W", f".github/workflows/{workflow_file}"]
    for key, value in inputs.items():
        arguments += ["--input", f"{key}={value}"]

    subprocess.Popen(args=[
        ShellConfig.shell,
        ShellConfig.docker_run_script,
        docker_environment.ACT_IMAGE,
        container_name,
        *arguments
    ], cwd=".")

    return Response(status_code=204)