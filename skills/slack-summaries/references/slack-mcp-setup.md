# Slack MCP Server — Setup Guide

This guide explains how to connect the Slack MCP server to Claude Code so that the `/slack-summaries` skill can read your messages.

---

## What is the Slack MCP server?

The Slack MCP (Model Context Protocol) server is an official integration that gives Claude Code direct, read access to your Slack workspace — channels, DMs, and threads — without you having to export anything manually.

---

## Step 1: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) and click **Create New App**
2. Choose **From scratch**
3. Name it something like `Claude MCP` and select your Ersilia workspace
4. Click **Create App**

---

## Step 2: Configure OAuth Scopes

In your app settings, go to **OAuth & Permissions** → **Scopes** → **User Token Scopes** and add:

| Scope | Purpose |
|-------|---------|
| `channels:history` | Read public channel messages |
| `channels:read` | List public channels |
| `groups:history` | Read private channel messages |
| `groups:read` | List private channels |
| `im:history` | Read direct messages |
| `im:read` | List direct message conversations |
| `mpim:history` | Read group direct messages |
| `mpim:read` | List group direct message conversations |
| `search:read` | Search messages (used for mention detection) |
| `users:read` | Look up user info by ID |

> **Note**: Use **User Token Scopes** (not Bot Token Scopes) so the skill sees messages as you, including DMs.

---

## Step 3: Install the App to Your Workspace

1. In your app settings, go to **OAuth & Permissions**
2. Click **Install to Workspace**
3. Review and authorise the requested permissions
4. Copy the **User OAuth Token** (starts with `xoxp-`)

---

## Step 4: Add the MCP Server to Claude Code

Run this command in your terminal:

```bash
claude mcp add slack-mcp-server \
  -e SLACK_BOT_TOKEN=xoxp-your-token-here \
  -- npx -y @modelcontextprotocol/server-slack
```

Or, if you prefer to configure it manually, add this to your `~/.claude.json` under `mcpServers`:

```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "xoxp-your-token-here"
  }
}
```

Replace `xoxp-your-token-here` with the User OAuth Token from Step 3.

---

## Step 5: Verify the Connection

Start a new Claude Code session and run:

```
/slack-summaries --since 1d
```

If the connection is working, Claude will list your channels and begin fetching messages.

If you see an error like `tool not found: slack_list_channels`, double-check that the MCP server was added correctly and restart Claude Code.

---

## Troubleshooting

**"Missing scope" errors**: Return to Step 2 and add the missing scope, then reinstall the app to your workspace (Step 3) to get a new token.

**"Channel not found" errors**: The token may not have access to private channels you're not a member of — this is expected and safe to ignore.

**Token expired**: Slack user tokens don't expire automatically, but if you revoke and reinstall the app, you'll need to update the token in your MCP config.

---

## Security Note

Your Slack token gives read access to your messages. Keep it private — do not commit it to any repository. Store it only in your local Claude Code config (`~/.claude.json`) or as an environment variable.
