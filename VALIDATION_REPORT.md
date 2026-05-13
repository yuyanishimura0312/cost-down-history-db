# Cost-Down History DB (CDH-DB) v1.0 — 検証レポート

_検証実施日時: 2026-05-14 08:15:23_  
_対象DB: `/Users/nishimura+/projects/research/cost-down-history-db/cdh.sqlite`_  
_検証スクリプト: `scripts/validate_db.py`_  

## 0. はじめに

本レポートは Cost-Down History DB v1.0 に対して、スキーマ整合性・数値妥当性・系譜構造・メカニズム軸分布・出典 URL 生存性・ハルシネーション疑いの 6 観点で実施した自動検証の結果である。検証は標準ライブラリのみで構成された `validate_db.py` により再現可能であり、URL 生存確認は `concurrent.futures.ThreadPoolExecutor` を用いて 24 並列で実行した。判定は PASS（合格）・WARN（要確認）・FAIL（要修正）の 3 段階で示し、数値の根拠はすべて SQLite クエリの結果として提示する。推測によるラベル付けは行わない。

## 1. サマリー

検証は合計 25 項目について行われ、その分布は以下の通りである。 FAIL がゼロまたは少数であれば DB の構造的健全性は確保されており、 WARN 群は今後のメンテナンスで優先的に確認すべき箇所として位置づけられる。

| 区分 | 件数 |
|---|---|
| PASS | 20 |
| WARN | 5 |
| FAIL | 0 |

テーブル別レコード数は以下の通りである。スキーマ定義どおりに methods 213 件 / evidence 51 件 / genealogy 46 件 / critiques 16 件 / domains 11 件が格納されている。

| テーブル | 行数 |
|---|---|
| methods | 213 |
| evidence | 51 |
| genealogy | 46 |
| critiques | 16 |
| domains | 11 |

## 2. スキーマ整合性

method_id の一意性、外部キー参照（evidence・genealogy・critiques から methods への参照、methods から domains への参照）、必須フィールド（name_ja / primary_source_url / mechanism）の NULL チェックを実施した。PRIMARY KEY 制約によって ID 重複は構造的に防がれている一方、NOT NULL 制約が宣言されていない primary_source_url・mechanism は WARN 扱いとして個別レコード単位で確認している。

| 区分 | 内容 |
|---|---|
| PASS | methods.method_id is unique (PK constraint holds) |
| PASS | methods.method_id has no NULL/empty values |
| PASS | evidence.method_id → methods FK valid |
| PASS | genealogy.parent_method_id → methods FK valid |
| PASS | genealogy.child_method_id → methods FK valid |
| PASS | critiques.method_id → methods FK valid |
| PASS | methods.name_ja: no NULL/empty |
| PASS | methods.primary_source_url: no NULL/empty |
| PASS | methods.mechanism: no NULL/empty |
| PASS | methods.domain_code → domains FK valid |

## 3. 数値妥当性

era_start が 1700–2030 の西暦範囲に収まること、era_start < era_end（era_end == 9999 は 「現在まで継続」を表す sentinel として許容）、evidence.value に負値や非現実的な桁外れ （|x| > 1e7）が含まれないこと、% 単位で 100 を超える値の確認、evidence.year の範囲を検証した。

| 区分 | 内容 |
|---|---|
| PASS | era_start values within [1700, 2030] |
| PASS | era_start < era_end (or era_end == 9999) |
| PASS | era_end either ≤ 2030 or == 9999 sentinel |
| PASS | evidence.value has no negatives |
| WARN | evidence.value magnitude > 1e7: [('CDH-EVD-0029', 16000000000.0, 'USD', 'cost_savings_usd'), ('CDH-EVD-0030', 12000000000.0, 'USD', 'cost_savings_usd'), ('CDH-EVD-0040', 10000000000.0, 'USD', 'cost_savings_usd'), ('CDH-EVD-0292', 214000000.0, 'proteins', 'structure_db_growth'), ('CDH-EVD-0294', 40000000.0, 'USD/yr', 'cost_savings_usd_annual')] |
| WARN | % unit but value > 100 (review whether intended): [('CDH-EVD-0300', 'productivity_increase_pct', 126.0, '%')] |
| PASS | evidence.year within [1700, 2030] |

## 4. 系譜構造（genealogy）

