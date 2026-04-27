# 项目规范

## 技术栈

- **平台**: ESP32
- **语言**: MicroPython (非标准 Python)
- **并发**: asyncio (MicroPython 版本)
- **BLE HID**: MicroPythonBLEHID 库
- **文件系统**: ESP32 FAT 文件系统

## MicroPython 与 Python 差异

### os 模块

```python
# ❌ Python 标准库 (MicroPython 不支持)
import os.path
os.path.exists("file.txt")
os.path.mkdir("dir")

# ✅ MicroPython 正确方式
import os
os.listdir("dir")  # 列出目录（检查目录是否存在）
os.mkdir("dir")    # 创建目录

# 检查文件存在
try:
    with open("file.txt", "r"):
        exists = True
except OSError:
    exists = False
```

### asyncio

```python
# ❌ Python 标准库
await asyncio.sleep(1.0)

# ✅ MicroPython
await asyncio.sleep_ms(1000)  # 毫秒单位
```

### json

```python
# ✅ MicroPython 内置 json 模块
import json
json.dumps({"key": "value"})
json.loads('{"key": "value"}')
```

### 错误处理

```python
# ✅ MicroPython 标准模式
try:
    # 业务逻辑
except Exception as e:
    print(f"[ERROR] Module.method: {e}")
    import sys
    sys.print_exception(e)  # 打印完整堆栈
```

## 键盘按键规范

### 修饰键别名

以下别名统一映射到左侧修饰键：

| 用户输入别名 | HID 修饰键 | 说明 |
|-------------|-----------|------|
| `ctrl`, `control` | `left_control` | 控制键 |
| `shift` | `left_shift` | 上档键 |
| `alt`, `option` | `left_alt` | Alt/Option 键 |
| `win`, `gui`, `meta`, `cmd` | `left_gui` | Windows/Command/Super 键 |

**实现位置**: `src/hid_mapper.py:MODIFIER_KEY_ALIASES`

**组合键示例**:
```json
{"keys": ["ctrl", "s"]}      // Ctrl+S 保存
{"keys": ["win", "b"]}       // Win+B Windows 任务栏
{"keys": ["alt", "f4"]}      // Alt+F4 关闭窗口
{"keys": ["shift", "a"]}     // Shift+A 大写 A
```

### 常用键名

| 类别 | 键名 |
|------|------|
| 字母 | `a`-`z` |
| 数字 | `0`-`9` |
| 功能键 | `f1`-`f12` |
| 方向键 | `up`, `down`, `left`, `right` |
| 特殊键 | `enter`, `escape`, `backspace`, `tab`, `space`, `delete`, `insert`, `home`, `end` |

## 文件操作规范

### 目录创建

```python
# ✅ 创建目录前先检查
dir_path = "config"
try:
    os.listdir(dir_path)  # 检查是否存在
except OSError:
    os.mkdir(dir_path)    # 不存在则创建
```

### 文件路径

```python
# ✅ ESP32 文件系统路径
SCRIPTS_FILE = "config/scripts.json"  # 相对路径

# ❌ 避免绝对路径
SCRIPTS_FILE = "/config/scripts.json"  # ESP32 不支持
```

### 文件读写

```python
# ✅ MicroPython 文件操作
with open("config/scripts.json", "w") as f:
    json.dump(data, f)

with open("config/scripts.json", "r") as f:
    data = json.load(f)
```

## 命令协议规范

### JSON 格式 (v1.0)

```json
{
  "v": 1,
  "type": "<keyboard|script>",
  "action": "<action>",
  "params": {...}
}
```

### 默认值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `press_ms` | 50 | 按键按下时间 |
| `release_ms` | 50 | 按键释放时间 |
| `variance_ms` | 0 | 随机延时方差 |
| `delay_ms` | 50 | 字符输入间隔 |
| `loop` | false | 循环模式 |

### 错误响应格式

```json
{"success": false, "message": "Script not found: jig"}
```

## 测试规范

### 测试环境

- **运行位置**: PC (Python 3.10+)
- **MicroPython stubs**: `tests/micropython.py`
- **测试命令**: `python scripts/test.py`

### Mock 要求

```python
# ✅ 测试时需要 mock MicroPython 模块
from unittest.mock import patch

with patch('script_engine.os.listdir'):
    engine = ScriptEngine()
```

## 编码规范

### 文件头注释

```python
"""
模块名称

功能描述。
"""
```

### 日志格式

```python
print("[INFO] Module started")      # 信息
print("[WARN] Unknown key: xxx")    # 警告
print("[ERROR] Failed: reason")     # 错误
```

### 常量命名

```python
# ✅ MicroPython const 优化
from micropython import const
MAX_SCRIPTS = const(5)

# ✅ 配置常量
SCRIPTS_FILE = "config/scripts.json"
```

## 目录结构

```
esp32-python-keyboard/
├── boot.py              # ESP32 启动脚本
├── main.py              # 应用入口
├── config/              # 配置文件目录
│   └── scripts.json     # 脚本持久化
└── src/
    ├── config.py        # 统一配置
    ├── keyboard_app.py  # 应用协调器
    ├── keyboard_device.py   # 键盘设备
    ├── keyboard_service.py  # 命令处理
    ├── protocol_parser.py   # JSON 解析
    ├── script_engine.py     # 脚本引擎
    ├── hid_mapper.py        # HID 映射
    ├── msg_queue.py         # 消息队列
    ├── wifi_service.py      # WiFi 服务
    └── led_driver.py        # LED 驱动
```