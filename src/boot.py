"""
boot.py -- run on boot-up

配置系统路径，初始化基本设置。
"""

import sys

# 添加模块搜索路径
sys.path.insert(0, 'config')
sys.path.insert(0, 'drivers')
sys.path.insert(0, 'devices')
sys.path.insert(0, 'services')
sys.path.insert(0, 'app')
sys.path.insert(0, 'utils')
sys.path.insert(0, 'lib')

print("[BOOT] Path configured")
