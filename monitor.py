import platform
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

DEVICES = {
    "Google DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1",
}


def check_device(name: str, ip: str) -> dict:
    """Ping a device once and return a structured result."""
    flag = "-n" if platform.system() == "Windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", flag, "1", ip],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        reachable = result.returncode == 0
        # Matches time=12.3 ms, time<1ms and time=12.3ms.
        match = re.search(r"time\s*[=<]\s*([\d.]+)\s*ms", result.stdout, re.I)
        latency = float(match.group(1)) if reachable and match else None
    except (subprocess.TimeoutExpired, OSError):
        reachable = False
        latency = None

    return {
        "name": name,
        "ip": ip,
        "status": "UP" if reachable else "DOWN",
        "latency_ms": latency,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def monitor_devices() -> list[dict]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda item: check_device(*item), DEVICES.items()))
    for device in results:
        print(f"{device['name']} ({device['ip']}): {device['status']} | "
              f"latency: {device['latency_ms']} ms")
    return results


if __name__ == "__main__":
    monitor_devices()


import subprocess

def check_device(ip):
    result = subprocess.run(
        ["ping", "-c", "4", ip],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        print(f"{ip} is responding")
    else:
        print(f"{ip} is not responding")


router_ip = "192.168.0.1"

check_device(router_ip)

devices = {
    "Google DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1"
}