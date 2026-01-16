from collections import defaultdict
from datetime import datetime, timedelta

# =========================
# In-Memory Storage
# =========================

# IP -> list of attempt timestamps
FAILED_ATTEMPTS = defaultdict(list)

# IP -> last alerted severity
LAST_SEVERITY = {}

# =========================
# Detection Configuration
# =========================

WINDOW_SECONDS = 60  # Time Window (نافذة زمنية)

LOW_THRESHOLD = 5
MEDIUM_THRESHOLD = 8
HIGH_THRESHOLD = 11

# =========================
# Severity Logic
# =========================

def calculate_severity(attempts: int):
    """
    Determine severity level based on number of attempts.
    """
    if attempts >= HIGH_THRESHOLD:
        return "high"
    elif attempts >= MEDIUM_THRESHOLD:
        return "medium"
    elif attempts >= LOW_THRESHOLD:
        return "low"
    return None

# =========================
# Detection Logic
# =========================

def detect_bruteforce(event: dict):
    """
    Detect SSH brute-force attacks using failed login events.

    Alert is generated ONLY when severity level changes (escalation).
    """

    ip = event["actor"]["ip"]
    event_time = datetime.fromisoformat(event["timestamp"])

    # Add current attempt
    FAILED_ATTEMPTS[ip].append(event_time)

    # Remove attempts outside time window
    window_start = event_time - timedelta(seconds=WINDOW_SECONDS)
    FAILED_ATTEMPTS[ip] = [
        t for t in FAILED_ATTEMPTS[ip]
        if t >= window_start
    ]

    # Calculate attempts & severity
    attempts = len(FAILED_ATTEMPTS[ip])
    severity = calculate_severity(attempts)

    # No severity → no alert
    if not severity:
        return None

    # Prevent duplicate alerts for same severity
    if LAST_SEVERITY.get(ip) == severity:
        return None

    # Update last severity
    LAST_SEVERITY[ip] = severity

    # Generate alert
    return {
        "alert_type": "ssh_bruteforce",
        "severity": severity,
        "ip": ip,
        "attempts": attempts,
        "time_window_seconds": WINDOW_SECONDS,
        "first_seen": FAILED_ATTEMPTS[ip][0].isoformat(),
        "last_seen": FAILED_ATTEMPTS[ip][-1].isoformat()
    }
