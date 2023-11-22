# 安装
pip install esptool

# 擦除
esptool.exe  --chip esp32 --port com3 erase_flash

# 写入
esptool.exe --chip esp32 --port com3 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20220117-v1.18.bin

# 添加 ble库
https://github.com/Heerkog/MicroPythonBLEHID