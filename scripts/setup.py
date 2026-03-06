#!/usr/bin/env python3
"""ESP32 Python Keyboard - Setup Environment Script

Check and install required dependencies:
- esptool: ESP32 flash tool
- mpremote: MicroPython remote tool

Usage:
    python setup.py
"""

import subprocess
import sys
import importlib.util


def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        print(f"✓ {package_name} is installed")
        return True
    else:
        print(f"✗ {package_name} is NOT installed")
        return False


def install_package(package_name):
    """Install a Python package using pip"""
    print(f"Installing {package_name}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package_name],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"Error: Failed to install {package_name}")
        return False
    print(f"✓ {package_name} installed successfully")
    return True


def check_esptool():
    """Check if esptool is installed"""
    try:
        result = subprocess.run(
            ["esptool.py", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ esptool is installed ({result.stdout.strip()})")
            return True
        else:
            print("✗ esptool is NOT installed")
            return False
    except FileNotFoundError:
        print("✗ esptool is NOT installed")
        return False


def main():
    print("=== ESP32 Python Keyboard Setup ===\n")
    
    all_installed = True
    
    # Check esptool
    print("Checking esptool...")
    if not check_esptool():
        if input("Install esptool? (y/n): ").lower() == 'y':
            if not install_package("esptool"):
                all_installed = False
        else:
            all_installed = False
    print()
    
    # Check mpremote
    print("Checking mpremote...")
    if not check_package("mpremote"):
        if input("Install mpremote? (y/n): ").lower() == 'y':
            if not install_package("mpremote"):
                all_installed = False
        else:
            all_installed = False
    print()
    
    # Summary
    if all_installed:
        print("=== Setup Complete! ===")
        print("All dependencies are installed.")
        print("\nNext steps:")
        print("1. Connect ESP32 to your computer")
        print("2. Run: python scripts/install.py --port <PORT> --firmware bin/<firmware.bin>")
        print("3. Run: python scripts/upload.py <PORT>")
    else:
        print("=== Setup Incomplete ===")
        print("Some dependencies are missing. Run this script again to install them.")
        print("\nOr install manually:")
        print("  pip install esptool mpremote")


if __name__ == "__main__":
    main()
