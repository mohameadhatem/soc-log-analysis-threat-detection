try:
    from collector.journal_reader import stream_ssh_logs
    from parser.ssh_parser import parse_ssh_failed
    from detection.ssh_bruteforce import detect_bruteforce
    from datetime import datetime, timezone
    from logo.logo import secure_mind_team_format
    import uuid
except Exception as a:
    print(a)

try:
    def to_local(utc_iso: str) -> str:
        dt = datetime.fromisoformat(utc_iso)
        dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone()
        return local_dt.strftime("%Y-%m-%d %H:%M:%S")

    def main():
        secure_mind_team_format()
        print("[*] SSH SOC Detector is running...")

        for line in stream_ssh_logs():
            # Parsing
            event = parse_ssh_failed(line)
            if not event:
                continue

            # Detection
            alert = detect_bruteforce(event)

            # Alert
            if alert:
                alert_id = str(uuid.uuid4())
                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save alert to file
                with open("alerts.log", "a") as f:
                    f.write(
                        f"{alert_id} | {alert_time} | {alert['alert_type']} | "
                        f"{alert['severity']} | {alert['ip']} | {alert['attempts']} | "
                        f"{alert['first_seen']} | {alert['last_seen']}\n"
                    )

                print("\n🚨 ALERT DETECTED")
                print(f"Alert ID  : {alert_id}")
                print(f"Alert Time: {alert_time}")
                print(f"Type      : {alert['alert_type']}")
                print(f"Severity  : {alert['severity']}")
                print(f"IP        : {alert['ip']}")
                print(f"Attempts  : {alert['attempts']}")
                print(f"First Seen: {to_local(alert['first_seen'])}")
                print(f"Last Seen : {to_local(alert['last_seen'])}")
                print("-" * 40)

    if __name__ == "__main__":
        main()

except Exception as a:
    print(a)
