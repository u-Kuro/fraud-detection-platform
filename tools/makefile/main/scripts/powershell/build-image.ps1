param(
    [Parameter(Mandatory=$true, Position=0)][string]$DOCKERFILE,
    [Parameter(Mandatory=$true, Position=0)][string]$IMAGE
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker build `
    --file "${DOCKERFILE}" `
    --tag "${IMAGE}" `
    "."
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }