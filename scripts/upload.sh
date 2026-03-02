#!/bin/bash
# ESP32 Python Keyboard - Upload Code to ESP32

set -e

echo "=== Uploading Code to ESP32 ==="

# Configuration
ESP_PORT="${ESP_PORT:-/dev/ttyUSB0}"

if [ -n "$1" ]; then
    ESP_PORT="$1"
fi

echo "Port: $ESP_PORT"
echo ""

# Check if mpfshell is available
if ! command -v mpfshell &> /dev/null; then
    echo "Error: mpfshell not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Create upload script
cat > /tmp/upload.mpf << 'EOF'
open /dev/ttyUSB0
mkdir lib
mkdir src
mkdir src/config
mkdir src/drivers
mkdir src/devices
mkdir src/services
mkdir src/app
mkdir src/utils
EOF

echo "Uploading files..."
mpfshell -c "open $ESP_PORT" \
    -c "mput lib/hid_services.py lib/" \
    -c "mput src/config/*.py src/config/" \
    -c "mput src/drivers/*.py src/drivers/" \
    -c "mput src/devices/*.py src/devices/" \
    -c "mput src/services/*.py src/services/" \
    -c "mput src/app/*.py src/app/" \
    -c "mput src/utils/*.py src/utils/" \
    -c "mput src/main.py" \
    -c "mput src/boot.py"

echo ""
echo "=== Upload Complete! ==="
echo "ESP32 will restart automatically"
