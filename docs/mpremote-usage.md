# mpremote 使用说明

mpremote 是 MicroPython 官方串口工具，用于与 ESP32 设备交互。

## 常用命令

| 命令 | 说明 |
|------|------|
| `mpremote ls` | 列出设备文件 |
| `mpremote cat <file>` | 查看文件内容 |
| `mpremote rm <file>` | 删除文件 |
| `mpremote cp <local> :<remote>` | 上传文件 |
| `mpremote cp :<remote> <local>` | 下载文件 |
| `mpremote exec "<code>"` | 执行代码 |
| `mpremote reset` | 重启设备 |

## 示例

```bash
# 查看文件列表
mpremote ls

# 查看文件内容
mpremote cat keys.json

# 上传单个文件
mpremote cp src/config.py :config.py

# 上传目录
mpremote cp -r src :src

# 执行代码
mpremote exec "import main; main.test()"

# 重启设备
mpremote reset
```

## 连接指定设备

```bash
# 指定串口
mpremote connect /dev/ttyUSB0 ls

# Windows
mpremote connect COM3 ls
```

## 项目上传脚本

```bash
python scripts/upload.py /dev/ttyUSB0
```