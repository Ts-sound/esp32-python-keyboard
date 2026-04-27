# ESP32 Python Keyboard

基于 MicroPython 的 ESP32 BLE HID 键盘，支持 WiFi 远程控制和自动按键功能。

## 功能特性

- **BLE HID 键盘**: 作为蓝牙键盘连接到手机/电脑
- **WiFi 控制**: 通过 TCP 接收 JSON 命令
- **脚本引擎**: 支持命名脚本存储、循环执行、暂停/恢复
- **消息队列**: 模块间通信的发布/订阅机制
- **asyncio 并发**: 基于 asyncio 的并发模型，脚本后台运行

## 项目结构

```
esp32-python-keyboard/
├── bin/                           # 固件文件
│   └── ESP32_GENERIC-*.bin        # MicroPython 固件
│
├── boot.py                        # ESP32 启动脚本（保留空文件）
├── main.py                        # 应用入口（设备上 /main.py）
│
├── lib/                           # 外部依赖
│   └── MicroPythonBLEHID/         # MicroPythonBLEHID 库
│       └── hid_services.py        # HID 服务实现
│
├── src/                           # 源代码
│   ├── config.py                  # 统一配置
│   ├── keyboard_app.py            # 键盘应用逻辑
│   ├── keyboard_device.py         # 键盘设备（直接使用 hid_services）
│   ├── keyboard_service.py        # 键盘命令处理
│   ├── protocol_parser.py         # JSON 协议解析器
│   ├── script_engine.py           # 脚本引擎
│   ├── hid_mapper.py              # HID 键码映射
│   ├── led_driver.py              # LED 驱动
│   ├── msg_queue.py               # 消息队列
│   └── wifi_service.py            # WiFi 服务
│
├── tests/                         # 单元测试
│   ├── test_msg_queue.py
│   ├── test_keyboard_device.py
│   └── test_hid_mapper.py
│
├── scripts/                       # 工具脚本
│   ├── install.py                 # 烧录固件脚本
│   ├── upload.py                  # 上传代码脚本
│   └── test.py                    # 运行测试脚本
│
├── docs/                          # 文档
│   └── design/                    # 设计文档
│
├── DEPENDENCIES.md                # 依赖说明
└── README.md
```

## 快速开始

### 0. 安装依赖

```bash
# 使用 setup.py 脚本检查并安装依赖
python scripts/setup.py

# 或手动安装
pip install esptool mpremote
```

### 1. 烧录 MicroPython 固件

```bash
# 使用 install.py 脚本（推荐）
python scripts/install.py --port /dev/ttyUSB0 --firmware bin/ESP32_GENERIC-20240602-v1.23.0.bin

# 或使用 esptool 手动烧录
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 \
    write_flash -z 0x1000 bin/ESP32_GENERIC-20240602-v1.23.0.bin
```

### 2. 上传代码

```bash
# 使用 upload.py 脚本（使用 mpremote）
python scripts/upload.py /dev/ttyUSB0
```

### 3. 配置 WiFi

编辑 `src/config.py`，修改 WiFi 凭据：

```python
WIFI_SSID = "你的 WiFi 名称"
WIFI_PASSWORD = "你的 WiFi 密码"
```

### 4. 运行

重启 ESP32，LED 闪烁表示启动成功。

## WiFi 控制协议

### 连接

- **地址**: `tcp://<ESP32_IP>:80`
- **格式**: JSON (v1.0)

### 命令示例

```json
// 键盘按键
{"v": 1, "type": "keyboard", "action": "press", "params": {"keys": ["a"]}}
{"v": 1, "type": "keyboard", "action": "press", "params": {"keys": ["ctrl", "s"]}}
{"v": 1, "type": "keyboard", "action": "type", "params": {"text": "Hello World"}}

// 上传脚本
{"v": 1, "type": "script", "action": "upload", "params": {
  "name": "jig",
  "loop": true,
  "variance_ms": 10,
  "steps": [
    {"keys": ["a"], "press_ms": 800, "release_ms": 500}
  ]
}}

// 运行/停止脚本
{"v": 1, "type": "script", "action": "run", "params": {"name": "jig"}}
{"v": 1, "type": "script", "action": "stop"}
{"v": 1, "type": "script", "action": "status"}
```

完整协议文档见 [docs/design/protocols/json_protocol.md](docs/design/protocols/json_protocol.md)。

## 配置说明

主要配置项位于 `src/config.py`：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `WIFI_SSID` | "T" | WiFi 名称 |
| `WIFI_PASSWORD` | "12345678" | WiFi 密码 |
| `HID_DEVICE_NAME` | "ESP32-Keyboard" | BLE 设备名称 |

## 测试

### 单元测试（PC 上运行）

```bash
# 使用 test.py 脚本（推荐）
python scripts/test.py

# 或手动运行 pytest
cd tests
python -m pytest test_msg_queue.py -v
python -m pytest test_keyboard_device.py -v
python -m pytest test_hid_mapper.py -v
```

### 手动测试（ESP32 上）

1. 连接 BLE 设备
2. 测试键盘输入
3. 发送 WiFi 命令验证

## 架构说明

本项目采用分层架构设计，使用 asyncio 实现并发：

```
main.py (asyncio 入口)
    └── keyboard_app.py (asyncio 主循环)
        ├── ScriptEngine 后台任务 (asyncio.create_task)
        ├── WiFi 服务 (async 轮询)
        └── ProtocolParser → KeyboardService
```

详见 [设计文档](docs/design/README.md)。

- **MicroPythonBLEHID**: https://github.com/Heerkog/MicroPythonBLEHID.git
- **MicroPython**: v1.23+
- **mpremote**: MicroPython 官方串口工具

详见 [DEPENDENCIES.md](DEPENDENCIES.md)

## 开发

### 目录说明

- `boot.py` - ESP32 启动脚本（保留空文件，用于硬件初始化预留）
- `main.py` - 应用主入口（设备上 /main.py）
- `src/config.py` - 统一配置管理
- `src/keyboard_device.py` - 键盘设备（直接使用 hid_services）
- `src/keyboard_service.py` - 键盘命令处理
- `src/protocol_parser.py` - JSON 协议解析器
- `src/script_engine.py` - 脚本引擎
- `src/hid_mapper.py` - HID 键码映射表
- `src/led_driver.py` - LED 驱动
- `src/msg_queue.py` - 消息队列
- `src/wifi_service.py` - WiFi 服务
- `src/keyboard_app.py` - 应用逻辑协调器

### 添加新功能

1. 在 src/ 目录创建对应模块
2. 在 keyboard_app.py 中集成新模块
3. 添加测试用例到 tests/
4. 更新文档

### 脚本说明

- `scripts/setup.py` - 检查并安装依赖（esptool, mpremote）
- `scripts/install.py` - 烧录 MicroPython 固件到 ESP32
- `scripts/upload.py` - 使用 mpremote 上传代码到 ESP32
- `scripts/test.py` - 运行单元测试

## 依赖

项目代码采用 GPL-3.0 许可证（与 MicroPythonBLEHID 保持一致）。

## 致谢

- [MicroPythonBLEHID](https://github.com/Heerkog/MicroPythonBLEHID.git) - BLE HID 服务库
