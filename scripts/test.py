#!/usr/bin/env python3
"""ESP32 Python Keyboard - Test Runner Script

Usage:
    python test.py [--verbose] [--no-cov]
"""

import subprocess
import sys
import os


def main():
    print("=== Running Tests ===")
    
    # Check if tests directory exists
    if not os.path.exists("tests"):
        print("Error: tests/ directory not found")
        sys.exit(1)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    
    if "--no-cov" not in sys.argv:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])
    
    if "--verbose" in sys.argv or "-v" in sys.argv:
        cmd.append("-v")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print(f"\nTests failed with code {result.returncode}")
        sys.exit(result.returncode)
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    main()
