param(
    [Parameter(Mandatory=$true, Position=0)][string]$IMAGE_NAME,
    [Parameter(Mandatory=$true, Position=1)][string]$RUNNER_CONTAINER_NAME,
    [Parameter(Mandatory=$true, Position=2)][string]$COMMAND
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$WORKING_DIRECTORY = "/app"

docker run -it --init --rm --name "${RUNNER_CONTAINER_NAME}" `
    --use-api-socket `
    --network "host" `
    --add-host "host.docker.internal:host-gateway" `
    --add-host "api.host.docker.internal:host-gateway" `
    --volume "${Env:ABSOLUTE_ROOT_DIRECTORY}:${WORKING_DIRECTORY}" `
    --env RUNNER_CONTAINER_NAME="${RUNNER_CONTAINER_NAME}" `
    "${IMAGE_NAME}" `
    "${COMMAND}"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }