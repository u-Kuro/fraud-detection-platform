import subprocess
from functools import cache

@cache
def cuda_is_available() -> bool:
    try: return subprocess.run(["nvidia-smi", "-L"], capture_output=True, timeout=10).returncode == 0
    except: return False