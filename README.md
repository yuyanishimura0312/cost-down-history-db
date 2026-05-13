# Cost-Down History DB (CDH-DB)

技術・開発のコストダウンに関する歴史的手法を網羅した知識基盤。

**Live**: https://yuyanishimura0312.github.io/cost-down-history-db/

## 概要

230年史（1788年Watt遠心調速機から2022年生成AI自動化まで）を15領域に分割し、researcher エージェント x15体の並列バックグラウンド実行で網羅収集した。

- **methods**: 158手法（科学的管理法・TPS・Six Sigma・VE・モジュラー設計・Agile・OSS・学習曲線等）
- **evidence**: 26件の数値実証（Ford 65%減・Motorola Six Sigma 160億ドル・PV 700倍減 等）
- **genealogy**: 27件の派生関係（Taylor→Ford→TPS→Lean→Agile→Lean Startup 等）
- **critiques**: 9件の批判（Braverman労働疎外論・3M Six Sigmaイノベーション阻害・GM Saturn過剰投資 等）
- **domains**: 11領域（MFG/SW/ENG/SCM/FIN/HW/ENERGY/CONST/RD/LOG/AUTO）
- **mechanism axes**: 6軸（労働分解・学習効果・品質組込み・設計コスト織込み・境界解体・情報知能化）

## 構造

```
.
├── cdh.sqlite                 # SQLite DB本体
├── INTEGRATED_REPORT.md       # 統合レポート（15領域横断分析）
├── PROGRESS.md                # 構築進捗
├── SCHEMA_DRAFT.md            # スキーマ初期版
├── docs/
│   └── index.html             # ダッシュボード（GitHub Pages）
└── scripts/
    ├── build_db.py            # SQLite DB生成
    └── build_dashboard.py     # ダッシュボードHTML生成
```

## 使い方

### SQLite から検索

```bash
sqlite3 cdh.sqlite "SELECT method_id, name_ja, era_start FROM methods WHERE mechanism_axis='M2' ORDER BY era_start;"
```

### 領域別取得

```sql
SELECT m.name_ja, m.originator, m.era_start
FROM methods m
WHERE m.domain_code = 'MFG'
ORDER BY m.era_start;
```

### 系譜の追跡

```sql
SELECT p.name_ja AS parent, c.name_ja AS child, g.rel_type, g.year_transition
FROM genealogy g
JOIN methods p ON g.parent_method_id = p.method_id
JOIN methods c ON g.child_method_id = c.method_id
ORDER BY g.year_transition;
```

## スキーマ

5テーブル構造（methods / evidence / genealogy / critiques / domains）。詳細は `scripts/build_db.py` 参照。

## 品質ルール

- すべての手法に `primary_source_url` 必須
- 数値実証は出典URL付きで `evidence` テーブルに登録
- ハルシネーション排除を品質基準とし、未検証は `verification` フラグで識別
- 一次資料優先、Wikipedia は補助

## 引用

```
西村勇也 (2026). Cost-Down History DB v1.0. NPO法人ミラツク.
https://yuyanishimura0312.github.io/cost-down-history-db/
```

## ライセンス

MIT (コード) / CC BY 4.0 (データ)

## クレジット

NPO法人ミラツク / 西村勇也  
リサーチ: Claude Opus 4.7 researcher エージェント x15体 並列バックグラウンド
