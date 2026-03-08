# 🔐 SOC Log Analysis & Threat Detection

## 📌 Project Overview

A practical SOC learning project focused on **log analysis**, **threat detection**, and **security event modeling** using real Linux system logs.

This project simulates how **Security Operations Center (SOC)** tools monitor authentication logs to detect malicious activities such as **SSH brute-force attacks**.

The system implements a modular detection pipeline similar to real-world **SIEM and SOC monitoring architectures**.

---

## 🎯 Project Goals

This project demonstrates how SOC detection systems operate internally by implementing the following concepts:

* Log collection from live system logs
* Log parsing and normalization
* Stateful detection logic
* Time-based attack correlation
* Severity-based alert escalation

The project also builds a foundation for understanding:

* SOC monitoring workflows
* Detection engineering principles
* Security event modeling
* SIEM pipeline design

---

## 🧱 Project Architecture

System Logs (journalctl)
  │
  ▼
Log Collector
  │
  ▼
Log Parser
  │
  ▼
Detection Engine
  │
  ▼
SOC Alert

### Components

**Collector**

* Streams SSH authentication logs in real time using `journalctl`.

**Parser**

* Converts raw log messages into structured security events.

**Detection Engine**

* Correlates authentication failures and detects brute-force behavior.

**Main**

* Orchestrates the full SOC detection pipeline.

---

## 📂 Project Structure

soc-log-analysis-threat-detection/

├── collector/
│  └── journal_reader.py  # Live SSH log collection

├── parser/
│  └── ssh_parser.py    # SSH failed-login parser

├── detection/
│  └── ssh_bruteforce.py # Brute-force detection logic

├── logo/
│  └── logo.py      # Terminal banner

├── main.py        # Detection pipeline orchestrator

└── README.md

---

## ⚙️ Requirements

* Linux system with **systemd**
* Python **3.9+**
* SSH service enabled
* Permission to read system logs (`journalctl`)

---

## 🧾 Event Normalization

Raw SSH log example:

Failed password for invalid user test from 10.0.0.5 port 4444 ssh2

Converted into a **structured security event**:

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

This structure is inspired by **normalized SIEM event models** used in enterprise security platforms.

---

## 🚨 Brute Force Detection Logic

### Detection Strategy

The detection engine tracks **failed SSH login attempts per IP address** and uses a **sliding time window** to identify brute-force behavior.

Alerts are triggered only when attack severity escalates to reduce SOC noise and alert flooding.

---

## ⏱ Time Window

Detection operates using a **60-second sliding window**.

Failed attempts outside the window are automatically removed to ensure detection is based on **recent activity**.

---

## 🔥 Severity Model

| Failed Attempts | Severity  |
| --------------- | --------- |
| 5 – 7           | Low 🟢    |
| 8 – 10          | Medium 🟡 |
| 11+             | High 🔴   |

### SOC Rationale

Low → Possible user mistake or early probing activity
Medium → Suspicious automated authentication attempts
High → Confirmed brute-force attack behavior

---

## 🚦 Alert Escalation Logic

Alerts are generated **only when severity changes**.

| Attempts | Severity | Alert Generated |
| -------- | -------- | --------------- |
| 5        | Low      | ✅               |
| 6–7      | Low      | ❌               |
| 8        | Medium   | ✅               |
| 9–10     | Medium   | ❌               |
| 11       | High     | ✅               |
| 12+      | High     | ❌               |

This simulates **real SOC alert management practices**.

---

## ▶️ Running the Tool

Run the detection pipeline:

sudo python3 main.py

`sudo` is required because the tool reads system logs from **journalctl**.

---

## 🧪 Testing the Detection

Generate failed SSH login attempts:

ssh test@localhost

After multiple failed attempts, the system generates an alert:

🚨 ALERT DETECTED
Type   : ssh_bruteforce
Severity : medium
IP    : 127.0.0.1
Attempts : 8
First Seen: 2026-03-09 01:01:52
Last Seen : 2026-03-09 01:02:39

---

## 📸 Detection Example

Example output produced during a simulated brute-force test in a lab environment.

Add a screenshot in the repository:

screenshots/detection.png

---

## 🎯 SOC Skills Demonstrated

This project demonstrates practical **blue-team and SOC engineering skills**:

* Linux security log analysis
* Real-time log streaming using `journalctl`
* Security event normalization
* Brute-force detection engineering
* Time-window based event correlation
* SOC alert generation
* Modular security tool architecture

---

## 🚀 Future Improvements

Possible enhancements for the project:

* Persist detection state using Redis or a database
* Add automated response (IP blocking / firewall rules)
* Export alerts to SIEM platforms
* Create dashboards or visualization
* Add support for additional services (FTP, RDP, HTTP)

---

## 🛡 SOC Relevance

The architecture implemented in this project mirrors the internal workflow of many **SIEM and detection systems**:

Log Ingestion → Parsing → Event Normalization → Detection → Alerting

This demonstrates practical understanding of **SOC monitoring pipelines and detection engineering concepts**.

---

## 👤 Author

Mohamed Hatem
Cybersecurity & SOC Learning Project
