# PHP Code Review Guide

> PHPコードレビューガイド。型宣言、厳密な比較、例外処理、テスト、パフォーマンス最適化などの重要テーマを網羅。

## 目次

- 型宣言・PHPDoc
- 厳密な比較と型安全
- 例外処理
- よくある落とし穴
- テストのベストプラクティス
- パフォーマンス最適化
- コードスタイル
- レビューチェックリスト

---

## 型宣言・PHPDoc

### 基本

```php
// Bad: 型宣言なし
function processData($data, $count) {
    return substr($data, 0, $count);
}

// Good: 引数と戻り値に型宣言あり (PHP 7.0+)
function processData(string $data, int $count): string {
    return substr($data, 0, $count);
}
```

### 配列（コレクション）の型指定

PHP本体は配列の中身の型まで強制できないため、静的解析（PHPStanなど）やIDE向けにPHPDocを記述します。

```php
// Bad: 中身の型が不明
function getNames(array $users): array {
    return array_map(fn($u) => $u->name, $users);
}

// Good: PHPDocで配列の要素型を明示
/**
 * @param User[] $users
 * @return string[]
 */
function getNames(array $users): array {
    return array_map(fn(User $u): string => $u->name, $users);
}
```

---

## 厳密な比較と型安全

PHPの緩い比較（暗黙の型変換）による意図しないバグを防ぎます。

```php
// Bad: 緩い比較（0 == '0' や 0 == false が true になってしまう）
if ($status == 1) { ... }
if (strpos($text, 'a') == false) { ... } // 先頭(インデックス0)に'a'がある場合もtrueになる

// Good: 厳密な比較 (===, !==) を使用
if ($status === 1) { ... }
if (strpos($text, 'a') === false) { ... }
```

---

## 例外処理

```php
// Bad: 例外を握りつぶす
try {
    $result = $this->riskyOperation();
} catch (\Throwable $e) {
    // 何もしない
}

// Good: 具体的な例外をキャッチし、ログ記録やリスローを行う
try {
    $result = $this->riskyOperation();
} catch (\InvalidArgumentException $e) {
    $this->logger->error($e->getMessage());
    throw $e;
}
```

---

## よくある落とし穴

### isset, empty の誤用

```php
// Bad: 0 や '0', false も空と判定されてしまう
if (empty($request['point'])) {
    $point = 10; // ユーザーが 0 を送信した場合も 10 に上書きされる
}

// Good: Null合体演算子 (??) を使うか、厳密に判定する
$point = $request['point'] ?? 10;

// 条件分岐が必要な場合
if (!isset($request['point']) || $request['point'] === '') { ... }
```

---

## テスト (PHPUnit)

```php
// Good
public function testUserCreation(): void
{
    $user = new User('test@example.com');
    
    // assertEqual (==) ではなく assertSame (===) を使用する
    $this->assertSame('test@example.com', $user->getEmail());
}
```

---

## パフォーマンス

### ループ内の重い処理

```php
// Bad: ループの評価のたびに count() が実行される
for ($i = 0; $i < count($items); $i++) {
    echo $items[$i];
}

// Good: foreach を使うか、事前に件数を変数に入れる
foreach ($items as $item) {
    echo $item;
}
```

### in_array の計算量と厳密比較

```php
// Bad: in_array は O(N) の計算量がかかる。第3引数がないと緩い比較になる。
if (in_array($id, $largeArray)) { ... }

// Good: strict モード(第3引数をtrue)を有効にする
if (in_array($id, $largeArray, true)) { ... }

// Best (巨大な配列の場合): キーによる探索 (O(1)) を使う
$lookup = array_flip($largeArray);
if (isset($lookup[$id])) { ... }
```

---

## コードスタイル

* PSR-12 に準拠していること
* ファイルの先頭に `declare(strict_types=1);` を記述することを推奨
* クラス、メソッドには適切な docstring (PHPDoc) を書く

---

## Review Checklist

### 型安全・厳格性

- [ ] `declare(strict_types=1);` が宣言されている
- [ ] 関数・メソッドの引数と戻り値に型宣言がある
- [ ] 配列要素の型を示すPHPDoc（`@param Type[]`など）が適切に記述されている

### ロジック・比較

- [ ] `==` ではなく `===` (厳密な比較) を使用している
- [ ] `empty()` の挙動（`0`や`false`の評価）に起因するバグはない
- [ ] null合体演算子 (`??`) や null safe 演算子 (`?->`) を適切に活用している

### 例外処理

- [ ] 例外を握りつぶしている（空のcatch）箇所はない
- [ ] `\Exception` などの汎用例外ではなく、具体的な例外を捕捉・送出している

### テスト

- [ ] カバレッジが十分にある
- [ ] 境界値やエッジケースがテストされている
- [ ] PHPUnitのアサーションに `assertSame` などを適切に使用している

### スタイル・パフォーマンス

- [ ] 命名規約（PSR）に従っている
- [ ] ループ内での `count()` や、DBの N+1 クエリが発生していない
- [ ] `in_array` の第3引数（strictモード）を指定している
