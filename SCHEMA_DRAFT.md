# Cost-Down History DB — Schema Draft v0.1

10領域受領時点のスキーマ骨格。残り5領域完了後に確定版へ更新する。

---

## 設計方針

学術DB方法論（feedback_large_scale_academic_db_methodology.md）準拠の7フェーズ。
- Phase 0 スコーピング → 15領域確定
- Phase 1 調査設計 → 各領域20-30項目目標
- Phase 2 並列収集 → 進行中（10/15完了）
- Phase 3 検証 → 未着手
- Phase 4 関係抽出 → 未着手
- Phase 5 ダッシュボード → 未着手（textbook.htmlスタイル）

データソース品質: source_url必須、一次資料優先、ハルシネーション禁止。

---

## テーブル設計

### 1. methods（中核手法テーブル）

| カラム | 型 | 説明 |
|--------|-----|------|
| method_id | TEXT PK | CDH-MET-XXXX |
| name_ja | TEXT | 日本語名 |
| name_en | TEXT | 英語名 |
| domain | TEXT | 領域コード（MFG/SW/ENG/SCM/FIN/HW/ENERGY/CONST/RD/LOG/AUTO） |
| era_start | INT | 発祥年 |
| era_end | INT | 主導年代終了 |
| originator | TEXT | 提唱者 |
| origin_org | TEXT | 発祥組織 |
| origin_country | TEXT | 発祥国 |
| primary_source_url | TEXT | 一次資料URL |
| mechanism | TEXT | コスト削減メカニズム（地の文） |
| status | TEXT | active / mature / declining / legacy |
| verification | TEXT | verified / unverified / requires_review |

### 2. evidence（実証データテーブル）

| カラム | 型 | 説明 |
|--------|-----|------|
| evidence_id | TEXT PK | CDH-EVD-XXXX |
| method_id | TEXT FK | methods.method_id |
| metric_type | TEXT | cost_reduction_pct / lead_time / inventory / quality / learning_rate |
| value | REAL | 数値 |
| unit | TEXT | % / hours / kWh / DPMO / etc |
| baseline | TEXT | 比較基準（before値・時点） |
| company_case | TEXT | 事例企業 |
| year | INT | 観測年 |
| source_url | TEXT | 出典URL |

### 3. genealogy（系譜・派生関係テーブル）

| カラム | 型 | 説明 |
|--------|-----|------|
| rel_id | TEXT PK | CDH-REL-XXXX |
| parent_method_id | TEXT FK | 元となった手法 |
| child_method_id | TEXT FK | 派生先手法 |
| rel_type | TEXT | derives / inspires / integrates / contradicts / supersedes |
| year_transition | INT | 派生年 |
| rationale | TEXT | 派生のロジック |

### 4. critiques（批判・限界テーブル）

| カラム | 型 | 説明 |
|--------|-----|------|
| critique_id | TEXT PK | CDH-CRT-XXXX |
| method_id | TEXT FK | methods.method_id |
| critic | TEXT | 批判者 |
| year | INT | 批判提起年 |
| critique_type | TEXT | labor_alienation / lock_in / over_engineering / geopolitical / quality_decay |
| description | TEXT | 批判内容 |
| source_url | TEXT | 批判の典拠 |

### 5. domains（領域マスタ）

| code | 名称 | 代表手法 |
|------|------|----------|
| MFG | 製造業 | TPS, Lean, Six Sigma |
| SW | ソフトウェア開発 | Agile, DevOps |
| ENG | エンジニアリング設計 | VE, DFMA, Modular |
| SCM | サプライチェーン | Outsourcing, Container |
| FIN | 管理会計 | ABC, ZBB, TCO |
| HW | 半導体・ハード | Moore's Law, Modular |
| ENERGY | エネルギー | Learning curves, FIT |
| CONST | 建設 | Prefab, Lean Construction |
| RD | R&D | Stage-Gate, Open Innovation |
| LOG | 物流 | Container, VMI |
| AUTO | 自動化 | CNC, RPA, AI |

---

## 暫定レコード見込み

- methods: 約280項目（15領域 × 平均19項目）
- evidence: 約400件（手法あたり1.4件）
- genealogy: 約200件
- critiques: 約150件

---

## 公開先（予定）

- SQLite DB: `~/projects/research/cost-down-history-db/cost-down-history.sqlite`
- HTML ダッシュボード: textbook.htmlスタイル（赤白CI、サイドバー目次、ダークモード対応）
- 公開URL: `https://yuyanishimura0312.github.io/cost-down-history-db/`
- Research Dashboard 登録: `save-research.sh --content-file` 経由

15領域全完了後にこの草案を確定版へアップデートする。
