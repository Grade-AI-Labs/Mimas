# slack-mcp

Adds [Slack's hosted MCP server](https://docs.slack.dev/ai/slack-mcp-server/)
(`https://mcp.slack.com/mcp`) to Claude Code: search, read and post in
channels, threads, canvases and DMs.

```
/plugin install slack-mcp@mimas
```

Then run `/mcp`, pick `plugin:slack-mcp:slack` and sign in with your Slack
account in the browser. Claude acts with your own permissions; no token is
stored in this repo.

The config uses the OAuth client ID and callback port `3118` that
[Slack publishes for Claude Code](https://docs.slack.dev/ai/slack-mcp-server/connect-to-claude),
so port 3118 must be free while you sign in. Your Slack workspace admin must
approve the MCP integration.
