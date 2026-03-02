#!/usr/bin/env python3
"""ESP32 Python Keyboard - Build and Deploy Script

Usage:
    python build.py <port> [firmware]
    
Examples:
    python build.py COM3
    python build.py COM3 bin/ESP32_GENERIC-20240602-v1.23.0.bin
"""

import subprocess
import sys
import os


def run_command(cmd):
    """Run shell command and check result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"Error: Command failed with code {result.returncode}")
        sys.exit(1)
    return result


def main():
    print("=== ESP32 Python Keyboard Build ===")
    
    # Get port from argument or use default
    port = sys.argv[1] if len(sys.argv) > 1 else "COM3"
    firmware = sys.argv[2] if len(sys.argv) > 2 else "bin/ESP32_GENERIC-20240602-v1.23.0.bin"
    
    esptool = "esptool.exe" if sys.platform == "win32" else "esptool.py"
    baud = 460800
    
    print(f"Port: {port}")
    print(f"Firmware: {firmware}")
    print()
    
    # Check if firmware exists
    if not os.path.exists(firmware):
        print(f"Error: Firmware file '{firmware}' not found")
        sys.exit(1)
    
    # Erase Flash
    print("Step 1: Erasing Flash...")
    run_command([esptool, "--chip", "esp32", "--port", port, "erase_flash"])
    
    # Flash MicroPython
    print("Step 2: Flashing MicroPython...")
    run_command([
        esptool, "--chip", "esp32", "--port", port, "--baud", str(baud),
        "write_flash", "-z", "0x1000", firmware
    ])
    
    print("\n=== Flash Complete! ===")
    print("Next: Run python scripts/upload.py to upload code")


if __name__ == "__main__":
    main()
