#!/usr/bin/env python3
"""ESP32 Python Keyboard - Environment Setup Script

Usage:
    python setup.py [--venv venv] [--no-mpfshell]
"""

import subprocess
import sys
import os
import venv


def run_command(cmd, capture=False):
    """Run shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if not capture:
        return result
    return result


def check_python():
    """Check Python version"""
    print("Checking Python version...")
    result = run_command([sys.executable, "--version"], capture=True)
    print(result.stdout.strip())


def create_venv(venv_path="venv"):
    """Create virtual environment if not exists"""
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists at {venv_path}")
        return
    
    print(f"Creating virtual environment at {venv_path}...")
    venv.create(venv_path, with_pip=True)
    print("Virtual environment created!")


def get_pip_path(venv_path="venv"):
    """Get pip executable path"""
    if sys.platform == "win32":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    return os.path.join(venv_path, "bin", "pip")


def install_requirements(pip_path):
    """Install dependencies"""
    if os.path.exists("requirements.txt"):
        print("Installing dependencies from requirements.txt...")
        run_command([pip_path, "install", "-r", "requirements.txt"])
    else:
        print("Installing test dependencies...")
        run_command([pip_path, "install", "pytest", "pytest-cov"])


def install_mpfshell(pip_path):
    """Install mpfshell-lite"""
    print("Installing mpfshell-lite...")
    run_command([pip_path, "install", "mpfshell-lite"])


def check_esptool():
    """Check if esptool is available"""
    esptool = "esptool.exe" if sys.platform == "win32" else "esptool.py"
    print("Checking esptool...")
    
    try:
        result = subprocess.run([esptool, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"esptool found: {result.stdout.strip()}")
            return
    except FileNotFoundError:
        pass
    
    print("esptool not found, installing...")
    pip_path = get_pip_path()
    run_command([pip_path, "install", "esptool"])


def main():
    print("=== ESP32 Python Keyboard Setup ===")
    
    check_python()
    create_venv()
    
    pip_path = get_pip_path()
    install_requirements(pip_path)
    install_mpfshell(pip_path)
    check_esptool()
    
    print("\n=== Setup Complete! ===")
    print()
    print("Next steps:")
    if sys.platform == "win32":
        print("1. Activate venv: venv\\Scripts\\activate")
    else:
        print("1. Activate venv: source venv/bin/activate")
    print("2. Edit src/config/config.py with your WiFi credentials")
    print("3. Upload code: python scripts/upload.py")


if __name__ == "__main__":
    main()
