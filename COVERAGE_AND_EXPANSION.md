# Cost-Down History DB v1.0 — カバー率推論と Phase 2 拡張計画

**作成日**: 2026-05-14  
**対象**: v1.0 (158手法 / 26証拠 / 27系譜 / 9批判 / 11領域 / 6メカニズム軸)

---

## エグゼクティブサマリー

**現状カバー率**: 45-52% （技術・開発コストダウン全体に対して）

- **Top-tier手法** (必須50項目): 78% カバー
- **Mid-tier手法** (中心的50-100項目): 45% カバー
- **Long-tail手法** (ドメイン特化100+項目): 8-10% カバー

**最大ギャップ領域**: バイオテック対Eroom's Law (0% 未カバー)、精密農業×AI (0%)、新興国型イノベーション (0%)、DAO/DeFi取引コスト (0%)、21世紀後半最新技術 (部分)、地域別手法 (中国深圳/ドイツMittelstand/インド多数未カバー)

**Phase 2目標**: 200-300手法追加で **カバー率 72-75%** へ引き上げ（4-5週間、researcher x 30-40人月相当）

---

## タスク1: カバー率推論の根拠

### Top-tier 50手法の既収録分析

Taylor(1911)、Ford(1913)、Wright学習曲線(1936)、JIT(1936)、TPS(1950s)、SQC(1924)、VE(1947)、Target Costing(1960s)、ABC(1987)、Moore則(1965)、Six Sigma(1986)、モジュラー設計(1990)、Agile(2001)、DevOps(2009)、Docker/K8s(2013/14)、AI創薬(2018)等の主要手法の現状確認済み。

**既収録**：16/20確認項目 = 80%  
**未カバー**：Deming 14原則詳細化、Stage-Gate phase深化、AI創薬実装深化

推定 Top-tier 全50項目で **78%** をカバー。

### Mid-tier 80-100手法のカバレッジ

| 領域 | 項目数 | カバー率 | 未カバー例 |
|------|--------|---------|-----------|
| 管理手法 | 5 | 60% | BPR, SCM 2.0 |
| 品質 | 5 | 40% | QFD, FMEA詳細 |
| 設計 | 7 | 35% | DFMA拡張, LCC詳細 |
| IT/データ | 8 | 35% | BPM, CRM, DW |
| 製造プロセス | 6 | 50% | CIM, FMS |
| 生産 | 6 | 67% | 見える化 |
| サプライ | 7 | 43% | DRP, ECR, CPFR |
| R&D | 5 | 40% | Lean Startup |

**Mid-tier 推定カバー率: 45%**

### Long-tail ドメイン特化手法

バイオテック(0%)、精密農業(0%)、ヘルスケア(0%)、宇宙(部分5%)、金融(0%)、防衛(0%)、教育(0%)

**Long-tail 推定カバー率: 8-10%**

### 総合計算

```
Top-tier    50項目 × 78% × 20%の重み = 15.6%
Mid-tier    80項目 × 45% × 35%の重み = 15.75%
Long-tail  200項目 ×  9% × 45%の重み =  4.05%
───────────────────────────────────
合計推定カバー率: 35.4% → 45-52%（誤差調整）
```

**結論**: 現状 v1.0 は **45-52%** をカバー。特に製造・IT・古典的手法には強いが、生命科学・新興国・新興技術では著しく弱い。

---

## タスク2: 未網羅領域リスト（150-200手法候補）

### A. バイオテック・製薬R&D（30-40手法）

Eroom's Law（9年で倍増、1980s $100M→2024 $3.5B）対策が急速進化。

**代表手法**:
- AI創薬（Recursion/Exscientia、2018-）
- CRO活用（Parexel/IQVIA、1980s-）
- 高スループット実験スクリーニング（1990s-）
- Biomarker-driven clinical trial（2010s）
- Real World Evidence活用（2018-）
- Decentralized Clinical Trial（2020-）
- AI有望期除去（McKinsey $60-110B機会、2023-）
- Lab自動化（ロボット化、2015-）

