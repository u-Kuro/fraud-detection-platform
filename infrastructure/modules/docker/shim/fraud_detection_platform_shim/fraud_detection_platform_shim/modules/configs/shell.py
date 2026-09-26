from dataclasses import dataclass

from fraud_detection_platform_shim.modules.environment.docker import docker_environment

@dataclass(frozen=True)
class ShellConfig:
    shell: str = "/bin/bash"
    docker_run_script: str = f"{docker_environment.SCRIPT_DIRECTORY}/docker-run.sh"