# 项目依赖

## 运行时依赖

### MicroPythonBLEHID

BLE HID 服务库，提供 Keyboard、Mouse、Joystick 等 BLE HID 设备实现。

- **来源**: https://github.com/Heerkog/MicroPythonBLEHID.git
- **位置**: `lib/hid_services.py`
- **许可证**: GPL-3.0
- **版本**: 当前使用主分支最新代码

### 添加依赖

```bash
# 方式 1: 使用 git submodule（推荐）
git submodule add https://github.com/Heerkog/MicroPythonBLEHID.git lib/MicroPythonBLEHID
git submodule update --init --recursive

# 方式 2: 手动复制（当前采用）
# 已将 hid_services.py 复制到 lib/ 目录
```

## 部署到 ESP32

### 使用 esptool 烧录固件

```bash
# 擦除 Flash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# 烧录 MicroPython 固件
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin
```

### 上传代码

```bash
# 使用 mpfshell
mpfshell -c "open /dev/ttyUSB0" -c "mput -r lib/" -c "mput -r src/"

# 或使用 rshell
rshell -p /dev/ttyUSB0 cp -r lib/ src/ /pyboard/
```

## 开发依赖

| 工具 | 用途 | 安装 |
|------|------|------|
| esptool | ESP32 固件烧录 | `pip install esptool` |
| mpfshell | MicroPython 文件传输 | `pip install mpfshell` |
| rshell | MicroPython REPL | `pip install rshell` |

## 固件版本要求

- **最低版本**: MicroPython v1.18
- **推荐版本**: MicroPython v1.23+
- **蓝牙支持**: 需要 BLE 支持的 ESP32 固件
