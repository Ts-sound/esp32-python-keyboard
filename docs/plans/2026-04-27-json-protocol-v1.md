# JSON Protocol v1.0 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Implement JSON protocol v1.0 for ESP32 keyboard, replacing pure-text commands with structured JSON format, adding script storage and execution.

**Architecture:** New ProtocolParser module handles JSON parsing/validation. ScriptEngine manages script storage (max 5) and execution with pause/resume/stop. KeyboardService refactored to dispatch JSON commands. RF4Service removed entirely.

**Tech Stack:** MicroPython, asyncio, json module (built-in)

---

## Task Group 1: Core Infrastructure

**Tasks:** 1-3
**Goal:** Protocol parsing and validation foundation
**Acceptance:** Parser handles all command types, proper error responses

### Task 1: ProtocolParser - JSON Parsing and Validation

**Files:**
- Create: `src/protocol_parser.py`
- Create: `tests/test_protocol_parser.py`

**Acceptance Criteria:**
- [ ] Parse valid JSON commands into dict
- [ ] Validate required fields (v, type, action)
- [ ] Return error dict for invalid JSON
- [ ] Return error dict for missing fields
- [ ] Return error dict for unknown type/action
- [ ] Tests pass

**Reference:** Design doc section "请求格式", "响应格式"

**Implementation Notes:**
- Use MicroPython built-in `json` module
- Error format: `{"success": false, "message": "..."}`
- Follow existing error handling pattern (try/except with print_exception)

### Task 2: ProtocolParser - Keyboard Command Validation

**Files:**
- Modify: `src/protocol_parser.py`
- Modify: `tests/test_protocol_parser.py`

**Acceptance Criteria:**
- [ ] Validate keyboard press/release params (keys array)
- [ ] Validate sequence params (steps, loop, variance_ms)
- [ ] Validate type params (text, delay_ms)
- [ ] Apply default values (press_ms=50, release_ms=50, variance_ms=0)
- [ ] Tests pass

**Reference:** Design doc section "键盘命令"

**Implementation Notes:**
- `keys` must be non-empty array
- `loop` can be bool or int
- `variance_ms` defaults to 0, step-level overrides

### Task 3: ProtocolParser - Script Command Validation

**Files:**
- Modify: `src/protocol_parser.py`
- Modify: `tests/test_protocol_parser.py`

**Acceptance Criteria:**
- [ ] Validate script upload params (name, steps, loop, variance_ms)
- [ ] Validate script run/delete params (name)
- [ ] Validate list/status/pause/resume/stop (no params required)
- [ ] Script name must be valid string
- [ ] Tests pass

**Reference:** Design doc section "脚本命令"

**Implementation Notes:**
- `name` required for upload/run/delete
- Steps validation same as sequence

---

## Task Group 2: Script Engine

**Tasks:** 4-6
**Goal:** Script storage and execution with control
**Acceptance:** Scripts stored, executed, paused, stopped

### Task 4: ScriptEngine - Storage and Basic Operations

**Files:**
- Create: `src/script_engine.py`
- Create: `tests/test_script_engine.py`

**Acceptance Criteria:**
- [ ] Store scripts in dict (max 5)
- [ ] upload() creates or updates script
- [ ] delete() removes script
- [ ] list() returns script names
- [ ] Reject upload when limit reached
- [ ] Tests pass

**Reference:** Design doc section "upload", "delete", "list"

**Implementation Notes:**
- Use dict for storage: `self._scripts = {"name": {"steps": [...], "loop": true}}`
- Max 5 scripts constant in config.py

### Task 5: ScriptEngine - Execution with Random Delay

**Files:**
- Modify: `src/script_engine.py`
- Modify: `tests/test_script_engine.py`

**Acceptance Criteria:**
- [ ] run() executes steps sequentially
- [ ] Apply variance_ms to press_ms and release_ms
- [ ] Support loop modes (true=int infinite, int=n times)
- [ ] Each step: press keys, wait press_ms±variance, release, wait release_ms±variance
- [ ] Tests pass (mock keyboard_device)

**Reference:** Design doc section "随机延时计算"

**Implementation Notes:**
- Copy random delay logic from rf4_service.py
- Use `random.uniform(base - variance, base + variance)`
- Async execution with asyncio.sleep_ms

### Task 6: ScriptEngine - Control Operations

