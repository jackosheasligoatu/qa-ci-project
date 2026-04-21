import subprocess

import sys

TESTS = [

    "tests/test_login.py",

    "tests/test_deposit.py",

    "tests/test_withdrawal.py",

    "tests/test_gameplay.py",

]

for test in TESTS:

    print(f"\n▶ Running {test} ...")

    result = subprocess.run([sys.executable, test])

    if result.returncode != 0:

        print(f"❌ Failed: {test}")

        sys.exit(result.returncode)

print("\n✅ All tests passed")
