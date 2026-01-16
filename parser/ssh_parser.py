from datetime import datetime
import uuid

def parse_ssh_failed(line: str):

    if "Failed password for" not in line:
        return None

    parts = line.split()

    try:
     
        user_index = parts.index("for") + 1
        if parts[user_index] == "invalid":
            user = parts[user_index + 2]   # invalid user <name>
        else:
            user = parts[user_index]

        ip = parts[parts.index("from") + 1]
        port = int(parts[parts.index("port") + 1])

    except (ValueError, IndexError):
        return None

    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "source": {
            "type": "linux",
            "service": "ssh"
        },
        "event": {
            "category": "authentication",
            "action": "login_failed",
            "outcome": "failure"
        },
        "actor": {
            "user": user,
            "ip": ip
        },
        "network": {
            "src_ip": ip,
            "src_port": port
        },
        "raw": line.strip()
    }

    return event
