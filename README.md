# mcp-listchange-audit

Offline JSONL checker for MCP traces. It spots tool calls after `notifications/tools/list_changed` but before a fresh `tools/list`, plus traces that end without a refresh.

## Who it helps

MCP client, gateway, and Agent developers debugging dynamic tool discovery. Public reports describe clients that keep stale tools after list-change notifications; this checker turns a captured exchange into a reproducible diagnostic.

## Quick start

Requires Python 3.9+; standard library only.

```console
python mcp_listchange_audit.py examples/stale.jsonl --pretty
```

Exit code is `0` when no finding is present and `1` when the trace contains a finding. It never connects to a server or invokes a tool.

Example JSONL:

```jsonl
{"jsonrpc":"2.0","method":"notifications/tools/list_changed"}
{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"new_tool","arguments":{}}}
{"jsonrpc":"2.0","id":9,"method":"tools/list","params":{}}
```

The first call is reported as `call_before_refresh`; the following list refresh closes the stale window.

## Input and output

Input is one UTF-8 JSON-RPC message per line, captured in wire order. Output is a JSON object with message counts and line-numbered findings. Invalid JSON lines are reported without echoing their contents.

## Limits

This is a conservative trace heuristic. It does not infer whether a particular client UI refreshed, parse SSE framing, correlate server sessions, or prove that a call used a newly introduced tool. Capture one session at a time and include client requests, not only server responses.

## Evidence and rationale

Reports in [MCP Inspector #1292](https://github.com/modelcontextprotocol/inspector/issues/1292), [TypeScript SDK #2964](https://github.com/modelcontextprotocol/typescript-sdk/issues/2964), and [Claude Code #79826](https://github.com/anthropics/claude-code/issues/79826) describe stale or lost list-change refresh behavior. Those issue reports are evidence of reported failures, not prevalence estimates. The [MCP protocol schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/schema.mdx) defines the notification.

## Tests

```console
python -m unittest discover -s tests -v
```

Local verification uses Python 3.11 on Windows; CI is configured for Python 3.11 on Windows and Ubuntu. No runtime dependencies. MIT license; no copied upstream code or assets.
