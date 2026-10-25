# Shared admission for local campaign workers. One ledger for every campaign process on this host.
import json
import os
import socket
import time

try:
    import fcntl
except ImportError:
    fcntl = None

AGG_MEM_GB = 110
AGG_JOBS   = 48
AGG_CPUS   = 48
MEM_CUSHION_GB = 20
_LIVE_MEMORY_NOTE = False
_TOKEN_SEQ = 0

# mem_gb, cpus, kind, ceiling, slurm_mem
MODE_TABLE = {
    "Only_2D":        {"mem_gb": 3,  "cpus": 1, "kind": "histogram",  "ceiling": 6,  "slurm_mem": "3GB"},
    "Only_3D":        {"mem_gb": 4,  "cpus": 1, "kind": "histogram",  "ceiling": 8,  "slurm_mem": "4GB"},
    "Only_5D":        {"mem_gb": 14, "cpus": 1, "kind": "histogram",  "ceiling": 2,  "slurm_mem": "14GB"},
    "Only_1D":        {"mem_gb": 4,  "cpus": 1, "kind": "histogram",  "ceiling": 2,  "slurm_mem": "4GB"},
    "Diagnostic_1D":  {"mem_gb": 5,  "cpus": 1, "kind": "histogram",  "ceiling": 3,  "slurm_mem": "5GB"},
    "rc":             {"mem_gb": 3,  "cpus": 1, "kind": "rc",          "ceiling": 10, "slurm_mem": "3GB"},
    "bc":             {"mem_gb": 3,  "cpus": 1, "kind": "bc",          "ceiling": 10, "slurm_mem": "3G"},
    "iteration_3d":   {"mem_gb": 16, "cpus": 1, "kind": "iteration",   "ceiling": 1,  "slurm_mem": None},
    "unfold_3d":      {"mem_gb": 16, "cpus": 1, "kind": "unfold",      "ceiling": 1,  "slurm_mem": None},
    "iteration_5d":   {"mem_gb": 24, "cpus": 1, "kind": "iteration",   "ceiling": 1,  "slurm_mem": None},
    "unfold_5d":      {"mem_gb": 24, "cpus": 1, "kind": "unfold",      "ceiling": 1,  "slurm_mem": None},
    "acceptance":     {"mem_gb": 4,  "cpus": 1, "kind": "acceptance",  "ceiling": 1,  "slurm_mem": None},
}

PRODUCT_MODE = {
    "2D_Presentation": "Only_2D",
    "Only_3D": "Only_3D",
    "Only_5D": "Only_5D",
    "Only_1D": "Only_1D",
    "Diagnostic_1D": "Diagnostic_1D",
}


def histogram_ceilings():
    ceilings = {}
    for mode in ["Only_2D", "Only_3D", "Only_5D", "Only_1D", "Diagnostic_1D"]:
        ceilings[mode] = MODE_TABLE[mode]["ceiling"]
    return ceilings


def slurm_for_product(product_key):
    mode = PRODUCT_MODE.get(product_key)
    if(mode is None):
        return None
    row = MODE_TABLE[mode]
    return mode, row["slurm_mem"], row["ceiling"]


def clamp_histogram_cap(value):
    if(value in [None, 0]):
        return None
    cap = int(value)
    if(cap < 1):
        return None
    if(cap > AGG_JOBS):
        print("histogram local cap %s is above %s and was clamped" % (cap, AGG_JOBS))
        return AGG_JOBS
    return cap


def slot_directory(data_root):
    folder = None
    try:
        from jlab_work_paths import data_root_path
        root = data_root_path(data_root)
        if(os.path.isdir(root)):
            folder = os.path.join(root, "SIDIS_Campaign", "direct_inputs", "local_resource_slots")
    except Exception:
        folder = None
    if(folder is None):
        folder = os.path.join("/tmp", "SIDIS_local_resource_slots")
    if(not os.path.isdir(folder)):
        os.makedirs(folder, exist_ok=True)
    return folder


def pid_alive(pid):
    if(pid in [None, 0, ""]):
        return False
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    return True


def mem_available_gb(meminfo_text=None):
    text = meminfo_text
    if(text is None):
        path = "/proc/meminfo"
        if(not os.path.isfile(path)):
            return None
        handle = open(path)
        text = handle.read()
        handle.close()
    for line in text.splitlines():
        if(line.startswith("MemAvailable:")):
            parts = line.split()
            if(len(parts) < 2):
                return None
            return float(parts[1]) / (1024.0 * 1024.0)
    return None


def _note_live_memory_once():
    global _LIVE_MEMORY_NOTE
    if(_LIVE_MEMORY_NOTE):
        return
    _LIVE_MEMORY_NOTE = True
    print("live memory was not visible; admission uses the reservation ledger only")


def _lock(folder):
    if(fcntl is None):
        return None
    path = os.path.join(folder, "lock")
    handle = open(path, "a")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def _unlock(handle):
    if(handle is None):
        return
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        handle.close()
    except Exception:
        pass


