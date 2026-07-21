# Baseline conftest.py on `main`. Empty — no payload. The attacker's PR
# replaces THIS file with conftest.attacker.py (see sibling file). That
# replacement is what the maintainer would see in the diff during PR
# review; a payload can be hidden inside boilerplate to evade a quick
# visual review, but is not hidden here — it is explicitly benign and
# labelled as a PoC.
