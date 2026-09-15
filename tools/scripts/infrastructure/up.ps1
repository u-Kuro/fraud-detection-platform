#requires -Version 7.4
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

if ((Get-Item .).Name -ne "infrastructure") {
    Push-Location infrastructure
}
try {
    terraform apply `
        -target="module.ministack_container.docker_container.ministack" `
        -auto-approve `
        -parallelism=1

    terraform apply `
        -target="module.eks.data.external.k3s_configuration" `
        -auto-approve `
        -parallelism=1

    terraform apply -auto-approve -parallelism=1
} finally {
    Pop-Location
}