#requires -Version 7.4
param(
    [Parameter(Mandatory=$true, Position=0)][string]$DOCKERFILE,
    [Parameter(Mandatory=$true, Position=0)][string]$IMAGE
)
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

docker build `
    --file "${DOCKERFILE}" `
    --tag "${IMAGE}" `
    "."