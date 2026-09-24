import math
import os
import sys

def read_cgroup_v2_cpu_limit() -> float | None:
    """
    cgroups v2  →  /sys/fs/cgroup/cpu.max
    Format: "<quota_us> <period_us>"  or  "max <period_us>"
    Used by: Docker ≥ 20.10 (cgroupns=private), Kubernetes (cgroup v2 nodes).
    """
    try:
        with open("/sys/fs/cgroup/cpu.max") as cpu_max_file:
            quota_string, period_string = cpu_max_file.read().strip().split()
        if quota_string == "max":
            return None
        return int(quota_string) / int(period_string)
    except Exception:
        return None

def read_cgroup_v1_cpu_limit() -> float | None:
    """
    cgroups v1  →  /sys/fs/cgroup/cpu/cpu.cfs_quota_us
    -1 means "unlimited".
    Used by: older Docker / LXC / Kubernetes (cgroup v1 nodes).
    """
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
    """
    CPU affinity mask  →  os.sched_getaffinity(0)
    Reflects cpuset restrictions from taskset, numactl, or the
    container runtime.  Available on Linux and some BSDs.
    """
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return None

def get_safe_cpu_count() -> int:
    """
    Return a safe value for ``n_jobs`` in ML packages (scikit-learn,
    joblib, XGBoost, LightGBM, etc.) that avoids hangs, deadlocks, and
    resource starvation across all environments:
    Docker · Kubernetes · bare Linux · macOS · Windows · VMs.

    Detection order — first hit wins:
      1. cgroups v2 quota       /sys/fs/cgroup/cpu.max
      2. cgroups v1 quota       /sys/fs/cgroup/cpu/cpu.cfs_quota_us
      3. CPU affinity mask      os.sched_getaffinity(0)   [Linux / BSD]
      4. os.cpu_count() × 0.75  universal fallback with safety margin

    Always returns at least 1.
    """

    # ── 1 & 2. cgroup CPU quota (Docker / Kubernetes on Linux) ──────────
    if sys.platform.startswith("linux"):
        for cgroup_limit_reader in (read_cgroup_v2_cpu_limit, read_cgroup_v1_cpu_limit):
            detected_cpu_quota = cgroup_limit_reader()
            if detected_cpu_quota is not None:
                return max(1, math.floor(detected_cpu_quota))

    # ── 3. CPU affinity mask (Linux / some BSDs) ─────────────────────────
    detected_affinity_count = read_cpu_affinity_count()
    if detected_affinity_count:
        return max(1, detected_affinity_count)

    # ── 4. Logical CPU count with a 75 % safety margin ───────────────────
    # Fallback for Windows, macOS, and Linux without cgroup / affinity info.
    total_logical_cpu_count = os.cpu_count() or 1
    return max(1, math.floor(total_logical_cpu_count * 0.75))