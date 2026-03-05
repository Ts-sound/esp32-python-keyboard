"""
boot.py -- run on boot-up
"""

import sys

sys.path.insert(0, 'config')
sys.path.insert(0, 'drivers')
sys.path.insert(0, 'devices')
sys.path.insert(0, 'services')
sys.path.insert(0, 'app')
sys.path.insert(0, 'utils')
sys.path.insert(0, 'lib')

print("[BOOT] Path configured")
