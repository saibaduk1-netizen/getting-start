# Robot Control System (Learning Project)

## 1. Overview
This project implements a TCP-based robot control system using a state machine and JSON protocol.

The goal is to design a **scalable robot command interface**, not just simple socket communication.

---

## 2. System Architecture
Client (CLI)
→ TCP Socket
→ Server
→ State Machine
→ Robot State

- Client: sends commands in JSON format
- Server: handles TCP communication
- State Machine: processes commands
- Robot State: maintains current state (OPEN/CLOSED, angle)

---
## 3. Command Protocol
- Basic Commands
{"cmd": "open"}
{"cmd": "close"}
{"cmd": "status"}

- Move Command (v0.4)
{"cmd": "move", "mode": "absolute", "angle": 30}
{"cmd": "move", "mode": "relative", "delta": 10}

- Description
absolute: move to target angle
relative: move from current angle

## 4. Features
TCP client-server communication
JSON-based command protocol
State machine-based command handling
Input validation (type / range)
Extended command interface (absolute / relative move)

## 4. How to Run
### 1. Server
cd ~/getting_start
python3 src/robot/server.py

### 2. Client
cd ~/getting_start
python3 src/robot/client.py

---
### 3. Example
move absolute 30
move relative 10
status

---
## 5. Version History
### v0.4 (2026-03-18)
- extended move command (absolute / relative)
- improved command protocol design

response format consistency
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

## Versioning Strategy
This project uses a simple versioning scheme:
- v0.x : Feature-based development stage

---

## 6. Future Plan
- Queue-based command processing (RTOS-style architecture)
- Multi-threaded command handling
- Simulation integration
- ROS2 integration (future)