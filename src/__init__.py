import os
import sys
import tomllib
from pathlib import Path

def _get_version():
    """Read version from pyproject.toml"""
    try:
        # Find pyproject.toml in the project root
        current_dir = Path(__file__).parent
        while current_dir != current_dir.parent:
            pyproject_path = current_dir / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                return data["project"]["version"]
            current_dir = current_dir.parent
        
        # Fallback if pyproject.toml not found
        return "0.1.0"
    except Exception:
        # Fallback in case of any error
        return "0.1.0"

__version__ = _get_version()
