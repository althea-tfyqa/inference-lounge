#!/usr/bin/env python
"""
Pre-commit hook script to ensure DEVELOPER_TOOLS is disabled before committing.
"""

import sys
from pathlib import Path


def main():
    config_path = Path("config.py")
    
    if not config_path.exists():
        # config.py not in this commit, that's fine
        return 0
    
    content = config_path.read_text()
    
    if "DEVELOPER_TOOLS = True" in content:
        print()
        print("  ❌ COMMIT BLOCKED")
        print("  ─────────────────────────────────────────────")
        print("  DEVELOPER_TOOLS is set to True in config.py")
        print()
        print("  Please change it to False before committing:")
        print("    DEVELOPER_TOOLS = False")
        print()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())