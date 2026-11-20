#!/usr/bin/env python3
"""Audit MCP JSON-RPC JSONL traces for stale tool-list refreshes."""
import argparse
import json
import sys
from pathlib import Path


def audit(lines):
    pending = []
    findings = []
    counts = {"notifications": 0, "list_requests": 0, "tool_calls": 0}
    for number, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        try:
            message = json.loads(raw)
        except json.JSONDecodeError:
            findings.append({"code": "invalid_jsonl", "line": number, "message": "line is not valid JSON"})
            continue
        if not isinstance(message, dict):
            findings.append({"code": "invalid_message", "line": number, "message": "JSON value is not an object"})
            continue
        method = message.get("method")
        if method == "notifications/tools/list_changed":
            counts["notifications"] += 1
            pending.append({"line": number, "calls": []})
        elif method == "tools/list" and "id" in message:
            counts["list_requests"] += 1
            pending.clear()
        elif method == "tools/call" and "id" in message:
            counts["tool_calls"] += 1
            params = message.get("params")
            name = params.get("name") if isinstance(params, dict) else None
            for notice in pending:
                notice["calls"].append({"line": number, "tool": name})
                findings.append({"code": "call_before_refresh", "notification_line": notice["line"],
                    "line": number, "tool": name,
                    "message": "tool call occurred after list_changed and before a new tools/list request"})
    for notice in pending:
        if not notice["calls"]:
            findings.append({"code": "missing_refresh", "notification_line": notice["line"],
                "message": "trace ended without a subsequent tools/list request"})
    return {"summary": counts, "findings": findings, "ok": not findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", nargs="?", default="-", help="JSONL file, or - for stdin")
    parser.add_argument("--pretty", action="store_true", help="indent JSON output")
    args = parser.parse_args(argv)
    try:
        if args.trace == "-":
            result = audit(sys.stdin)
        else:
            with Path(args.trace).open(encoding="utf-8") as source:
                result = audit(source)
    except OSError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
