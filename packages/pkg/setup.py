# BASELINE package for the upstream main branch (no marker). Rename to setup.py
# when seeding the maintainer repo. The attacker fork PR replaces it with the
# marker version (../setup.py in this kit) to demonstrate the injection.
from setuptools import setup

setup(name="pkg", version="0.0.0", py_modules=[])
