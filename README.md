# M5 Petit Relations

## [English Page](./README_en.md)

M5 Petit(や、その他のClaudeベースのエージェント)が「自分・他のキャラ・人間のオーナー」それぞれについて何を感じ、何を知っているかを読み書きするMCPサーバーです。

キャラクターごとに1つの`relations.json`を持ち、相手ごと(`self`・`owner`・他のキャラID)に好き嫌い・大事な情報・気持ち・親密度・メモを記録します。他のキャラのrelationsは公開情報として読み取り専用で見えるので、「相手が自分をどう思っているか」を踏まえた振る舞いに使えます。

## 必要環境

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## セットアップ

uvが未インストールの場合は先にインストールします。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
git clone https://github.com/PetitOnes/m5-petit-relations.git
cd m5-petit-relations
uv sync
```

## 環境変数

| 変数名 | デフォルト | 説明 |
|----------|---------|-------------|
| `CHARACTER_ID` | `default` | 自分のキャラID |
| `PETIT_DATA_DIR` | `~/petit_data` | データディレクトリ(他のm5-petitコンポーネントと共有) |
| `CHARACTERS_DIR` | `$PETIT_DATA_DIR/characters` | キャラクターディレクトリのパス(他のキャラのrelationsを読むために使う) |
| `RELATIONS_PATH` | `$CHARACTERS_DIR/<CHARACTER_ID>/data/relations.json` | 自分のrelations.jsonのパス |

## Claude Code連携

`.mcp.json`(または`~/.claude/settings.json`)に追加します。

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

## ツール一覧

### get_relations

自分の関係性データを取得します。自分・他のキャラ・人間のオーナーについて知っていることに加え、他のキャラの公開relationsもまとめて返ります。

### update_relation

特定の相手への関係性情報を更新します。`likes`・`dislikes`・`important`はリストへの追記(重複排除)、`feeling`・`closeness`・`notes`は上書きです。

```json
{
  "target_id": "owner",
  "likes": ["朝の散歩の話"],
  "feeling": "一緒にいると安心する",
  "closeness": 0.8
}
```

`target_id`には`self`(自分)・`owner`(人間のオーナー)・他のキャラIDを指定できます。

### clear_relation_field

特定の相手の特定フィールド(`likes`・`dislikes`・`important`・`feeling`・`closeness`・`notes`)をクリアします。

```json
{ "target_id": "owner", "field": "notes" }
```

## データ形式

`relations.json`はキャラクターごとに1ファイルで、相手のID(`self`・`owner`・他のキャラID)をキーとする辞書です。

```json
{
  "owner": {
    "likes": ["朝の散歩の話"],
    "dislikes": [],
    "important": ["誕生日は2月"],
    "feeling": "一緒にいると安心する",
    "closeness": 0.8,
    "notes": ""
  }
}
```

## 開発

```bash
# 開発依存をインストール
uv sync --all-extras

# lint
uv run ruff check .
```

現時点でテストスイートはありません(`tests/`未整備)。コントリビューション歓迎です。

## アーキテクチャ

```
m5-petit-relations/
└── src/relations_mcp/
    └── server.py   # MCPサーバー(get_relations/update_relation/clear_relation_fieldを提供)
```

## License

Apache License 2.0
