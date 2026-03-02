# LEDDriver - LED 驱动设计

## 概述

控制 ESP32 板载 LED，提供状态指示功能。

## 类结构

```
LEDDriver
└── _pin: machine.Pin
```

## 核心方法

| 方法 | 描述 |
|------|------|
| `on()` | 打开 LED |
| `off()` | 关闭 LED |
| `toggle()` | 切换状态 |
| `blink(count, interval_ms)` | 闪烁指定次数 |
| `heartbeat(interval_ms)` | 心跳闪烁（阻塞） |

## 默认配置

- 引脚：GPIO 2（ESP32 板载 LED）
- 逻辑：高电平点亮

## 使用示例

```python
from drivers.led_driver import LEDDriver

led = LEDDriver(pin=2)

# 开关
led.on()
led.off()

# 闪烁 3 次
led.blink(count=3, interval_ms=200)

# 心跳（每秒一次）
while True:
    led.heartbeat(interval_ms=1000)
```

## 应用场景

| 场景 | 模式 |
|------|------|
| 启动指示 | blink(3) |
| 连接成功 | blink(1) |
| 心跳 | heartbeat(1000) |
| 错误指示 | 快速闪烁 |
