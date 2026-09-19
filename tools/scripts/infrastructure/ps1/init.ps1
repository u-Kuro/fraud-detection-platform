#requires -Version 7.4
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$location_pushed = $false
if ((Get-Item .).Name -ne "infrastructure") {
    Push-Location infrastructure
    $location_pushed = $true
}
try {
    terraform init
} finally {
    if ($location_pushed) {
        Pop-Location
    }
}