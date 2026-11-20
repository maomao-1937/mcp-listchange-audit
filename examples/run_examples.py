import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[1]
run = subprocess.run([sys.executable, str(root / "mcp_listchange_audit.py"),
    str(root / "examples" / "stale.jsonl"), "--pretty"], capture_output=True, text=True, timeout=5)
result = json.loads(run.stdout)
assert run.returncode == 1
assert result["findings"][0]["code"] == "call_before_refresh"
assert result["findings"][0]["line"] == 2
print(json.dumps({"example": "stale trace detected", "finding": result["findings"][0]["code"]}))
