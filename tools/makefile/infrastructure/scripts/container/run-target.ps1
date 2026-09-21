param(
    [Parameter(Mandatory=$true, Position=0)][string]$IMAGE,
    [Parameter(Mandatory=$true, Position=1)][string]$MAKEFILE_TARGET
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$WORKING_DIRECTORY = "/app"

docker run --rm `
    --use-api-socket `
    --network "host" `
    --add-host "host.docker.internal:host-gateway" `
    --add-host "api.host.docker.internal:host-gateway" `
    --volume "${Env:ABSOLUTE_ROOT_DIRECTORY}:${WORKING_DIRECTORY}" `
    "${IMAGE}" `
    "make ${MAKEFILE_TARGET}"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }