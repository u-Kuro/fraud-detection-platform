import math
import os
import sys

def read_cgroup_v2_cpu_limit() -> float | None:
    # Docker ≥ 20.10 (cgroupns=private), Kubernetes (cgroup v2 nodes).
    try:
        with open("/sys/fs/cgroup/cpu.max") as cpu_max_file:
            quota_string, period_string = cpu_max_file.read().strip().split()
        if quota_string == "max":
            return None
        return int(quota_string) / int(period_string)
    except Exception:
        return None

def read_cgroup_v1_cpu_limit() -> float | None:
    # Older Docker / LXC / Kubernetes (cgroup v1 nodes).
    try:
        with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us") as quota_file:
            quota_microseconds = int(quota_file.read().strip())
        if quota_microseconds <= 0:
            return None
        with open("/sys/fs/cgroup/cpu/cpu.cfs_period_us") as period_file:
            period_microseconds = int(period_file.read().strip())
        return quota_microseconds / period_microseconds if period_microseconds > 0 else None
    except Exception:
        return None

def read_cpu_affinity_count() -> int | None:
    # Linux and some BSDs.
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return None

def get_safe_cpu_count() -> int:
    # cgroup CPU quota (Docker / Kubernetes on Linux)
    if sys.platform.startswith("linux"):
        for cgroup_limit_reader in (read_cgroup_v2_cpu_limit, read_cgroup_v1_cpu_limit):
            detected_cpu_quota = cgroup_limit_reader()
            if detected_cpu_quota is not None:
                return max(1, math.floor(detected_cpu_quota))

    # CPU affinity mask (Linux / some BSDs)
    detected_affinity_count = read_cpu_affinity_count()
    if detected_affinity_count:
        return max(1, detected_affinity_count)

    # Fallback to logical CPU count with a 75 % safety margin
    total_logical_cpu_count = os.cpu_count() or 1
    return max(1, math.floor(total_logical_cpu_count * 0.75))