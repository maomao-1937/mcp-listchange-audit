# Selection evidence

- [MCP Inspector #1292](https://github.com/modelcontextprotocol/inspector/issues/1292) reports that the Tools panel remains stale after `notifications/tools/list_changed` is delivered.
- [MCP TypeScript SDK #2964](https://github.com/modelcontextprotocol/typescript-sdk/issues/2964) reports that a dropped auto-opened subscription stream is not re-opened and list refresh stops.
- [Claude Code #79826](https://github.com/anthropics/claude-code/issues/79826) reports a stale tool list until chat restart.
- [MCP protocol schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-06-18/schema.mdx) defines the notification.

These are public reports, not prevalence estimates. The selection judgment is that deterministic trace checks may help reproduce the reported refresh gap.
