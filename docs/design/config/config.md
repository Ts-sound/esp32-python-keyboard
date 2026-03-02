# Config - 配置管理设计

## 概述

统一的配置管理模块，集中管理所有系统参数。

## 配置类别

### WiFi 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `WIFI_SSID` | "T" | WiFi 名称 |
| `WIFI_PASSWORD` | "12345678" | WiFi 密码 |
| `WIFI_PORT` | 80 | TCP 端口 |
| `WIFI_TIMEOUT_SEC` | 30 | 连接超时 (秒) |
| `WIFI_RECONNECT_DELAY_SEC` | 5 | 重连延迟 |
| `WIFI_SOCKET_TIMEOUT_SEC` | 1800 | Socket 超时 |

### RF4 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `RF4_JIG_PRESS_MS` | 1135 | JIG 按压时间 |
| `RF4_JIG_RELEASE_MS` | 1985 | JIG 释放时间 |
| `RF4_PULL_PRESS_MS` | 800 | PULL 按压时间 |
| `RF4_PULL_RELEASE_MS` | 500 | PULL 释放时间 |
| `RF4_RANDOM_VARIANCE` | 0.1 | 随机方差 (10%) |

### HID 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `HID_DEVICE_NAME` | "ESP32-Keyboard" | BLE 设备名 |
| `HID_BATTERY_LEVEL_DEFAULT` | 100 | 默认电量 |
| `HID_REPORT_INTERVAL_MS` | 20 | 报告间隔 |
| `HID_ADVERTISING_TIMEOUT_SEC` | 30 | 广播超时 |

### 硬件配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `LED_PIN` | 2 | LED 引脚 |
| `LED_BLINK_COUNT` | 3 | 启动闪烁次数 |
| `LED_BLINK_INTERVAL_MS` | 200 | 闪烁间隔 |
| `LED_HEARTBEAT_INTERVAL_MS` | 1000 | 心跳间隔 |

### 消息队列配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MSG_QUEUE_MAX_SIZE` | 10 | 队列最大长度 |
| `MSG_QUEUE_DEFAULT_TIMEOUT_MS` | 0 | 默认超时 |

### 系统配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MAIN_LOOP_INTERVAL_MS` | 100 | 主循环间隔 |
| `DEBUG_ENABLED` | 1 | 调试开关 |

## 使用方式

```python
from config.config import WIFI_SSID, WIFI_PASSWORD

print(f"Connecting to {WIFI_SSID}...")
```

## 常量定义

使用 `micropython.const()` 定义编译时常量：
```python
from micropython import const
LED_PIN = const(2)
```

## 修改配置

编辑 `src/config/config.py`，修改后重新上传到 ESP32。
