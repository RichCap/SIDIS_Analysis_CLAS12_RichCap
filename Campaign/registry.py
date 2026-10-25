# Append-only artifact registry. A completed record is reused only when the identity matches.
import json
import os

IDENTITY_FIELDS = [
    "campaign", "source", "variation", "dimension", "method", "acceptance_cut",
    "acceptance_weight", "phi_mode", "spline_iter", "q2y_bin", "stage", "producer",
    "binning_version", "k_selected", "k_provenance", "background_source", "match",
]

STATUSES = [
    "pending", "ready", "running", "completed", "failed", "blocked", "retryable",
    "awaiting_farm", "awaiting_local", "awaiting_jlab_validation",
]


def campaign_dir(data_root, campaign):
    return os.path.join(data_root, "SIDIS_Campaign", campaign)


class Registry:
    def __init__(self, data_root, campaign):
        self.root      = campaign_dir(data_root, campaign)
        self.reg_dir   = os.path.join(self.root, "registry")
        self.jsonl     = os.path.join(self.reg_dir, "artifacts.jsonl")
        self.state_path = os.path.join(self.reg_dir, "state.json")
        os.makedirs(self.reg_dir, exist_ok=True)
        if(not os.path.isfile(self.state_path)):
            self.write_state({})

    def write_state(self, state):
        handle = open(self.state_path, "w")
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.close()

    def read_state(self):
        handle = open(self.state_path)
        state = json.load(handle)
        handle.close()
        return state

    def set_status(self, stage_key, status):
        if(status not in STATUSES):
            raise ValueError("unknown status %s" % status)
        state = self.read_state()
        state[stage_key] = status
        self.write_state(state)

    def append(self, record):
        handle = open(self.jsonl, "a")
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")
        handle.close()

    def records(self):
        if(not os.path.isfile(self.jsonl)):
            return []
        rows = []
        handle = open(self.jsonl)
        for line in handle:
            line = line.strip()
            if(line):
                rows.append(json.loads(line))
        handle.close()
        return rows

    def identity_matches(self, record, wanted):
        for field in IDENTITY_FIELDS:
            if(field not in wanted):
                continue
            if(str(record.get(field)) != str(wanted.get(field))):
                return False
        return True

    def find_completed(self, wanted):
        found = None
        for record in self.records():
            if(record.get("status") != "completed"):
                continue
            if(record.get("validation") not in ["ok", "passed", True]):
                continue
            if(self.identity_matches(record, wanted)):
                found = record
        return found
