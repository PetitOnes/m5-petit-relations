"""相手ごとの updated_at(いつ書きかえたか)"""
import importlib
import json
from datetime import datetime

import pytest


@pytest.fixture
def server(tmp_path, monkeypatch):
    monkeypatch.setenv("PETIT_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CHARACTER_ID", "aaa")
    monkeypatch.delenv("RELATIONS_PATH", raising=False)
    monkeypatch.delenv("CHARACTERS_DIR", raising=False)
    import relations_mcp.server as mod
    return importlib.reload(mod)


def _data(server) -> dict:
    return json.loads(server.RELATIONS_PATH.read_text(encoding="utf-8"))


def test_update_stamps_only_that_target(server, monkeypatch):
    monkeypatch.setattr(server, "_now", lambda: "2026-11-14T10:00:00+09:00")
    server.update_relation("bbb", feeling="すき", closeness=0.5)
    monkeypatch.setattr(server, "_now", lambda: "2026-11-15T10:00:00+09:00")
    server.update_relation("ccc", likes=["うた"])
    data = _data(server)
    assert data["bbb"]["updated_at"] == "2026-11-14T10:00:00+09:00"
    assert data["ccc"]["updated_at"] == "2026-11-15T10:00:00+09:00"


def test_empty_call_does_not_move_the_time(server, monkeypatch):
    monkeypatch.setattr(server, "_now", lambda: "2026-11-14T10:00:00+09:00")
    server.update_relation("bbb", feeling="すき")
    monkeypatch.setattr(server, "_now", lambda: "2026-11-20T10:00:00+09:00")
    server.update_relation("bbb")
    assert _data(server)["bbb"]["updated_at"] == "2026-11-14T10:00:00+09:00"


def test_clear_stamps_and_updated_at_cannot_be_cleared(server, monkeypatch):
    monkeypatch.setattr(server, "_now", lambda: "2026-11-14T10:00:00+09:00")
    server.update_relation("bbb", feeling="すき", notes="めも")
    monkeypatch.setattr(server, "_now", lambda: "2026-11-16T10:00:00+09:00")
    server.clear_relation_field("bbb", "notes")
    assert _data(server)["bbb"]["updated_at"] == "2026-11-16T10:00:00+09:00"
    server.clear_relation_field("bbb", "updated_at")
    assert "updated_at" in _data(server)["bbb"]


def test_old_entries_without_time_still_work(server):
    server.RELATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    old = {"bbb": {"feeling": "むかし", "closeness": 0.4}}
    server.RELATIONS_PATH.write_text(json.dumps(old), encoding="utf-8")
    server.update_relation("bbb", closeness=0.6)
    entry = _data(server)["bbb"]
    assert entry["feeling"] == "むかし" and entry["closeness"] == 0.6
    datetime.fromisoformat(entry["updated_at"])