**Files:**
- Modify: `src/script_engine.py`
- Modify: `tests/test_script_engine.py`

**Acceptance Criteria:**
- [ ] pause() pauses current execution
- [ ] resume() continues from paused step
- [ ] stop() stops and clears state
- [ ] status() returns running/paused/step/loop_count
- [ ] Tests pass

**Reference:** Design doc section "pause", "resume", "stop", "status"

**Implementation Notes:**
- Use state enum: IDLE, RUNNING, PAUSED
- Track current_step, loop_count
- asyncio.Event for pause/resume

---

## Task Group 3: Service Layer Integration

**Tasks:** 7-9
**Goal:** Integrate new modules into app
**Acceptance:** Commands processed, responses sent, RF4 removed

### Task 7: KeyboardService - Refactor for JSON Commands

**Files:**
- Modify: `src/keyboard_service.py`
- Modify: `tests/test_keyboard_service.py`

**Acceptance Criteria:**
- [ ] Use ProtocolParser to parse incoming commands
- [ ] Dispatch to keyboard_device for press/release/release_all/type
- [ ] Handle sequence action (immediate execution)
- [ ] Return JSON response via wifi_service
- [ ] Tests pass

**Reference:** Design doc section "键盘命令"

**Implementation Notes:**
- Remove old text-based parsing
- sequence action: create temp execution context (no storage)

### Task 8: WiFiService - Add Response Sending

**Files:**
- Modify: `src/wifi_service.py`

**Acceptance Criteria:**
- [ ] send_response() method sends JSON response
- [ ] Called by KeyboardService/ScriptEngine after command
- [ ] Response format matches design doc

**Reference:** Design doc section "响应格式"

**Implementation Notes:**
- Reuse existing send_data() method
- JSON encode response dict

### Task 9: KeyboardApp - Replace RF4 with ScriptEngine

**Files:**
- Modify: `src/keyboard_app.py`
- Modify: `src/config.py`
- Delete: `src/rf4_service.py`

**Acceptance Criteria:**
- [ ] Replace RF4Service with ScriptEngine
- [ ] ScriptEngine runs as asyncio background task
- [ ] KeyboardService dispatches script commands to ScriptEngine
- [ ] Remove RF4 config constants
- [ ] Tests pass

**Reference:** Design doc section "实现模块"

**Implementation Notes:**
- Keep message queue pattern
- Subscribe wifi/raw topic to unified handler

---

## Task Group 4: Documentation and Cleanup

**Tasks:** 10-11
**Goal:** Update docs, verify integration
**Acceptance:** Docs updated, all tests pass

### Task 10: Update Design Docs

**Files:**
- Modify: `docs/design/README.md`
- Modify: `docs/design/protocols/wifi_command.md`
- Modify: `README.md`

**Acceptance Criteria:**
- [ ] Remove RF4 references from architecture diagram
- [ ] Add ProtocolParser and ScriptEngine to diagram
- [ ] Update wifi_command.md to point to json_protocol.md
- [ ] Update README.md with new protocol examples
- [ ] Remove deprecated JSON suggestion section

**Reference:** Design doc

**Implementation Notes:**
- Update mermaid diagrams
- Keep backward compatibility notes

### Task 11: Integration Testing

**Files:**
- Run: `python scripts/test.py`

**Acceptance Criteria:**
- [ ] All unit tests pass
- [ ] No import errors
- [ ] Manual test: send JSON command via TCP

**Reference:** scripts/test.py

**Implementation Notes:**
- Run pytest on all tests
- Check upload.py still works

---

## Execution Notes

**Testing approach:**
- Run `python scripts/test.py` after each task group
- Mock keyboard_device in tests (no real hardware)

**Commit strategy:**
- Commit after each task group completes
- Commit message: "feat(json-protocol): implement Task Group X"

**Backward compatibility:**
- No backward compatibility with old text protocol
- RF4Service completely removed

**File summary:**
- Create: `src/protocol_parser.py`, `src/script_engine.py`, `tests/test_protocol_parser.py`, `tests/test_script_engine.py`
- Modify: `src/keyboard_service.py`, `src/wifi_service.py`, `src/keyboard_app.py`, `src/config.py`
- Delete: `src/rf4_service.py`
- Docs: `docs/design/README.md`, `docs/design/protocols/wifi_command.md`, `README.md`