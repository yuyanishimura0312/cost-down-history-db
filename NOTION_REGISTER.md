# Notion App List 登録用テキスト

下記をそのまま Notion の「アプリ一覧」ページ（ID: `332893fe-3a40-81e8-a8b5-df9bd87b0a60`）または「Claude code」ページ（ID: `332893fe-3a40-805f-979b-d0d6ef8d3105`）配下に新規ページとして貼り付けてください。

---

# Cost-Down History DB v1.0

**カテゴリ**: 学術DB / 知識基盤
**ステータス**: 本番公開中
**構築日**: 2026-05-13

## URL

- 公開ダッシュボード: https://yuyanishimura0312.github.io/cost-down-history-db/
- GitHubリポジトリ: https://github.com/yuyanishimura0312/cost-down-history-db
- ローカル: `~/projects/research/cost-down-history-db/`

## 概要

技術・開発のコストダウンに関する歴史的手法を網羅した知識基盤。230年史（1788年Watt遠心調速機から2022年生成AI自動化まで）を15領域に分割し、researcher エージェント x15体の並列バックグラウンド実行で約30分で完了。

## データ構成

| テーブル | 件数 | 内容 |
|---|---|---|
| methods | 158 | 科学的管理法・TPS・Six Sigma・VE・モジュラー設計・Agile・OSS・学習曲線等 |
| evidence | 26 | Ford 65%減・Motorola Six Sigma 160億ドル・PV 700倍減 等 |
| genealogy | 27 | Taylor→Ford→TPS→Lean→Agile→Lean Startup 等の派生関係 |
| critiques | 9 | Braverman労働疎外論・3M Six Sigmaイノベーション阻害・GM Saturn過剰投資 等 |
| domains | 11 | MFG/SW/ENG/SCM/FIN/HW/ENERGY/CONST/RD/LOG/AUTO |

## 15領域

| ID | 領域 | 期間 |
|---|---|---|
| R01 | 科学的管理法・フォーディズム | 1900-1950 |
| R02 | TPS・リーン・JIT | 1950-1990 |
| R03 | TQM・カイゼン・シックスシグマ | 1950-2000 |
| R04 | 価値工学・原価企画 | 1947- |
| R05 | 管理会計・原価計算 | 1920- |
| R06 | アウトソーシング・SCM | 1989- |
| R07 | ムーア則・学習曲線 | 1936- |
| R08 | モジュラー設計・プラットフォーム | 1964- |
| R09 | ソフトウェア開発手法 | 1968- |
| R10 | OSS・クラウド | 1983- |
| R11 | エネルギー学習曲線 | 1976- |
| R12 | 建設プレハブ・モジュラー | 1908- |
| R13 | R&D効率化 | 1935- |
| R14 | 物流・コンテナ化 | 1956- |
| R15 | 自動化・ロボティクス | 1788- |

## 6メカニズム軸

| 軸 | 名称 | 代表 |
|---|---|---|
| M1 | 労働の分解と再構成 | Taylor / Ford / TPS / RPA / 生成AI |
| M2 | 学習効果と規模経済 | Wright / Moore / Swanson / Carlson |
| M3 | 品質の事前組込み | Shewhart / Deming / Taguchi / Six Sigma |
| M4 | 設計時のコスト織込み | VE / Target Costing / DFMA / TCO |
| M5 | 境界の解体と再結合 | コンテナ化 / モジュラー / Outsourcing / SaaS |
| M6 | 情報の自動化と知能化 | NC / PLC / CIM / BIM / AI |

## 構築方法

researcher エージェント x15体 並列バックグラウンド実行（2026-05-13、同日完了）。一次資料URL必須・ハルシネーション排除を品質基準とし、未検証は `verification` フラグで識別。

## スキーマ

5テーブル構造: methods / evidence / genealogy / critiques / domains
SQLite 形式（cdh.sqlite, 106KB）+ HTML ダッシュボード（textbook.htmlスタイル、赤白CI #CC1400、Noto Sans/Serif JP、サイドバー目次、ダークモード対応）

## 引用

```
西村勇也 (2026). Cost-Down History DB v1.0. NPO法人ミラツク.
https://yuyanishimura0312.github.io/cost-down-history-db/
```

## ライセンス

- コード: MIT
- データ: CC BY 4.0

---

## 自動登録の再有効化（任意）

現セッションで Notion MCP サーバーが Claude Code に未登録のため自動登録できませんでした。次回以降の自動化には:

```bash
claude mcp add notion --command "npx" --args "-y,@notionhq/notion-mcp-server" \
  --env "OPENAPI_MCP_HEADERS={\"Authorization\":\"Bearer <新しいntn_トークン>\",\"Notion-Version\":\"2022-06-28\"}"
```

新しい Internal Integration Token は https://www.notion.so/profile/integrations から取得し、対象ページに招待することで自動登録が可能になります。
