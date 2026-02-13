#!/usr/bin/env python
"""
Minimal setup.py for backwards compatibility.

The primary build configuration is now in pyproject.toml and CMakeLists.txt.
This file is kept only for tools that require setup.py presence.

For new installations, use:
  pip install -e .

Which automatically detects and uses the pyproject.toml configuration.
"""

from setuptools import setup

# Modern builds use pyproject.toml + CMakeLists.txt
# This setup() call is a no-op when build config is in pyproject.toml
setup()
