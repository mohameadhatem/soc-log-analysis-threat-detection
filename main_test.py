from collector.journal_reader import stream_ssh_logs
from parser.ssh_parser import parse_ssh_failed
from detection.ssh_bruteforce import detect_bruteforce

def main():
    print("[*] SSH SOC Detector is running...")

    for line in stream_ssh_logs():
        # 1️⃣ Parsing (تحليل اللوج)
        event = parse_ssh_failed(line)
        if not event:
            continue

        # 2️⃣ Detection (كشف الهجوم)
        alert = detect_bruteforce(event)

        # 3️⃣ Alert (تنبيه)
        if alert:
            print("\n🚨 ALERT DETECTED")
            print(f"Type      : {alert['alert_type']}")
            print(f"Severity  : {alert['severity']}")
            print(f"IP        : {alert['ip']}")
            print(f"Attempts  : {alert['attempts']}")
            print(f"First Seen: {alert['first_seen']}")
            print(f"Last Seen : {alert['last_seen']}")
            print("-" * 40)

if __name__ == "__main__":
    main()
