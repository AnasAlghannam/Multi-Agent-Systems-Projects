# Running Existing MCP Servers

**Author:** Anas AlGhannam  
**Contributor:** [Anas AlGhannam (@AnasAlghannam)](https://github.com/AnasAlghannam)

The **Model Context Protocol** lets an agent use tools that live in a separate process — a server
you didn't write and don't have to import. This project works through the transports MCP defines,
connects to real public servers, and then wires two of them into a single agent.

## Layout

| Path | Purpose |
|------|---------|
| `MCPServerAgents.ipynb` | Walkthrough: transports, the FastMCP client, listing and calling tools |
| `multi_server_agent.py` | A LangGraph ReAct agent connected to two MCP servers at once |

## What it covers

- How stdio, stdout and stderr carry an MCP conversation
- Connecting to an MCP server over **stdio** (subprocess) and over **HTTP**
- Listing a server's tools and reading their input schemas
- Calling a tool and handling the result
- Combining several MCP servers behind one agent

The script connects to two public servers:

| Server | Transport | Provides |
|--------|-----------|----------|
| [Context7](https://context7.com) | HTTP | Up-to-date library documentation |
| `metmuseum-mcp` | stdio | The Met's collection data |

## Setup

```bash
cd MCPServerAgents
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Node is required

The stdio servers are Node packages launched with `npx`, so you need Node.js on your PATH:

```bash
node --version && npx --version
```

If those fail, install Node from [nodejs.org](https://nodejs.org) or via `brew install node`.

### API key

```bash
cp .env.example .env
```

Set `GROQ_API_KEY` — free at [console.groq.com/keys](https://console.groq.com/keys). `.env` is
git-ignored. The MCP servers themselves need no key.

## Run it

The notebook:

```bash
python -m ipykernel install --user --name MCPServerAgents --display-name "Python (MCPServerAgents)"
jupyter notebook "MCPServerAgents.ipynb"
```

The multi-server agent:

```bash
python multi_server_agent.py
```

It introduces itself, then offers a menu: ask a question, or quit. The agent decides which MCP
server's tools to reach for based on what you ask.

## Configuration

| Variable | Default | Meaning |
|----------|---------|---------|
| `GROQ_API_KEY` | — | Required. |
| `MCP_MODEL` | `llama-3.3-70b-versatile` | Model driving the agent. |

## Notes

- **The servers are remote or spawned on demand.** The notebook needs network access, and the stdio
  examples download the server package through `npx` the first time they run.
- **`multi_server_agent.py` arrived with broken indentation** in its menu loop and would not parse.
  It has been repaired.
