---
# 🔐 SOC Log Analysis & Threat Detection

## 📌 Project Overview
A practical SOC learning project focused on **log analysis**, **threat detection**, and **security event modeling** using real system logs.

This project simulates how SOC tools process authentication logs to detect malicious activity such as brute-force attacks.

---

## 🎯 Project Goals
* Log collection
* Log parsing & normalization
* Stateful detection logic
* Alert severity escalation
  in a **modular, production-like design**.
  ---
- Understand how SOC tools work internally
- Analyze real Linux authentication logs (SSH)
- Convert raw logs into structured security events
- Build a foundation for detection, investigation, and SIEM concepts

---

## 🧱 Project Architecture
```
SSH Logs (systemd journal)
        ↓
Collector (Live Logs Streaming)  
        ↓
Parser (Log Normalization)
        ↓
Detection Engine (Brute Force Logic)
        ↓
Alerts (Severity-based)
```

---
### Components

* **Collector**: Streams SSH logs in real time from `journalctl`
* **Parser**: Converts raw logs into structured security events
* **Detection Engine**: Correlates events over time to detect attacks
* **Main**: Orchestrates the pipeline

---

## 📂 Current Project Structure

```
soc-log-analysis-threat-detection/
│
├── collector/
│   └── journal_reader.py      # Live SSH log collection
│
├── parser/
│   └── ssh_parser.py          # SSH failed-login parser
│
├── detection/
│   └── bruteforce.py          # Brute-force detection logic
│
├── main.py                    # Pipeline orchestrator
└── README.md
```
---

### Design Principle

The project follows **Separation of Concerns**:

* Each component has **one clear responsibility**
* Detection logic is isolated from parsing and collection
* Easy to extend with new detections or log sources

---

## 🧾 Event Normalization

Raw SSH log example:

```
Failed password for invalid user test from 10.0.0.5 port 4444 ssh2
```

Parsed into a **structured security event**:

```json
{
  "event_id": "uuid",
  "timestamp": "2026-01-16T04:23:58",
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
    "user": "test",
    "ip": "10.0.0.5"
  },
  "network": {
    "src_ip": "10.0.0.5",
    "src_port": 4444
  },
  "raw": "Failed password for invalid user test from 10.0.0.5 port 4444 ssh2"
}
```

This format is inspired by **SIEM normalized event models**.

---

## 🚨 Brute Force Detection Logic

### Detection Strategy

* Track failed SSH login attempts **per IP**
* Use a **sliding time window**
* Generate alerts only when **severity escalates**

This prevents:

* Alert flooding
* SOC noise
* Repeated alerts for the same behavior

---

## ⏱ Time Window

* **60 seconds sliding window**
* Old attempts outside the window are automatically removed

---

## 🔥 Severity Model

| Failed Attempts | Severity  |
| --------------- | --------- |
| 5 – 7           | Low 🟢    |
| 8 – 10          | Medium 🟡 |
| 11+             | High 🔴   |

### SOC Rationale

* **Low**: Possible user mistake
* **Medium**: Suspicious automated behavior
* **High**: Confirmed brute-force attack

---

## 🚦 Alert Escalation Logic

Alerts are generated **only when severity changes**:

| Attempts | Severity | Alert |
| -------- | -------- | ----- |
| 5        | Low      | ✅     |
| 6–7      | Low      | ❌     |
| 8        | Medium   | ✅     |
| 9–10     | Medium   | ❌     |
| 11       | High     | ✅     |
| 12+      | High     | ❌     |

This simulates **real SOC alert handling**.

---

## ▶️ How to Run

```bash
sudo python3 main.py
```

> `sudo` is required to read system logs via `journalctl`.

---

## 🧪 Testing the Detection

Run multiple failed SSH login attempts:

```bash
ssh test@localhost
```

After enough attempts, alerts will appear:

```
🚨 ALERT DETECTED
Type      : ssh_bruteforce
Severity  : high
IP        : ::1
Attempts  : 11
```

---

## 🎯 Skills Demonstrated

This project demonstrates:

* Linux log analysis
* Real-time log streaming
* Event normalization
* Stateful detection logic
* Time-based correlation
* SOC alerting strategy
* Clean Python project structure

---

## 🚀 Future Improvements

* Persist detection state (Redis / database)
* Add automated response (IP blocking)
* Add dashboard or alert export
* Support additional services (FTP, RDP, HTTP)

---

## 🧠 Why This Project Matters

This project reflects **how SOC detection systems actually work**, not just theoretical scripts.

It shows:

* Blue Team mindset
* Detection engineering fundamentals
* Production-aware design decisions


---

## 👤 Author
Mohamed Hatem  
SOC & Cyber Security Learning Project
