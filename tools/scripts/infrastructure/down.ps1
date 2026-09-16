#requires -Version 7.4
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

if ((Get-Item .).Name -ne "infrastructure") {
    Push-Location infrastructure
}
try {
    try {
        terraform state rm `
        -backup=terraform.tfstate.backup `
        module.postgres `
        module.metallb `
        module.mlflow `
        module.exports 2> $null
    } catch {}

    terraform destroy -auto-approve -parallelism=1
} finally {
    Pop-Location
}
