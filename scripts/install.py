#!/usr/bin/env python3
"""ESP32 Python Keyboard - Install and Flash Script

Usage:
    python install.py [--port COM3] [--baud 460800] [--firmware <bin_file>]
    
Examples:
    python install.py --port COM3
    python install.py --port COM3 --firmware bin/ESP32_GENERIC-20240602-v1.23.0.bin
"""

import argparse
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


def erase_flash(port, baud):
    """Erase ESP32 flash"""
    print("\n=== Erasing Flash ===")
    cmd = [
        "esptool.exe" if sys.platform == "win32" else "esptool.py",
        "--chip", "esp32",
        "--port", port,
        "erase_flash"
    ]
    run_command(cmd)
    print("Flash erased successfully!")


def write_flash(port, baud, firmware):
    """Write firmware to ESP32"""
    print(f"\n=== Writing Firmware: {firmware} ===")
    
    if not os.path.exists(firmware):
        print(f"Error: Firmware file '{firmware}' not found")
        sys.exit(1)
    
    cmd = [
        "esptool.exe" if sys.platform == "win32" else "esptool.py",
        "--chip", "esp32",
        "--port", port,
        "--baud", str(baud),
        "write_flash", "-z", "0x1000", firmware
    ]
    run_command(cmd)
    print("Firmware written successfully!")


def main():
    parser = argparse.ArgumentParser(description="ESP32 Install and Flash Tool")
    parser.add_argument("--port", default="COM3", help="Serial port (e.g., COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=460800, help="Baud rate (default: 460800)")
    parser.add_argument("--firmware", default=None, help="Firmware bin file")
    parser.add_argument("--erase", action="store_true", help="Only erase flash")
    
    args = parser.parse_args()
    
    print("=== ESP32 Python Keyboard Install ===")
    print(f"Port: {args.port}")
    print(f"Baud: {args.baud}")
    
    if args.erase:
        erase_flash(args.port, args.baud)
        return
    
    if not args.firmware:
        print("\nAvailable firmware in bin/:")
        bin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")
        if os.path.exists(bin_dir):
            for f in os.listdir(bin_dir):
                if f.endswith(".bin"):
                    print(f"  - bin/{f}")
        print("\nPlease specify --firmware <file>")
        sys.exit(1)
    
    erase_flash(args.port, args.baud)
    write_flash(args.port, args.baud, args.firmware)
    
    print("\n=== Install Complete! ===")
    print("Press reset button on ESP32 to boot")


if __name__ == "__main__":
    main()
