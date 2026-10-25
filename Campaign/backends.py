# Turn one stage command into a single-line tcsh or SWIF2 invocation.
import shlex


def shell_join(parts):
    return " ".join([shlex.quote(str(part)) for part in parts])


def one_line(command):
    text = command.strip()
    if("\\\n" in text or text.endswith("\\")):
        raise ValueError("farm commands must be one line")
    return text


def swif2_add_job(workflow, name, command, phase, ram, time_limit, cores, stdout_path, stderr_path, antecedents, account, partition, shell):
    parts = [
        "swif2", "add-job",
        "-workflow", workflow,
        "-name", name,
        "-phase", str(phase),
        "-ram", ram,
        "-time", time_limit,
        "-cores", str(cores),
        "-shell", shell,
        "-stdout", stdout_path,
        "-stderr", stderr_path,
        "-account", account,
        "-partition", partition,
    ]
    for parent in antecedents:
        parts.extend(["-antecedent", parent])
    return one_line(shell_join(parts) + " " + one_line(command))


def swif2_create(workflow, max_concurrent):
    return one_line("swif2 create -workflow %s -maxconcurrent %d" % (workflow, int(max_concurrent)))


def local_command(command):
    return one_line(command)
