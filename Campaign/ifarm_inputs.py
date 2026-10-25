# New iFarm HIPO inputs. rho0_new is the internal source. The discriminator only selects files.
import json
import os

_DEFAULT = os.path.join(os.path.dirname(__file__), "ifarm_inputs.json")


def load_ifarm_inputs(path=None):
    use = path if(path) else _DEFAULT
    if(not os.path.isfile(use)):
        return {}
    handle = open(use)
    payload = json.load(handle)
    handle.close()
    return payload


def rho_source_token(config=None):
    config = load_ifarm_inputs() if(config is None) else config
    return str(config.get("rho_source_token", "") or "")


def rho_name_discriminator(config=None):
    config = load_ifarm_inputs() if(config is None) else config
    return str(config.get("rho_name_discriminator", "") or "")


def source_order(config=None):
    config = load_ifarm_inputs() if(config is None) else config
    order = list(config.get("source_order") or ["lundvpk", "lundrho"])
    token = rho_source_token(config)
    if((token) and (token not in order)):
        order.append(token)
    return order


def matches_new_rho(name, config=None):
    config = load_ifarm_inputs() if(config is None) else config
    low = str(name).lower()
    token = rho_source_token(config).lower()
    disc = rho_name_discriminator(config).lower()
    if((token) and (token in low)):
        return True
    if((disc) and (disc in low)):
        return True
    return False


def registered_rho0_new_norm(path=None):
    # Campaign/rho_factors.json: {"rho0_new": {"n_rho": <finite float>}}.
    # The placeholder RHO_NORM_RHO0_NEW = 1.0 is not used once this file exists.
    use = path if(path) else os.path.join(os.path.dirname(__file__), "rho_factors.json")
    if(not os.path.isfile(use)):
        raise SystemExit("rho0_new weight requested but %s is not registered. Finish the unweighted normalization first." % use)
    handle = open(use)
    payload = json.load(handle)
    handle.close()
    entry = payload.get("rho0_new") if(isinstance(payload, dict)) else None
    value = entry.get("n_rho") if(isinstance(entry, dict)) else None
    if(isinstance(value, bool) or (not isinstance(value, (int, float)))):
        raise SystemExit("rho0_new weight requested but %s has no numeric rho0_new.n_rho. Do not use the placeholder 1.0 or another sample." % use)
    value = float(value)
    if((value != value) or (value == float("inf")) or (value == float("-inf"))):
        raise SystemExit("rho0_new weight requested but %s rho0_new.n_rho is not finite." % use)
    return value


def classify_rho_name(name, config=None):
    # Returns the internal source, or "" when the name is not a dedicated rho file.
    config = load_ifarm_inputs() if(config is None) else config
    low = str(name).lower()
    if(matches_new_rho(name, config)):
        token = rho_source_token(config)
        return token if(token) else "rho0_new"
    if((".rho0." in low) and ("lundvpk" in low)):
        return "lundvpk"
    if("lundvpk" in low):
        return "lundvpk"
    if((".rho0." in low) or ("lundrho" in low)):
        return "lundrho"
    return ""
