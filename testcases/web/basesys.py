# 为Jenkins提供导包环境配置
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.abspath(os.path.dirname(curPath) + os.path.sep + "..")
sys.path.append(rootPath)