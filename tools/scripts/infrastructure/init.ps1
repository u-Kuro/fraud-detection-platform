#requires -Version 7.4
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

if ((Get-Item .).Name -ne "infrastructure") {
    Push-Location infrastructure
}
try {
    terraform init
} finally {
    Pop-Location
}