def _read_slot(path):
    try:
        handle = open(path)
        payload = json.load(handle)
        handle.close()
    except Exception:
        return None
    return payload


def _live_slots(folder, host):
    live = []
    for name in os.listdir(folder):
        if(not name.endswith(".json")):
            continue
        path = os.path.join(folder, name)
        payload = _read_slot(path)
        if(not isinstance(payload, dict)):
            continue
        if(payload.get("host") != host):
            continue
        worker = payload.get("worker_pid")
        parent = payload.get("parent_pid")
        if(worker not in [None, 0, ""]):
            if(not pid_alive(worker)):
                try:
                    os.remove(path)
                except OSError:
                    pass
                continue
        elif(not pid_alive(parent)):
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        live.append(payload)
    return live


def _fits(live, row, histogram_cap, meminfo_text):
    mem_sum = 0.0
    cpu_sum = 0
    mode_count = 0
    histogram_count = 0
    for slot in live:
        mem_sum += float(slot.get("mem_gb", 0))
        cpu_sum += int(slot.get("cpus", 0))
        if(slot.get("mode") == row["mode"]):
            mode_count += 1
        if(slot.get("kind") == "histogram"):
            histogram_count += 1
    if((mode_count + 1) > row["ceiling"]):
        return False, "mode ceiling"
    if((len(live) + 1) > AGG_JOBS):
        return False, "job budget"
    if((cpu_sum + row["cpus"]) > AGG_CPUS):
        return False, "cpu budget"
    if((mem_sum + row["mem_gb"]) > AGG_MEM_GB):
        return False, "memory budget"
    if((row["kind"] == "histogram") and (histogram_cap not in [None, ""])):
        if((histogram_count + 1) > int(histogram_cap)):
            return False, "histogram cap"
    available = mem_available_gb(meminfo_text)
    if(available is None):
        if(meminfo_text is None):
            _note_live_memory_once()
    elif(available < (row["mem_gb"] + MEM_CUSHION_GB)):
        return False, "MemAvailable"
    return True, ""


def try_acquire(data_root, mode, histogram_cap=None, meminfo_text=None, parent_pid=None):
    spec = MODE_TABLE.get(mode)
    if(spec is None):
        print("no local reservation for mode %s" % mode)
        return False, None
    row = {"mode": mode, "mem_gb": spec["mem_gb"], "cpus": spec["cpus"], "kind": spec["kind"], "ceiling": spec["ceiling"]}
    folder = slot_directory(data_root)
    host = socket.gethostname()
    lock = _lock(folder)
    token = None
    try:
        live = _live_slots(folder, host)
        ok, reason = _fits(live, row, histogram_cap, meminfo_text)
        if(not ok):
            print("local slot deferred for %s: %s" % (mode, reason))
            return False, None
        global _TOKEN_SEQ
        _TOKEN_SEQ += 1
        token = "%s-%s-%s" % (os.getpid(), mode, _TOKEN_SEQ)
        payload = {
            "host": host,
            "parent_pid": os.getpid() if(parent_pid is None) else int(parent_pid),
            "worker_pid": None,
            "mode": mode,
            "kind": spec["kind"],
            "mem_gb": spec["mem_gb"],
            "cpus": spec["cpus"],
        }
        path = os.path.join(folder, "%s.json" % token)
        handle = open(path, "w")
        json.dump(payload, handle)
        handle.write("\n")
        handle.close()
    finally:
        _unlock(lock)
    return True, token


def bind_worker(data_root, token, worker_pid):
    if(token in [None, ""]):
        return
    folder = slot_directory(data_root)
    path = os.path.join(folder, "%s.json" % token)
    lock = _lock(folder)
    try:
        payload = _read_slot(path)
        if(not isinstance(payload, dict)):
            return
        payload["worker_pid"] = int(worker_pid)
        handle = open(path, "w")
        json.dump(payload, handle)
        handle.write("\n")
        handle.close()
    finally:
        _unlock(lock)


def release(data_root, token):
    if(token in [None, ""]):
        return
    folder = slot_directory(data_root)
    path = os.path.join(folder, "%s.json" % token)
    lock = _lock(folder)
    try:
        if(os.path.isfile(path)):
            os.remove(path)
    except OSError:
        pass
    finally:
        _unlock(lock)


def acquire_blocking(data_root, mode, histogram_cap=None):
    while(True):
        ok, token = try_acquire(data_root, mode, histogram_cap=histogram_cap)
        if(ok):
            return token
        time.sleep(15)


def record_peak(data_root, mode, reserved_gb, peak_text, mem_visible):
    folder = slot_directory(data_root)
    parent = os.path.dirname(folder)
    path = os.path.join(parent, "local_resource_peaks.txt")
    line = "mode=%s reserved_gb=%s max_child_rss=%s memavailable=%s\n" % (mode, reserved_gb, peak_text, mem_visible)
    try:
        handle = open(path, "a")
        handle.write(line)
        handle.close()
    except OSError as exc:
        print("could not append %s: %s" % (path, exc))
