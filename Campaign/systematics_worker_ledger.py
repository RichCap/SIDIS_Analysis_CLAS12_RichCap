# Count-only local-worker ledger for one systematic campaign.
# Unrelated runs keep Campaign/local_resource_gate.py.
import json
import os
import time

try:
    import fcntl
except ImportError:
    fcntl = None


def ledger_folder(data_root, campaign, folder=None):
    if(folder not in [None, ""]):
        os.makedirs(folder, exist_ok=True)
        return folder
    base = None
    try:
        from jlab_work_paths import data_root_path
        root = data_root_path(data_root)
        if(os.path.isdir(root)):
            base = os.path.join(root, "SIDIS_Campaign", "systematics", str(campaign), "worker_slots")
    except Exception:
        base = None
    if(base is None):
        base = os.path.join("/tmp", "SIDIS_systematics_campaign", str(data_root), str(campaign), "worker_slots")
    os.makedirs(base, exist_ok=True)
    return base


def pid_alive(pid):
    if(pid in [None, 0, ""]):
        return False
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    return True


def lock_ledger(folder):
    handle = open(os.path.join(folder, ".lock"), "a+")
    if(fcntl is not None):
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def unlock_ledger(handle):
    if(handle is None):
        return
    try:
        if(fcntl is not None):
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        handle.close()
    except Exception:
        pass


def read_slot(path):
    try:
        handle = open(path)
        payload = json.load(handle)
        handle.close()
    except Exception:
        return None
    if(not isinstance(payload, dict)):
        return None
    return payload


def slot_is_live(payload):
    worker = payload.get("worker_pid")
    parent = payload.get("parent_pid")
    if(worker not in [None, ""]):
        return pid_alive(worker)
    return pid_alive(parent)


def live_slots(folder):
    live = []
    for name in os.listdir(folder):
        if(not name.endswith(".json")):
            continue
        path = os.path.join(folder, name)
        payload = read_slot(path)
        if(payload is None):
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        if(not slot_is_live(payload)):
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        payload["token"] = name[:-5]
        live.append(payload)
    return live


def try_acquire(data_root, campaign, cap, kind, label, folder=None, parent_pid=None):
    # Returns (ok, token). A full ledger does not cancel any SLURM task.
    limit = int(cap)
    slot_dir = ledger_folder(data_root, campaign, folder=folder)
    handle = lock_ledger(slot_dir)
    token = None
    try:
        live = live_slots(slot_dir)
        if((len(live) + 1) > limit):
            return False, None
        token = "%s-%s-%s" % (os.getpid(), kind, time.time_ns())
        payload = {
            "parent_pid": os.getpid() if(parent_pid is None) else int(parent_pid),
            "worker_pid": None,
            "kind": str(kind),
            "label": str(label),
        }
        path = os.path.join(slot_dir, "%s.json" % token)
        out = open(path, "w")
        json.dump(payload, out)
        out.write("\n")
        out.close()
    finally:
        unlock_ledger(handle)
    return True, token


def bind_worker(data_root, campaign, token, worker_pid, folder=None):
    if(token in [None, ""]):
        return
    slot_dir = ledger_folder(data_root, campaign, folder=folder)
    path = os.path.join(slot_dir, "%s.json" % token)
    handle = lock_ledger(slot_dir)
    try:
        payload = read_slot(path)
        if(not isinstance(payload, dict)):
            return
        payload["worker_pid"] = int(worker_pid)
        out = open(path, "w")
        json.dump(payload, out)
        out.write("\n")
        out.close()
    finally:
        unlock_ledger(handle)


def release(data_root, campaign, token, folder=None):
    if(token in [None, ""]):
        return
    slot_dir = ledger_folder(data_root, campaign, folder=folder)
    path = os.path.join(slot_dir, "%s.json" % token)
    handle = lock_ledger(slot_dir)
    try:
        if(os.path.isfile(path)):
            os.remove(path)
    except OSError:
        pass
    finally:
        unlock_ledger(handle)


def acquire_blocking(data_root, campaign, cap, kind, label, folder=None, poll_s=5):
    while(True):
        ok, token = try_acquire(data_root, campaign, cap, kind, label, folder=folder)
        if(ok):
            return token
        time.sleep(poll_s)


def ledger_self_test():
    import tempfile
    folder = tempfile.mkdtemp(prefix="sidis_ledger_")
    ok, token = try_acquire("work_b", "test", 1, "histogram", "a", folder=folder, parent_pid=os.getpid())
    if((not ok) or (token in [None, ""])):
        raise SystemExit("ledger did not grant the first slot")
    blocked, other = try_acquire("work_b", "test", 1, "unfold", "b", folder=folder, parent_pid=os.getpid())
    if(blocked or (other not in [None, ""])):
        raise SystemExit("ledger exceeded the cap")
    release("work_b", "test", token, folder=folder)
    ok2, token2 = try_acquire("work_b", "test", 1, "unfold", "c", folder=folder, parent_pid=os.getpid())
    if(not ok2):
        raise SystemExit("ledger did not reuse a released slot")
    bind_worker("work_b", "test", token2, os.getpid(), folder=folder)
    release("work_b", "test", token2, folder=folder)
    try:
        os.remove(os.path.join(folder, ".lock"))
        os.rmdir(folder)
    except OSError:
        pass
