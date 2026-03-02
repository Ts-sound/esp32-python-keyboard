#!/bin/bash
# ESP32 Python Keyboard - Build and Deploy Script

set -e

echo "=== ESP32 Python Keyboard Build ==="

# Configuration
ESP_PORT="${ESP_PORT:-/dev/ttyUSB0}"
ESP_BAUD="${ESP_BAUD:-460800}"

# Check if port is specified
if [ -z "$1" ]; then
    echo "Usage: $0 <serial_port> [firmware]"
    echo "Example: $0 /dev/ttyUSB0"
    echo ""
    echo "Using default port: $ESP_PORT"
fi

if [ -n "$1" ]; then
    ESP_PORT="$1"
fi

# Check if firmware file is specified
FIRMWARE="${2:-ESP32_GENERIC-20240602-v1.23.0.bin}"

echo "Port: $ESP_PORT"
echo "Firmware: $FIRMWARE"
echo ""

# Check if firmware exists
if [ ! -f "$FIRMWARE" ]; then
    echo "Error: Firmware file '$FIRMWARE' not found"
    exit 1
fi

# Erase Flash
echo "Step 1: Erasing Flash..."
esptool.py --chip esp32 --port "$ESP_PORT" erase_flash

# Flash MicroPython
echo "Step 2: Flashing MicroPython..."
esptool.py --chip esp32 --port "$ESP_PORT" --baud "$ESP_BAUD" \
    write_flash -z 0x1000 "$FIRMWARE"

echo ""
echo "=== Flash Complete! ==="
echo "Next: Run ./scripts/upload.sh to upload code"
