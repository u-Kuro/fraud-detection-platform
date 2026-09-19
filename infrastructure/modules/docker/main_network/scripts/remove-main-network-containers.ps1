#requires -Version 7.4
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$main_network_name = $Env:MAIN_NETWORK_NAME

$main_network_json_configurations = (docker inspect $main_network_name | ConvertFrom-Json)[0]
$main_network_containers          = $main_network_json_configurations.Containers

$exclude_containers = @("ministack", "traefik-http-proxy")
foreach ($container_properties in $main_network_containers.PSObject.Properties) {
    $container = $container_properties.Value
    if ($container.Name -in $exclude_containers) { continue }
    docker rm --force $container.Name
}