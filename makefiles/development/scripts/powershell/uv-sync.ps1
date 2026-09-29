Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (-not $Env:ABSOLUTE_ROOT_DIRECTORY) { throw "ABSOLUTE_ROOT_DIRECTORY environment is not set" }

$paths = @(
    "dags"
    "infrastructure/modules/docker/shim/fraud_detection_platform_shim"
    "notebooks"
    "services"
)
try {
    foreach ($path in $paths) {
        Set-Location -LiteralPath "${Env:ABSOLUTE_ROOT_DIRECTORY}/${path}"

        uv sync --all-packages --all-groups
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
} finally {
    Set-Location -LiteralPath $Env:ABSOLUTE_ROOT_DIRECTORY
}