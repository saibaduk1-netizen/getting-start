# Robot Control System (Learning Project)

## 1. Overview
This project is a simple robot control system built with:
- Python
- TCP socket communication
- JSON-based command protocol

The goal is to simulate a robot control architecture:
Client → Server → State Machine

---
## 2. System Architecture
Client (CLI)
↓ JSON
Server (Socket)
↓ dict
State Machine

---
## 3. How to Run
### 1. Server
cd ~/getting_start
python3 src/robot/server.py

### 2. Client
cd ~/getting_start
python3 src/robot/client.py

---
## 4. Supported Commands
open
close
status
(JSON 기반 구조)
{"cmd": "open"}

---
## 5. Version History
### v0.3
- Added move command with angle parameter
- Expanded robot state with angle value
- Added input validation for move command

### v0.2 (Current)
- JSON-based command protocol implemented
- TCP client-server communication established
- State machine integrated with server

### v0.1
- Basic state machine implemented
- CLI-based command input

# Robot Control System (Learning Project)
## Versioning Strategy
This project uses a simple versioning scheme:
- v0.x : Feature-based development stage

---

## 6. Future Plan
- Add robot joint control (move command)
- Extend command structure (position, angle)
- Integrate with ROS2