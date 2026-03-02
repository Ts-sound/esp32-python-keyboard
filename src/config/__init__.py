"""
ESP32 Keyboard 统一配置模块

所有配置参数集中在此文件中管理。
"""

from micropython import const


# ====================
# WiFi 配置
# ====================
WIFI_SSID = "T"
WIFI_PASSWORD = "12345678"
WIFI_PORT = const(80)
WIFI_TIMEOUT_SEC = const(30)
WIFI_RECONNECT_DELAY_SEC = const(5)
WIFI_SOCKET_TIMEOUT_SEC = const(1800)

# ====================
# RF4 服务配置
# ====================
RF4_JIG_PRESS_MS = const(1135)
RF4_JIG_RELEASE_MS = const(1985)
RF4_PULL_PRESS_MS = const(800)
RF4_PULL_RELEASE_MS = const(500)
RF4_RANDOM_VARIANCE = const(0.1)

# ====================
# HID 配置
# ====================
HID_DEVICE_NAME = "ESP32-Keyboard"
HID_BATTERY_LEVEL_DEFAULT = const(100)
HID_REPORT_INTERVAL_MS = const(20)
HID_ADVERTISING_TIMEOUT_SEC = const(30)

# ====================
# 硬件配置
# ====================
LED_PIN = const(2)
LED_BLINK_COUNT = const(3)
LED_BLINK_INTERVAL_MS = const(200)
LED_HEARTBEAT_INTERVAL_MS = const(1000)

# ====================
# 消息队列配置
# ====================
MSG_QUEUE_MAX_SIZE = const(10)
MSG_QUEUE_DEFAULT_TIMEOUT_MS = const(0)

# ====================
# 系统配置
# ====================
MAIN_LOOP_INTERVAL_MS = const(100)
DEBUG_ENABLED = const(1)
