Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (-not $Env:ABSOLUTE_ROOT_DIRECTORY) { throw "ABSOLUTE_ROOT_DIRECTORY environment is not set" }

try {
    Set-Location -LiteralPath "${Env:ABSOLUTE_ROOT_DIRECTORY}/database"

    atlas migrate hash
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Set-Location -LiteralPath $Env:ABSOLUTE_ROOT_DIRECTORY
}