# Python Code Review Guide

> Pythonコードレビューガイド。型注釈、async/await、テスト、例外処理、パフォーマンス最適化などの重要テーマを網羅。

## 目次

- 型注釈
- 非同期プログラミング
- 例外処理
- よくある落とし穴
- テストのベストプラクティス
- パフォーマンス最適化
- コードスタイル
- レビューチェックリスト

---

## 型注釈

### 基本

```python
# Bad: 型注釈なし
def process_data(data, count):
    return data[:count]

# Good: 型注釈あり
def process_data(data: str, count: int) -> str:
    return data[:count]
```

### コンテナ型

```python
from typing import List, Dict, Sequence

# Bad
def get_names(users: list) -> list:
    return [u.name for u in users]

# Good
def get_names(users: List[User]) -> List[str]:
    return [u.name for u in users]

def process_items(items: Sequence[str]) -> int:
    return len(items)
```

---

## 非同期プログラミング

### 基本

```python
# Bad: 同期で逐次実行
def fetch_all_sync(urls):
    return [requests.get(url).text for url in urls]

# Good: 非同期で並列実行
async def fetch_all(urls):
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)
```

---

## 例外処理

```python
# Bad
try:
    result = risky_operation()
except:
    pass

# Good
try:
    result = risky_operation()
except ValueError as e:
    logger.error(e)
    raise
```

---

## よくある落とし穴

### 可変デフォルト引数

```python
# Bad
def add_item(item, items=[]):
    items.append(item)
    return items

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## テスト

```python
# Good
def test_user_creation():
    user = User(email="test@example.com")
    assert user.email == "test@example.com"
```

---

## パフォーマンス

```python
# Bad
result = ""
for item in items:
    result += str(item)

# Good
result = "".join(str(item) for item in items)
```

---

## コードスタイル

* 命名は一貫性を持つ
* docstring を書く

---

## Review Checklist

### 型安全

* 関数に型注釈がある
* Optionalの使用が適切

### 非同期

* async/awaitが正しく使われている
* ブロッキング処理がない

### 例外処理

* 適切な例外を捕捉している
* エラー情報が失われていない

### データ構造

* 可変デフォルト引数を使っていない

### テスト

* カバレッジが十分
* エッジケースがテストされている

### スタイル

* 命名が明確

### パフォーマンス

* 無駄なループがない
* 適切なデータ構造を使用
