# Trivial test so pytest has something to collect (mirrors fairchem's
# tests/core/units/... layout). The presence of any test file causes
# pytest to walk the tree, find conftest.py, and import it — which is
# how the attacker's conftest.py gets executed.
def test_smoke():
    assert True