自己ループ（parent == child）と有向グラフ上の循環参照（A→B→A）を深さ優先探索で検出した。また year_transition（派生年）が parent の era_start 以降、かつ child の era_start を概ね超えない（±5 年の許容）ことを確認している。理論の派生は常に発祥より後に起こるはずであり、この時系列の単調性は系譜データの最低限の整合条件である。

| 区分 | 内容 |
|---|---|
| PASS | no self-loops in genealogy |
| PASS | no cycles detected in genealogy DAG |
| WARN | year_transition era misalignment (5): [('CDH-REL-0083', 'year_transition before parent.era_start', 2013, 2018), ('CDH-REL-0087', 'year_transition before parent.era_start', 2008, 2011), ('CDH-REL-0096', 'year_transition before parent.era_start', 1769, 1770), ('CDH-REL-0097', 'year_transition before parent.era_start', 1775, 1788), ('CDH-REL-0098', 'year_transition before parent.era_start', 1771, 1776)] |

## 5. メカニズム軸の分布

本 DB は 6 つのメカニズム軸（M1: 標準化と分業 / M2: 自動化と機械化 / M3: 規模・経験曲線 / M4: 情報・最適化 / M5: 外部化・市場化 / M6: 制度・会計）を備える。各軸の手法数を以下に示し、軸が未割当のレコードや想定外の軸ラベルの混入を検出した。

| 軸 | 手法数 |
|---|---|
| M1 | 33 |
| M2 | 23 |
| M3 | 30 |
| M4 | 26 |
| M5 | 63 |
| M6 | 38 |

| 区分 | 内容 |
|---|---|
| PASS | every method has a mechanism_axis assigned |
| PASS | all axes ∈ {M1, M2, M3, M4, M5, M6} |

## 6. 出典 URL 生存確認

methods.primary_source_url / evidence.source_url / critiques.source_url を重複排除した URL 集合に対して、Mozilla 互換 User-Agent で HTTP HEAD を発行し、HEAD が拒否される場合は GET で再試行している。200 / 301 / 302 などの 2xx・3xx を success、404 / 5xx ほかの 4xx・5xx および接続エラーを failure と判定する。瞬間的なネットワーク状態に左右されるため、failure 群は手動再確認の対象として記載する。

| 区分 | 内容 |
|---|---|
| WARN | URL liveness: 205/242 OK (37 failure, 20.4s @ 24 parallel) |

### 6.1. 失敗 URL 一覧

