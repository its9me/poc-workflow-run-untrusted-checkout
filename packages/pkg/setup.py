# Innocuous baseline package. NO payload. On real fairchem this file is
# named packages/fairchem-core/setup.py and does the equivalent legit build.
# The attack sink is NOT this file — it is the conftest.py collected by
# pytest below. See tests/units/conftest.py.
from setuptools import setup

setup(name="pkg", version="0.0.0", py_modules=[])
