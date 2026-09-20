#requires -Version 7.4
param(
    [Parameter(Mandatory=$true, Position=0)][string]$MAKEFILE_PHONY
)
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$WORKING_DIRECTORY = "/app"

docker run --rm `
    --network "host" `
    --add-host "host.docker.internal:host-gateway" `
    --add-host "api.host.docker.internal:host-gateway" `
    --volume "${Env:ROOT_DIRECTORY}:${WORKING_DIRECTORY}" `
    --volume "${Env:DOCKER_SOCK}:/var/run/docker.sock" `
    "${Env:INFRASTRUCTURE_IMAGE}" `
    "make ${MAKEFILE_PHONY}"