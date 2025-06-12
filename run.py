#!/usr/bin/env python3

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kube_context_pyside_gui import main

if __name__ == "__main__":
    print("애플리케이션을 시작합니다...") 
    main()
    print("애플리케이션이 종료되었습니다.")