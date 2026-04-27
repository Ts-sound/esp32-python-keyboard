# JSON 协议 v1.0

## 概述

JSON 协议 v1.0 替代原有的纯文本命令格式，提供结构化的命令和响应机制。

## 协议版本

- **当前版本**: 1
- **版本字段**: `v`

## 请求格式

```json
{
  "v": 1,
  "type": "<type>",
  "action": "<action>",
  "params": {...}
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `v` | int | 是 | 协议版本，当前为 1 |
| `type` | string | 是 | 命令类型：`keyboard` / `script` |
| `action` | string | 是 | 具体操作 |
| `params` | object | 否 | 参数对象（部分 action 无参数） |

## 响应格式

### 成功响应

```json
{
  "success": true,
  "message": "OK",
  "data": {...}
}
```

### 失败响应

```json
{
  "success": false,
  "message": "Script not found: jig"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | bool | 执行结果 |
| `message` | string | 结果描述 |
| `data` | object | 返回数据（可选） |

## 键盘命令

**type**: `keyboard`

### press - 按下按键

按下按键但不自动释放。

```json
{
  "v": 1,
  "type": "keyboard",
  "action": "press",
  "params": {
    "keys": ["ctrl", "s"]
  }
}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `keys` | string[] | 按键列表，支持修饰键组合 |

### release - 释放按键

```json
{
  "v": 1,
  "type": "keyboard",
  "action": "release",
  "params": {
    "keys": ["a"]
  }
}
```

### release_all - 释放所有按键

```json
{
  "v": 1,
  "type": "keyboard",
  "action": "release_all"
}
```

无参数。

### type - 输入字符串

```json
{
  "v": 1,
  "type": "keyboard",
  "action": "type",
  "params": {
    "text": "Hello World",
    "delay_ms": 50
  }
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | string | - | 输入文本 |
| `delay_ms` | int | 50 | 每个字符间隔 |

### sequence - 按键序列

执行按键序列，支持循环和随机延时。

```json
{
  "v": 1,
  "type": "keyboard",
  "action": "sequence",
  "params": {
    "loop": true,
    "variance_ms": 10,
    "steps": [
      {"keys": ["a"], "press_ms": 50, "release_ms": 50},
      {"keys": ["b"], "press_ms": 100, "release_ms": 80, "variance_ms": 20}
    ]
  }
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `steps` | object[] | - | 按键步骤列表 |
| `loop` | bool/int | false | 循环模式：`true`=无限，数字=指定次数 |
| `variance_ms` | int | 0 | 随机延时方差（统一应用于所有步骤） |

**step 格式**:

```json
{
  "keys": ["a"],
  "press_ms": 50,
  "release_ms": 50,
  "variance_ms": 10
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `keys` | string[] | - | 按键列表 |
| `press_ms` | int | 50 | 按下持续时间 |
| `release_ms` | int | 50 | 释放后间隔 |
| `variance_ms` | int | 继承上级 | 随机延时方差，可覆盖默认值 |

**随机延时计算**:

```
实际时间 = 设定时间 + random(-variance_ms, variance_ms)
```

例如：`press_ms=50, variance_ms=10` → 随机范围 40-60ms

## 脚本命令

**type**: `script`

脚本存储在 RAM 中，最多 5 个命名脚本。

### upload - 上传脚本

```json
{
  "v": 1,
  "type": "script",
  "action": "upload",
  "params": {
    "name": "jig",
    "loop": true,
    "variance_ms": 10,
    "steps": [
      {"keys": ["a"], "press_ms": 800, "release_ms": 500},
      {"keys": ["b"], "press_ms": 300, "release_ms": 200, "variance_ms": 30}
    ]
  }
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | string | - | 脚本名称（唯一标识） |
| `steps` | object[] | - | 按键步骤列表（格式同 sequence） |
| `loop` | bool/int | false | 循环模式 |
| `variance_ms` | int | 0 | 随机延时方差 |

### list - 列出脚本

```json
{
  "v": 1,
  "type": "script",
  "action": "list"
}
```

**响应**:

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "scripts": ["jig", "pull", "custom"]
  }
}
```

### run - 运行脚本

```json
{
  "v": 1,
  "type": "script",
  "action": "run",
  "params": {
    "name": "jig"
  }
}
```

### pause - 暂停脚本

暂停当前运行的脚本。

```json
{
  "v": 1,
  "type": "script",
  "action": "pause"
}
```

无参数。

### resume - 恢复脚本

恢复暂停的脚本。

```json
{
  "v": 1,
  "type": "script",
  "action": "resume"
}
```

无参数。

### stop - 停止脚本

停止当前脚本，清除运行状态。

```json
{
  "v": 1,
  "type": "script",
  "action": "stop"
}
```

无参数。

### delete - 删除脚本

```json
{
  "v": 1,
  "type": "script",
  "action": "delete",
  "params": {
    "name": "jig"
  }
}
```

### status - 查询状态

```json
{
  "v": 1,
  "type": "script",
  "action": "status"
}
```

**响应**:

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "running": true,
    "paused": false,
    "script": "jig",
    "step": 3,
    "total_steps": 10,
    "loop_count": 5,
    "max_loops": 10
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `running` | bool | 是否正在运行 |
| `paused` | bool | 是否暂停 |
| `script` | string | 当前脚本名称 |
| `step` | int | 当前步骤索引 |
| `total_steps` | int | 总步骤数 |
| `loop_count` | int | 已循环次数 |
| `max_loops` | int | 最大循环次数（`true` 表示无限） |

## 按键名称映射

### 修饰键

| 名称 | HID 键码 |
|------|----------|
| `ctrl` | Left Control |
| `shift` | Left Shift |
| `alt` | Left Alt |
| `win` | Left GUI (Windows/Command) |

### 常用键

| 名称 | 说明 |
|------|------|
| `a`-`z` | 字母键 |
| `0`-`9` | 数字键 |
| `enter` | 回车键 |
| `escape` / `esc` | 退出键 |
| `backspace` | 退格键 |
| `space` | 空格键 |
| `tab` | Tab 键 |
| `f1`-`f12` | 功能键 |
| `up`/`down`/`left`/`right` | 方向键 |

## 错误处理

| 错误场景 | 响应 message |
|----------|--------------|
| JSON 解析失败 | `Invalid JSON` |
| 缺少必填字段 | `Missing field: type` |
| 未知 type | `Unknown type: xxx` |
| 未知 action | `Unknown action: xxx` |
| 脚本不存在 | `Script not found: xxx` |
| 脚本数量超限 | `Script limit reached (max 5)` |
| 脚本已存在 | `Script already exists: xxx` |
| 无脚本运行 | `No script running` |
| 脚本未暂停 | `Script not paused` |

## Python 客户端示例

```python
import socket
import json

def send_command(ip, port, command):
    sock = socket.socket()
    sock.connect((ip, port))
    sock.send(json.dumps(command).encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    sock.close()
    return json.loads(response)

# 按键
resp = send_command("192.168.1.100", 80, {
    "v": 1,
    "type": "keyboard",
    "action": "press",
    "params": {"keys": ["ctrl", "s"]}
})

# 上传脚本
resp = send_command("192.168.1.100", 80, {
    "v": 1,
    "type": "script",
    "action": "upload",
    "params": {
        "name": "jig",
        "loop": True,
        "steps": [
            {"keys": ["a"], "press_ms": 800, "release_ms": 500}
        ]
    }
})

# 运行脚本
resp = send_command("192.168.1.100", 80, {
    "v": 1,
    "type": "script",
    "action": "run",
    "params": {"name": "jig"}
})

# 查询状态
resp = send_command("192.168.1.100", 80, {
    "v": 1,
    "type": "script",
    "action": "status"
})
```

## 与旧协议对比

| 特性 | 旧协议（纯文本） | 新协议（JSON v1.0） |
|------|------------------|---------------------|
| 格式 | `jig;800;500` | 结构化 JSON |
| 组合键 | `ctrl+a` | `{"keys":["ctrl","a"]}` |
| 脚本 | 无 | 支持命名脚本存储 |
| 控制 | 仅开始/停止 | pause/resume/status |
| 循环 | 无 | loop 参数 |
| 随机延时 | 无 | variance_ms 参数 |
| 响应 | 无响应 | 结构化 JSON 响应 |
| 错误处理 | 隐式 | 显式错误消息 |

## 实现模块

| 模块 | 文件 | 职责 |
|------|------|------|
| 协议解析器 | `src/protocol_parser.py` | JSON 解析、验证、错误处理 |
| 脚本引擎 | `src/script_engine.py` | 脚本存储、执行、控制 |
| 键盘服务 | `src/keyboard_service.py` | 键盘命令处理（重构） |
| WiFi 服务 | `src/wifi_service.py` | TCP 通信、响应发送 |