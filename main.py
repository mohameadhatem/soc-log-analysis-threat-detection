try:
    from collector.journal_reader import stream_ssh_logs
    from parser.ssh_parser import parse_ssh_failed
    from detection.ssh_bruteforce import detect_bruteforce
    from datetime import datetime, timezone
    from logo.logo import secure_mind_team_format
except Exception as a:
    print(a)    

try:

    def to_local(utc_iso: str) -> str:
        # نحول النص إلى datetime
        dt = datetime.fromisoformat(utc_iso)

        # نعتبره UTC صراحة
        dt = dt.replace(tzinfo=timezone.utc)

        # نحوله لتوقيت الجهاز
        local_dt = dt.astimezone()

        return local_dt.strftime("%Y-%m-%d %H:%M:%S")

    def main():
        secure_mind_team_format()
        print("[*] SSH SOC Detector is running...")

        for line in stream_ssh_logs():
            # Parsing (تحليل اللوج)
            event = parse_ssh_failed(line)
            if not event:
                continue

            # Detection (كشف الهجوم)
            alert = detect_bruteforce(event)

            # Alert (تنبيه)
            if alert:
                print("\n🚨 ALERT DETECTED")
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
    print (a)