| URL | ステータス | エラー |
|---|---|---|
| https://www.nature.com/articles/nature.2015.18190 | 303 | HTTPError 303 |
| https://academic.oup.com/nar/article/52/D1/D368/7337620 | 403 | HTTPError 403 |
| https://direct.mit.edu/books/monograph/1856/Design-Rules-Volume-1The-Power-of-Modularity | 403 | HTTPError 403 |
| https://tech.slashdot.org/story/19/01/05/0248207/what-happened-when-automation-came-to-general-motors | 403 | HTTPError 403 |
| https://www.adb.org/sites/default/files/publication/964626/adb-brief-299-india-unified-payments-interface.pdf | 403 | HTTPError 403 |
| https://www.bcg.com/ja-jp/increase-resilience-global-supply-chain | 403 | HTTPError 403 |
| https://www.bcg.com/publications/1968/business-unit-strategy-growth-experience-curve | 403 | HTTPError 403 |
| https://www.ecr-community.org/ | 403 | HTTPError 403 |
| https://www.emerald.com/insight/content/doi/10.1108/jmtm-08-2018-0270/full/html | 403 | HTTPError 403 |
| https://www.iea.org/ | 403 | HTTPError 403 |
| https://www.innocentive.com/ | 403 | HTTPError 403 |
| https://www.netsuite.com/portal/resource/articles/erp/distribution-requirement-planning-drp.shtml | 403 | HTTPError 403 |
| https://www.projectmanagement.com/blog-post/412/does-six-sigma-kill-creativity- | 403 | HTTPError 403 |
| https://www.value-eng.org/ | 403 | HTTPError 403 |
| https://www.value-eng.org/page/ValueStandards | 403 | HTTPError 403 |
| https://deming.org/explore/pdsa-cycle/ | 404 | HTTPError 404 |
| https://en.wikipedia.org/wiki/I-SPY_trial | 404 | HTTPError 404 |
| https://evboosters.com/ev-charging-news/the-blueprint-of-an-empire-how-byd-built-global-dominance-through-vertical-integration/ | 404 | HTTPError 404 |
| https://q-ctrl.com/blog/q-ctrl-transforms-quantum-advantage-outlook-breaking-previous-records-for-optimization-problems-and-outperforming-competitive-technologies-for-optimization-problems-and-outperforming-competitive-technologies/ | 404 | HTTPError 404 |
| https://sciencedirect.com/article/pii/S1098301520322026 | 404 | HTTPError 404 |
| https://sortly.com/blog/rfid-vs-barcode-for-inventory-tracking | 404 | HTTPError 404 |
| https://www.2-data.com/knowledge-hub/a-history-of-salesforce | 404 | HTTPError 404 |
| https://www.fda.gov/media/120060/download | 404 | HTTPError 404 |
| https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry | 404 | HTTPError 404 |
| https://www.ice.org.uk/news-views-insights/inside-infrastructure/smeaton-vs-watt-the-steam-engine-rivalry | 404 | HTTPError 404 |
| https://www.schrodinger.com/life-science/learn/white-papers/reversing-erooms-law-can-computers-dramtically-impact-productivity-drug-discovery/ | 404 | HTTPError 404 |
| https://www.srgresearch.com/articles/cloud-market-jumped-to-330-billion-in-2024 | 404 | HTTPError 404 |
| https://innovationlabasia.dk/en/shenzhen-the-spot-for-rapid-prototyping/ | 451 | HTTPError 451 |
| https://www.federalregister.gov/documents/2024/09/18/2024-21078/conducting-clinical-trials-with-decentralized-elements | 500 | HTTPError 500 |
| https://www.orcalean.com/article/genchi-genbutsu-toyota's-approach-to-quality-and-root-cause-analysis | 500 | HTTPError 500 |
| https://maaw.info/ArticleSummaries/ArtSumKaplanAnderson2007.htm | 502 | HTTPError 502 |
| https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/ | - | timeout |
| https://corporate.ford.com/articles/history/the-model-t/ | - | timeout |
| https://indianote.asia/india-it-big3 | - | URLError: [Errno 8] nodename nor servname provided, or not known |
| https://strateos.com/ | - | URLError: timed out |
| https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-2024 | - | timeout |
| https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-return-of-zero-base-budgeting | - | timeout |

## 7. ハルシネーション疑い

1 人の originator が異なる era_start で複数登場し、その範囲が 30 年を超えるケースは、発祥年の取り違えあるいは人名同定エラーの兆候として WARN 扱いとする。また method 名の正規化文字列に対する SequenceMatcher 比率 0.90 以上のペアを近似重複として抽出した。いずれも自動判定にとどめ、人手による発祥年・名称の最終確認を前提とする。

| 区分 | 内容 |
|---|---|
| WARN | originators with era_start span > 30 years across multiple methods (2): [('トヨタ自動車', [1960, 1990, 2000, 2015], 'CDH-MET-0043,CDH-MET-0044,CDH-MET-0045,CDH-MET-0117,CDH-MET-0120,CDH-MET-0243'), ('豊田佐吉/大野耐一', [1890, 1950], 'CDH-MET-0013,CDH-MET-0316')] |
| PASS | no near-duplicate method names (threshold 0.9) |

### 7.1. era_start が広く分散した originator

| originator | era_start 群 | 関連 method_id |
|---|---|---|
| トヨタ自動車 | [1960, 1990, 2000, 2015] | CDH-MET-0043,CDH-MET-0044,CDH-MET-0045,CDH-MET-0117,CDH-MET-0120,CDH-MET-0243 |
| 豊田佐吉/大野耐一 | [1890, 1950] | CDH-MET-0013,CDH-MET-0316 |

## 8. 修正提案

1. URL 失敗群は Wayback Machine（https://web.archive.org/）の保存版に差し替えるか、一次資料（書籍・学術論文 DOI）への置換を検討する。
2. 同一 originator の era_start 大幅乖離は、同名異人の混同または初出文献の取り違えの可能性があるため、原典への突き合わせを行う。

## 9. 再現方法

本検証は以下の単一コマンドで完全に再現可能である。標準ライブラリのみを使用しているため、追加の pip インストールは不要である。

```bash
python3 scripts/validate_db.py
```

---

_本レポートは `scripts/validate_db.py` により自動生成された。設定値は同スクリプト冒頭の定数で調整可能である。_
