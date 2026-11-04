# atlassian-mcp

Adds [Atlassian's hosted Rovo MCP server](https://github.com/atlassian/atlassian-mcp-server) v2
(`https://mcp.atlassian.com/v2/mcp`) to Claude Code: Jira, Confluence and
Compass tools.

```
/plugin install atlassian-mcp@mimas
```

Then run `/mcp`, pick `plugin:atlassian-mcp:atlassian` and sign in with your
Atlassian account in the browser. Claude acts with your own permissions; no
token is stored in this repo.

Your Atlassian site admin must allow the Rovo MCP server for the site.
