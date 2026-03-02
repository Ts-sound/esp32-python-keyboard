# WiFi 远程控制协议规格

## 概述

通过 TCP 协议实现对 ESP32 Keyboard 的远程控制，支持 RF4 自动按键和键盘输入。

## 连接信息

| 项目 | 值 |
|------|-----|
| 协议 | TCP |
| 端口 | 80 |
| 地址 | ESP32 IP 地址 |
| 编码 | UTF-8 |

## 命令格式

```
<command>;<param1>;<param2>;...
```

## RF4 控制命令

### jig - JIG 模式

**格式**: `jig;<press_ms>;<release_ms>`

| 参数 | 说明 | 默认值 |
|------|------|--------|
| press_ms | 按压时间 (毫秒) | 1135 |
| release_ms | 释放时间 (毫秒) | 1985 |

**示例**:
```bash
echo "jig;1135;1985" | nc 192.168.1.100 80
```

### pull - PULL 模式

**格式**: `pull;<press_ms>;<release_ms>`

| 参数 | 说明 | 默认值 |
|------|------|--------|
| press_ms | 按压时间 (毫秒) | 800 |
| release_ms | 释放时间 (毫秒) | 500 |

**示例**:
```bash
echo "pull;800;500" | nc 192.168.1.100 80
```

### clear - 停止自动按键

**格式**: `clear`

**示例**:
```bash
echo "clear" | nc 192.168.1.100 80
```

## 键盘控制命令

### 单键

**格式**: `<key>`

| 键名 | 说明 |
|------|------|
| a-z | 字母 |
| 0-9 | 数字 |
| enter | 回车 |
| escape | 退出键 |
| backspace | 退格 |
| space | 空格 |
| f1-f12 | 功能键 |

**示例**:
```bash
echo "a" | nc 192.168.1.100 80
echo "enter" | nc 192.168.1.100 80
```

### 组合键

**格式**: `<modifier>+<key>`

| 修饰符 | 说明 |
|--------|------|
| ctrl | 控制键 |
| shift |  Shift 键 |
| alt | Alt 键 |
| win | Windows 键 |

**示例**:
```bash
echo "ctrl+s" | nc 192.168.1.100 80  # 保存
echo "shift+a" | nc 192.168.1.100 80  # 大写 A
```

### 字符串输入

**格式**: `type:<text>`

**示例**:
```bash
echo "type:Hello World" | nc 192.168.1.100 80
```

## 鼠标控制命令

### move - 鼠标移动

**格式**: `mmove;<x>;<y>`

| 参数 | 范围 | 说明 |
|------|------|------|
| x | -127~127 | X 轴位移 |
| y | -127~127 | Y 轴位移 |

**示例**:
```bash
echo "mmove;50;30" | nc 192.168.1.100 80
```

### click - 鼠标点击

**格式**: `mclick;<button>`

| 按钮 | 说明 |
|------|------|
| left | 左键 |
| right | 右键 |
| middle | 中键 |

**示例**:
```bash
echo "mclick;left" | nc 192.168.1.100 80
```

### scroll - 滚轮滚动

**格式**: `mscroll;<steps>`

| 参数 | 说明 |
|------|------|
| steps | 步数（正数向上，负数向下） |

**示例**:
```bash
echo "mscroll;3" | nc 192.168.1.100 80  # 向上滚动
```

## Python 客户端示例

```python
import socket

def send_command(ip, port, command):
    sock = socket.socket()
    sock.connect((ip, port))
    sock.send(command.encode('utf-8'))
    sock.close()

# JIG 模式
send_command("192.168.1.100", 80, "jig;1000;2000")

# 发送字符串
send_command("192.168.1.100", 80, "type:Hello")

# 停止
send_command("192.168.1.100", 80, "clear")
```

## 错误处理

- 未知命令：ESP32 输出 `[WARN] unknown command`
- 参数错误：ESP32 使用默认值或忽略命令
