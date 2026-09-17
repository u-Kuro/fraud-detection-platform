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
        -backup="terraform.tfstate.backup" `
        module.exports `
        module.metallb `
        module.kyverno `
        module.metallb `
        module.mlflow `
        module.traefik `
        module.postgres `
        2> $null
    } catch {}

    terraform destroy -auto-approve -parallelism=1 -refresh=false
} finally {
    Pop-Location
}
