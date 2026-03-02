#!/usr/bin/env python3
"""ESP32 Python Keyboard - Upload Code to ESP32

Usage:
    python upload.py [port]
    
Examples:
    python upload.py COM3
    python upload.py /dev/ttyUSB0
"""

import subprocess
import sys
import os


def run_mpfshell(port, commands):
    """Run mpfshell commands"""
    esptool = "mpfshell.exe" if sys.platform == "win32" else "mpfshell"
    
    cmd = [esptool, "-c", f"open {port}"]
    
    for cmd_str in commands:
        cmd.extend(["-c", cmd_str])
    
    print(f"Running mpfshell on {port}...")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    print("=== Uploading Code to ESP32 ===")
    
    # Get port from argument or use default
    port = sys.argv[1] if len(sys.argv) > 1 else "COM3"
    
    print(f"Port: {port}")
    print()
    
    # Check if mpfshell is available
    mpfshell = "mpfshell.exe" if sys.platform == "win32" else "mpfshell"
    try:
        subprocess.run([mpfshell, "--version"], capture_output=True)
    except FileNotFoundError:
        print(f"Error: {mpfshell} not found. Run python scripts/setup.py first")
        sys.exit(1)
    
    # Build upload commands
    commands = [
        "mkdir lib",
        "mkdir src",
        "mkdir src/config",
        "mkdir src/drivers",
        "mkdir src/devices",
        "mkdir src/services",
        "mkdir src/app",
        "mkdir src/utils",
    ]
    
    # Add file upload commands
    if os.path.exists("lib/hid_services.py"):
        commands.append("mput lib/hid_services.py lib/")
    
    if os.path.exists("src/config"):
        commands.append("mput src/config/*.py src/config/")
    
    if os.path.exists("src/drivers"):
        commands.append("mput src/drivers/*.py src/drivers/")
    
    if os.path.exists("src/devices"):
        commands.append("mput src/devices/*.py src/devices/")
    
    if os.path.exists("src/services"):
        commands.append("mput src/services/*.py src/services/")
    
    if os.path.exists("src/app"):
        commands.append("mput src/app/*.py src/app/")
    
    if os.path.exists("src/utils"):
        commands.append("mput src/utils/*.py src/utils/")
    
    if os.path.exists("src/main.py"):
        commands.append("mput src/main.py")
    
    if os.path.exists("src/boot.py"):
        commands.append("mput src/boot.py")
    
    # Execute upload
    return_code = run_mpfshell(port, commands)
    
    if return_code != 0:
        print(f"\nError: Upload failed with code {return_code}")
        sys.exit(1)
    
    print("\n=== Upload Complete! ===")
    print("ESP32 will restart automatically")


if __name__ == "__main__":
    main()
