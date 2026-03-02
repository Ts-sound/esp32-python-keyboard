#!/bin/bash
# ESP32 Python Keyboard - Environment Setup Script

set -e

echo "=== ESP32 Python Keyboard Setup ==="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Installing test dependencies..."
    pip install pytest pytest-cov
fi

# Install mpfshell for ESP32 file management
echo "Installing mpfshell..."
pip install mpfshell-lite

# Check esptool
if command -v esptool.py &> /dev/null; then
    echo "esptool.py found: $(esptool.py --version)"
else
    echo "Installing esptool..."
    pip install esptool
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Edit src/config/config.py with your WiFi credentials"
echo "3. Upload code: ./scripts/upload.sh"
