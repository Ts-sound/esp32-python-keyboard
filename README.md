# ESP32 Python Keyboard

基于 MicroPython 的 ESP32 BLE HID 键盘，支持 WiFi 远程控制和自动按键功能。

## 功能特性

- **BLE HID 键盘**: 作为蓝牙键盘连接到手机/电脑
- **BLE HID 鼠标**: 支持鼠标模式
- **WiFi 控制**: 通过 TCP 接收远程命令
- **RF4 自动按键**: 支持 JIG 和 PULL 两种自动按键模式
- **消息队列**: 模块间通信的发布/订阅机制

## 项目结构

```
esp32-python-keyboard/
├── bin/                           # 固件文件
│   └── ESP32_GENERIC-*.bin        # MicroPython 固件
│
├── lib/                           # 外部依赖
│   └── MicroPythonBLEHID/         # MicroPythonBLEHID 库
│       └── hid_services.py        # HID 服务实现
│
├── src/                           # 源代码
│   ├── boot.py                    # 启动脚本
│   ├── main.py                    # 应用入口
│   ├── config.py                  # 统一配置
│   ├── keyboard_app.py            # 键盘应用逻辑
│   ├── keyboard_device.py         # 键盘设备
│   ├── mouse_device.py            # 鼠标设备
│   ├── hid_driver.py              # HID 驱动封装
│   ├── led_driver.py              # LED 驱动
│   ├── msg_queue.py               # 消息队列
│   ├── wifi_service.py            # WiFi 服务
│   ├── rf4_service.py             # RF4 服务
│   └── hid_mapper.py              # HID 键码映射
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
- **格式**: 纯文本命令

### 命令格式

```
# RF4 控制
jig;press_ms;release_ms     # JIG 模式
pull;press_ms;release_ms    # PULL 模式
clear                       # 停止自动按键

# 键盘控制
shift;a                     # Shift+A
ctrl;s                      # Ctrl+S
enter                       # 回车键
```

## 配置说明

主要配置项位于 `src/config.py`：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `WIFI_SSID` | "T" | WiFi 名称 |
| `WIFI_PASSWORD` | "12345678" | WiFi 密码 |
| `RF4_JIG_PRESS_MS` | 1135 | JIG 按压时间 (ms) |
| `RF4_JIG_RELEASE_MS` | 1985 | JIG 释放时间 (ms) |
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

## 依赖

- **MicroPythonBLEHID**: https://github.com/Heerkog/MicroPythonBLEHID.git
- **MicroPython**: v1.23+
- **mpremote**: MicroPython 官方串口工具

详见 [DEPENDENCIES.md](DEPENDENCIES.md)

## 开发

### 目录说明

- `src/boot.py` - ESP32 启动脚本
- `src/main.py` - 应用主入口
- `src/config.py` - 统一配置管理
- `src/keyboard_device.py` / `src/mouse_device.py` - HID 设备封装
- `src/hid_driver.py` / `src/led_driver.py` / `src/msg_queue.py` - 驱动层
- `src/wifi_service.py` / `src/rf4_service.py` - 业务服务
- `src/keyboard_app.py` - 应用逻辑协调器
- `src/hid_mapper.py` - HID 键码映射表

### 添加新功能

1. 在 src/ 目录创建对应模块
2. 在 keyboard_app.py 中集成新模块
3. 添加测试用例到 tests/
4. 更新文档

### 脚本说明

- `scripts/install.py` - 烧录 MicroPython 固件到 ESP32
- `scripts/upload.py` - 使用 mpremote 上传代码到 ESP32
- `scripts/test.py` - 运行单元测试

## 许可证

项目代码采用 GPL-3.0 许可证（与 MicroPythonBLEHID 保持一致）。

## 致谢

- [MicroPythonBLEHID](https://github.com/Heerkog/MicroPythonBLEHID.git) - BLE HID 服务库
