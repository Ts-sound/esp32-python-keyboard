#!/usr/bin/env python3
"""ESP32 Python Keyboard - Upload Code to ESP32 using mpremote
Supports recursive upload with force overwrite (cp -rf)
Uploads:
  - boot.py (to device root /boot.py)
  - src/ directory (main.py and all modules)
  - lib/MicroPythonBLEHID/hid_services.py
  - lib/MicroPythonBLEHID/hid_keystores.py
Usage:
    python upload.py [port]
    
Examples:
    python upload.py COM3
    python upload.py /dev/ttyUSB0
"""

import subprocess
import sys
import os
import platform


def run_mpremote_command(port, command):
    """
    Execute a single mpremote command on the specified serial port
    
    Args:
        port (str): Serial port identifier (e.g., COM3, /dev/ttyUSB0)
        command (str): mpremote subcommand to execute (e.g., "cp -rf src :/src")
    
    Returns:
        int: Return code from the subprocess call (0 = success, non-zero = error)
    """
    mpremote_cmd = ["mpremote", "connect", port] + command.split()
    
    print(f"Executing: {' '.join(mpremote_cmd)}")
    result = subprocess.run(
        mpremote_cmd,
        capture_output=True,
        text=True
    )
    
    # Print output (both stdout and stderr for mpremote)
    output = result.stdout.strip() + result.stderr.strip()
    if output:
        print(f"  {output}")
    
    return result.returncode


def main():
    print("=== Uploading Code to ESP32 (mpremote - recursive force overwrite) ===")
    
    # Get serial port (default: Windows=COM3, Linux/Mac=/dev/ttyUSB0)
    default_port = "COM3" if platform.system() == "Windows" else "/dev/ttyUSB0"
    port = sys.argv[1] if len(sys.argv) > 1 else default_port
    
    print(f"Target Port: {port}")
    print()
    
    # Check if mpremote is installed
    try:
        subprocess.run(
            ["mpremote", "--version"],
            capture_output=True,
            check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: mpremote not found. Please install it first with:")
        print("pip install mpremote")
        sys.exit(1)
    
    # Step 1: Upload files with force overwrite
    print("\n=== Uploading files (force overwrite) ===")
    upload_errors = False
    
    # 1. Upload boot.py to device root
    if os.path.exists("boot.py"):
        print("Uploading boot.py...")
        rc = run_mpremote_command(port, "cp -f boot.py :/boot.py")
        if rc != 0:
            upload_errors = True
    else:
        print("Warning: boot.py not found, skip uploading this file")
    
    # 2. Upload src directory (excluding boot.py)
    if os.path.exists("src"):
        print("Uploading src/ directory...")
        rc = run_mpremote_command(port, "cp -rf src :/")
        if rc != 0:
            upload_errors = True
    
    # 3. Upload lib/MicroPythonBLEHID/hid_services.py and hid_keystores.py
    print("Uploading lib/MicroPythonBLEHID/ files...")
    
    # Create /lib directory (ignore error if exists)
    run_mpremote_command(port, "fs mkdir /lib")
    
    # Create /lib/MicroPythonBLEHID directory (ignore error if exists)
    run_mpremote_command(port, "fs mkdir /lib/MicroPythonBLEHID")
    
    for filename in ["hid_services.py", "hid_keystores.py"]:
        filepath = f"lib/MicroPythonBLEHID/{filename}"
        if os.path.exists(filepath):
            print(f"  Uploading {filename}...")
            rc = run_mpremote_command(port, f"cp -f {filepath} :/lib/MicroPythonBLEHID/{filename}")
            if rc != 0:
                upload_errors = True
        else:
            print(f"  Warning: {filename} not found")
    
    # Step 2: Final status check
    if upload_errors:
        print("\n=== Upload Completed with Errors! ===")
        sys.exit(1)
    else:
        print("\n=== Upload Complete! ===")
        print("1. boot.py uploaded to device root")
        print("2. src/ directory uploaded (main.py, all modules)")
        print("3. lib/MicroPythonBLEHID/ files uploaded (hid_services.py, hid_keystores.py)")
        print("Restarting ESP32...")
        run_mpremote_command(port, "reset")


if __name__ == "__main__":
    main()