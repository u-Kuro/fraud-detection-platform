#requires -Version 7.4
param(
    [Parameter(Mandatory=$true, Position=0)][string]$MAKEFILE_PHONY
)
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$WORKING_DIRECTORY = "/app"

Write-Host @"
docker run --rm ``
    --volume "${Env:ROOT_DIRECTORY}:${WORKING_DIRECTORY}" ``
    --volume "${Env:DOCKER_SOCK}:/var/run/docker.sock" ``
    "${Env:INFRASTRUCTURE_IMAGE}" ``
    "${MAKEFILE_PHONY}"
"@

docker run --rm `
    --volume "${Env:ROOT_DIRECTORY}:${WORKING_DIRECTORY}" `
    --volume "${Env:DOCKER_SOCK}:/var/run/docker.sock" `
    "${Env:INFRASTRUCTURE_IMAGE}" `
    "make ${MAKEFILE_PHONY}"