# atlassian-mcp

Adds [Atlassian's hosted Rovo MCP server](https://github.com/atlassian/atlassian-mcp-server)
(`https://mcp.atlassian.com/v1/mcp`) to Claude Code: Jira, Confluence and
Compass tools.

The URL is the one the Atlassian connector in the Claude directory uses, so on
claude.ai and in Cowork the plugin reuses that connector instead of adding a
new one that a claude.ai Owner has to approve. Atlassian serves its v2 tools
on this URL too.

```
/plugin install atlassian-mcp@mimas
```

Then run `/mcp`, pick `plugin:atlassian-mcp:atlassian` and sign in with your
Atlassian account in the browser. Claude acts with your own permissions; no
token is stored in this repo.

Your Atlassian site admin must allow the Rovo MCP server for the site.
