# M5 Petit Relations

## [日本語ページ](./README.md)

An MCP server that lets M5 Petit (or any other Claude-based agent) read and write how it feels about, and what it knows about, "itself, other characters, and its human owner."

Each character keeps a single `relations.json`, recording likes/dislikes, important facts, feelings, closeness, and notes per counterpart (`self`, `owner`, or another character's ID). Other characters' relations data is exposed as read-only public information, so a character's behavior can take into account how others feel about it.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Setup

Install uv first if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
git clone https://github.com/PetitOnes/m5-petit-relations.git
cd m5-petit-relations
uv sync
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHARACTER_ID` | `default` | This character's ID |
| `PETIT_DATA_DIR` | `~/petit_data` | Data directory (shared with other m5-petit components) |
| `CHARACTERS_DIR` | `$PETIT_DATA_DIR/characters` | Path to the characters directory (used to read other characters' relations) |
| `RELATIONS_PATH` | `$CHARACTERS_DIR/<CHARACTER_ID>/data/relations.json` | Path to this character's own relations.json |

## Claude Code integration

Add to `.mcp.json` (or `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "relations": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/m5-petit-relations", "relations-mcp"],
      "env": {
        "CHARACTER_ID": "petit"
      }
    }
  }
}
```

## Tools

### get_relations

Fetches this character's relationship data - what it knows/feels about itself, other characters, and its human owner - plus every other character's public relations data.

### update_relation

Updates relationship info for a specific counterpart. `likes`, `dislikes`, and `important` are appended to (de-duplicated) lists; `feeling`, `closeness`, and `notes` are overwritten.

```json
{
  "target_id": "owner",
  "likes": ["stories about morning walks"],
  "feeling": "feels safe being together",
  "closeness": 0.8
}
```

`target_id` can be `self`, `owner` (the human owner), or another character's ID.

### clear_relation_field

Clears a specific field (`likes`, `dislikes`, `important`, `feeling`, `closeness`, `notes`) for a specific counterpart.

```json
{ "target_id": "owner", "field": "notes" }
```

## Data format

`relations.json` is one file per character, a dict keyed by counterpart ID (`self`, `owner`, or another character's ID).

```json
{
  "owner": {
    "likes": ["stories about morning walks"],
    "dislikes": [],
    "important": ["birthday is in February"],
    "feeling": "feels safe being together",
    "closeness": 0.8,
    "notes": ""
  }
}
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Lint
uv run ruff check .
```

There is no test suite yet (`tests/` has not been set up). Contributions welcome.

## Architecture

```
m5-petit-relations/
└── src/relations_mcp/
    └── server.py   # MCP server (exposes get_relations/update_relation/clear_relation_field)
```

## License

Apache License 2.0