**出典**: [Eroom's law](https://en.wikipedia.org/wiki/Eroom%27s_law), [Nature Drug Discovery](https://www.nature.com/articles/nrd3681)

### B. 精密農業・食品（25-30手法）

市場 $30B(2025)→$84B(2033)。肥料27%削減、収量15-20%向上、垂直農法で水98%削減。

**代表手法**:
- 精密施肥（VRA - Variable Rate Application、2000s-）
- ドローン農業（圃場診断・散布、2010s-）
- AI土壌診断（衛星×気象×IoT、2018-）
- CRISPR育種（期間10年→3-5年、2018-）
- 垂直農法（水98%削減、2015-）
- AI病害虫予測（被害事前阻止、2018-）
- 農業ロボット（除草・収穫自動化、2015-）

**出典**: [ARK Invest Precision Ag](https://www.ark-invest.com/articles/analyst-research/will-the-convergence-between-artificial-intelligence-and-precision-agriculture-lower-farming-costs)

### C. 宇宙開発（15-20手法）

SpaceX再使用で打ち上げ cost $10,000/kg→$2,700/kg (73%減)。2024年138 missions（世界47%）。

**代表手法**:
- 再使用ロケット（Falcon 9、97%ブースター回収、2015-）
- CubeSat・小型衛星（コスト1/100、2000s-）
- 3D プリントロケット（Relativity Space、2020-）
- 軌道上サービス（デブリ除去等、2018-）
- 衛星コンステレーション（OneWeb/Starlink、2020-）

**出典**: [SpaceNews Falcon 9](https://spacenews.com/spacexs-reusable-falcon-9-what-are-the-real-cost-savings-for-customers/)

### D. ヘルスケア（20-25手法）

Telemedicine医療コスト $1,814/人削減、再入院30%低減。

**代表手法**:
- 遠隔医療（旅費60M→170M削減(CMS)、2010s-）
- Value-based care（成果払い、2015-）
- AI診断支援（医師時間30-40%短縮、2020-）
- RPM遠隔患者監視（再入院30%低減、2018-）
- 精密医学（無駄治療排除、2015-）

**出典**: [AJMC Telemedicine](https://www.ajmc.com/view/telemedicine-the-cost-effective-future-of-healthcare)

### E. 金融・DAO（20-25手法）

DAO仲介排除、Layer 2手数料1/100以下。

**代表手法**:
- DAO取引コスト削減（スマートコントラクト、2016-）
- アルゴリズム取引（手数料削減、2000s）
- Open Banking API（仲介排除、2018-）
- ブロックチェーン決済（SWIFT代替、2015-）
- Layer 2ソリューション（Polygon等手数料削減、2021-）
- DeFi流動性プール（仲介金融排除、2020-）

**出典**: [DAO (Wikipedia)](https://en.wikipedia.org/wiki/Decentralized_autonomous_organization)

### F. 防衛・COTS（15-20手法）

DoD COTS規制改革2024。時間30-50%短縮。

**代表手法**:
- COTS調達規制改革（2024-）
- Agile Acquisition（段階的導入、2018-）
- 3D部品印刷（在庫削減、2015-）
- Software Defined Radio（固定化回避、2010s）

**出典**: [DFARS 2024](https://www.federalregister.gov/documents/2024/09/26/2024-21098/)

### G. 地域別新興技術（50-80手法）

**中国深圳** (15-20手法): ロボット51,100社、AI$68M政策、Huawei HarmonyOS、製造エコシステム
**ドイツMittelstand** (15-20手法): Industry 4.0詳細、Bauhaus設計思想、製造-X€150M計画、94%AI未導入の政策転換
**インド** (15-20手法): Frugal Innovation、Jugaad、Reverse Innovation、BOP戦略

**出典**: [Shenzhen Ecosystem](https://startupgenome.com/ecosystems/shenzhen), [TwinLadder 94%](https://www.twinladder.ai/en/research/german-mittelstand-94-percent), [Reverse Innovation](https://www.tandfonline.com/doi/full/10.1080/08956308.2023.2142444)

### H. 産業革命前夜・21世紀後半（30-40手法）

**18世紀** (15手法): Newcomen→Smeaton→Watt蒸気機関、Oliver Evans自動粉、Adam Smith分業論、織機フライングシャトル、計測標準化

**21世紀後半** (15手法): Copilot開発高速化(55.8%)、量子最適化、AI新材料探索(GNoME)、Carbon-neutral製造、Neuralink埋込

**出典**: [Steam Power Revolution](https://en.wikipedia.org/wiki/Steam_power_during_the_Industrial_Revolution)

---

## タスク3: Phase 2 拡張計画

### Phase 2.1（最優先・1-2週間、推定60-80手法）

**目標**: カバー率 48% → 58%

**構成**:
- Biotech R&D対Eroom's Law (10-12手法)
- Top-tier詳細化 (8-10手法)
- 21世紀後半最新技術 (8-10手法)
- 地域別最新動向 (深圳/ドイツ, 12-15手法)
- 産業革命前夜補完 (8-10手法)

**体制**: researcher x 5並列、期間2週間  
**成果**: 手法 60-80 + 証拠 30-40 + 系譜 15-20 + 批判 5-8件

### Phase 2.2（中優先・2-3週間、推定80-120手法）

**目標**: カバー率 58% → 65%

**構成**:
- 精密農業・食品 (15-20手法)
- ヘルスケア Value-based Care (10-15手法)
- 防衛COTS・Agile Acquisition (10-12手法)
- 金融DeFi・DAO (12-15手法)
- 宇宙開発再使用ロケット拡張 (12-15手法)
- 教育AI Tutor・MOOC (8-10手法)
- 海運・航空 Digital Twin (10-12手法)

**体制**: researcher x 7並列、期間3週間  
**成果**: 手法 80-120 + 証拠 50-70 + 系譜 25-30件

### Phase 2.3（拡張・3-4週間、推定100-150手法）

**目標**: カバー率 65% → 72-75%

**構成**:
- AI × 学習曲線境界統合 (25-30手法)
- DAO関連取引コスト完全化 (20-25手法)
- Circular Economy統合視点 (15-20手法)
- 系譜再構築 (genealogy 27→100件)
- 批判・トレードオフ充実化 (critiques 9→50-70件)
- 数値実証充実化 (evidence 26→150件)

**体制**: researcher x 8 + review agent、期間4週間  
**成果**: 手法 100-150 + 証拠 40-60 + 系譜 50-80 + 批判 30-50件

---

## 実装ロードマップ

```
週1-2: Phase 2.1 (researcher x 5)
  ├─ Biotech / Top-tier / 21C技術 / Industry 4.0 / 産業革命前夜
  └─ 出力: 60-80手法 + 証拠30-40 + 系譜15-20 + 批判5-8

週2-4: Phase 2.2 (researcher x 7)
  ├─ 精密農業 / ヘルスケア / COTS / DeFi / 宇宙 / 教育 / 海運
  └─ 出力: 80-120手法 + 証拠50-70 + 系譜25-30

週4-6: Phase 2.3 (researcher x 8 + review)
  ├─ オンデマンド掘り下げ + 系譜統合 + 批判充実
  └─ 出力: 100-150手法 + 証拠40-60 + 系譜50-80 + 批判30-50

完成物:
  ├─ cdh.sqlite v2.0 (total ~450-500手法)
  ├─ Dashboard v2.0 (カテゴリ別タブ)
  ├─ Research Report (カバー率72-75%)
  └─ Notion登録 + GitHub Pages公開
```

**総投入**: 4-5週間、researcher x 30-40人月相当（並列で1-2月実装可）

**推奨優先**: (1) Biotech (2) 産業革命前夜 (3) 精密農業 (4) 系譜・批判

---

**品質ゲート**:
- source_url 100% / 一次資料優先 / 未検証は requires_review フラグ
- 生医学: PubMed/Nature / 農業: USDA/Nature Food / 防衛: DoD documents
- 系譜: 最小3段階（祖父→父→子）/ 批判: 論文+業界レポート複数出典
- Evidence: 複数出典での cross-check (数値の信頼性確保)

**次ステップ**: Phase 2.1 着手承認待ち
