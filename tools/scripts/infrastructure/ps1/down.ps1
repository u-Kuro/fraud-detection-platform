#requires -Version 7.4
param(
    [Parameter(Mandatory=$true, Position=0)][string]$SHELL_CMD,
    [Parameter(Mandatory=$true, Position=1)][string]$SCRIPT_EXTENSION,
    [Parameter(Mandatory=$true, Position=2)][string]$SCRIPT_FLAG,
    [Parameter(Mandatory=$true, Position=3)][string]$COMMAND_FLAG
)
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$location_pushed = $false
if ((Get-Item .).Name -ne "infrastructure") {
    Push-Location infrastructure
    $location_pushed = $true
}
try {
    $Env:TF_VAR_SHELL_CMD        = $SHELL_CMD
    $Env:TF_VAR_SCRIPT_EXTENSION = $SCRIPT_EXTENSION
    $Env:TF_VAR_SCRIPT_FLAG      = $SCRIPT_FLAG
    $Env:TF_VAR_COMMAND_FLAG     = $COMMAND_FLAG

    try {
        terraform state rm `
            -backup="terraform.tfstate.backup" `
            module.exports `
            module.kyverno `
            module.metallb `
            module.mlflow `
            module.traefik `
            module.postgres `
            2>$null
    } catch {}

    terraform destroy -auto-approve -parallelism=1 -refresh=false
} finally {
    if ($location_pushed) {
        Pop-Location
    }
}
