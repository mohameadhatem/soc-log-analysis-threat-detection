import subprocess


def stream_ssh_logs():
    cmd = ["journalctl", "-u", "ssh", "-f", "-o", "cat"]
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True)
    for line in proc.stdout:
        yield line.rstrip("\n")
