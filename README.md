# Robot Control System

## 1. Overview
A scalable robot control system implementing asynchronous command processing using a queue-worker architecture over TCP.

The goal of this project is to design a robust execution architecture for robot control systems, not just socket-based communication.

---
## 2. Why this problem matters
In real-world robot and embedded systems:
- Command execution is often slower than communication
- Commands may arrive in bursts
- Blocking execution in the communication layer can cause system-wide degradation

This leads to:
- Blocking I/O
- Reduced responsiveness
- System instability under load
- Difficulty scaling the system

---
## 3. Design Goal
This project aims to:

- Decouple communication and execution
- Enable non-blocking command handling
- Provide a scalable command processing structure
- Simulate real-world robot control execution pipelines

---
## 4. System Architecture
Client → TCP → Server → Queue → Worker → CommandService → StateMachine → RobotState

### Layered Structure
- Interface Layer: TCP communication (Server/Client)
- Buffer Layer: CommandQueue (decoupling)
- Execution Layer: Worker + CommandService
- Decision Layer: StateMachine
- State Layer: RobotState

---
## 5. Core Design Principles
### 1. Separation of Concerns
Communication, buffering, execution, and decision logic are separated.

### 2. Asynchronous Boundary
Queue acts as a boundary between I/O and execution.

### 3. Non-blocking I/O
Server immediately responds after enqueue.

### 4. Scalable Execution Structure
Worker-based execution allows future extension to multi-worker systems.

---
## 6. Async Processing Model
This system follows a producer-consumer architecture:

- TCP Server → Producer
- CommandQueue → Buffer
- Worker → Consumer

This structure is commonly used in:

- RTOS message queue systems
- Robot execution pipelines
- Distributed processing systems

---
## 7. Data Flow
1. TCP Server receives raw bytes
2. Bytes are parsed into JSON
3. JSON is validated and converted into command
4. Command is pushed into queue
5. Worker consumes command
6. CommandService processes logic
7. StateMachine determines state transition
8. RobotState is updated

---
## 8. Command Processing Flow
Receive → Parse → Enqueue → Immediate Response → Worker Execute → State Update

---
## 9. State Machine Design
Supported commands:

- open
- close
- move (absolute / relative)
- status

Move command:
- absolute: move to target angle
- relative: move from current position

---
## 10. Command Protocol
{"command": "open"}
{"command": "close"}
{"command": "status"}
{"command": "move", "mode": "absolute", "angle": 30}
{"command": "move", "mode": "relative", "delta": 10}

---
## 11. Design Decisions
### Queue-based Decoupling
- Prevents blocking in communication layer
- Absorbs burst traffic
### Single Worker Model (v0.6)
- Ensures deterministic execution
- Simplifies concurrency issues
### Thread-based Execution (Future work: v0.7~)
- Lightweight and sufficient for current scale
- Can be extended to multi-thread or process-based execution

---
## 12. Features
- TCP client-server communication
- JSON-based command protocol
- Queue-based asynchronous processing
- State machine-based execution
- Input validation (type / range)
- Layered architecture
- Full pytest coverage

---
## 13. How to Run
### Server
python3 src/robot/run_server.py
### Client
python3 src/robot/run_client.py

---
## 14. Version History
### v0.6 (2026-03-20 23:30)
- Refactored application layer structure
- Introduced clear entry points (run_server / run_client)
- Stabilized service-state interaction
- Full test coverage across all layers
- Achieved system-level validation

### v0.5 (2026-03-18 23:20)
- Introduced queue-based asynchronous processing
- Implemented worker thread (producer-consumer model)
- Decoupled server I/O from command execution
- Verified core state machine logic with pytest before server refactoring
- Improved system scalability and structure

### v0.4 (2026-03-18 16:45)
- extended move command (absolute / relative)
- improved command protocol design
- response format consistency

### v0.3(2026-03-18 13:20)
- Added move command with angle parameter
- Expanded robot state with angle value
- Added input validation for move command

### v0.2(2026-03-18 08:30)
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

## 7. Future Plan
### v0.7 (Next Step)
- Command abstraction refinement
- Error handling improvements
- Logging system integration

### v0.8 
- Command result tracking
- Async response handling
- Command ID / status management

### v0.9+
- Multi-worker execution
- Priority queue
- Simulation adapter

### v1.0 Vision
- Integration with ROS2 execution model
- Support for real robot hardware interface