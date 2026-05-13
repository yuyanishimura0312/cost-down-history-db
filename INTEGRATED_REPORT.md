# 技術・開発のコストダウン歴史的手法 統合レポート v1.0

**作成日**: 2026-05-13
**実施方法**: 15領域並列リサーチ（researcher エージェント15体・バックグラウンド同時実行）
**収集レコード数**: 構造化手法 約280項目 / source_url 約280本 / 検証可能な数値実証多数
**DB予定名**: Cost-Down History DB (CDH-DB)

---

## エグゼクティブサマリー

技術・開発のコストダウンの230年史（1788年Watt遠心調速機から2026年生成AI自動化まで）を15領域に分割し、各領域20-30項目を一次資料 URL 付きで収集した。これらを横断的に分析すると、コストダウンの実体は**6つのメカニズム**の累積的・複合的作用として整理できる。

1. **労働の分解と再構成**（Taylor科学的管理法 → Ford組立ライン → トヨタTPS → セル生産 → RPA）
2. **学習効果と規模効果**（Wright 1936 → BCG経験曲線 1968 → Moore 1965 → Swanson/Carlson曲線）
3. **品質の事前組込み**（Shewhart SQC → Deming/Juran → 田口メソッド → Six Sigma）
4. **設計時のコスト織込み**（VE/Miles 1947 → 原価企画/トヨタ 1960s → DFMA → Target Costing）
5. **境界の解体と再結合**（IBM System/360 1964 → モジュラー化 → アウトソーシング → コンテナ化 → クラウド/SaaS）
6. **情報の自動化と知能化**（PLC 1968 → CAD/CAM → BIM → AI検査 → 生成AI支援開発）

これら6軸は独立ではなく相互参照する。たとえばトヨタTPSは軸1（労働分解）と軸3（品質組込み）と軸4（設計コスト織込み）の交差点にあり、AWS Lambdaは軸5（境界解体）と軸2（規模効果）の融合である。

---

## 15領域サマリ

### 領域1: 科学的管理法・フォーディズム（1900-1950）
- **代表手法**: Taylor科学的管理法(1911) / Ford組立ライン(1913) / Wright学習曲線(1936) / Whitney互換性部品(1798)
- **代表数値**: Model T 825ドル→290ドル(65%減)、組立時間12h→1.5h(92.5%減)、Whitney契約10,000銃→部品互換化
- **メカニズム**: 動作研究・時間研究・標準化・大量生産・経験曲線
- **批判**: Braverman『労働と独占資本』(1974) — 脱スキル化と労働疎外

### 領域2: TPS・リーン・JIT（1950-1990）
- **代表手法**: トヨタ生産方式 / Just-In-Time / カンバン / 自働化(Jidoka) / SMED / TPM / セル生産 / Lean Manufacturing
- **代表数値**: NUMMI比較で生産性2倍/在庫1/7/不良率1/3、SMED 4時間→1.5時間(さらに3分まで)、DENSO TPM 5年で故障90%削減、セル生産で消費電力1/8
- **メカニズム**: 流れの最適化 + 異常の即座可視化 + 全員参加カイゼン
- **批判**: 「Lean神話」西洋企業の形骸化、文化なき導入の失敗

### 領域3: TQM・カイゼン・シックスシグマ（1950-2000）
- **代表手法**: Shewhart SQC(1924) / Deming 14原則 / Juran Quality Trilogy / Ishikawa特性要因図 / 田口ロバスト設計 / QFD / FMEA / Six Sigma(Motorola 1986)
- **代表数値**: Motorola Six Sigma 160億ドル節減、GE 1995-2005 120億ドル、QC Circle 日本1978年1000万人参加
- **メカニズム**: 統計的工程管理 + 予防費投下による総品質コスト最小化 + 全員参加
- **批判**: 3MのSix Sigmaがイノベーション阻害（特許申請低下）、Black Beltエリート化の官僚主義

### 領域4: 価値工学・原価企画
- **代表手法**: VE/VA(Miles 1947) / FAST(Bytheway 1964) / Target Costing(トヨタ 1960s) / DTC / LCC / Should Cost / Teardown / VRP
- **代表数値**: トヨタCCC21(2000) 173部品30%減・2000-2004年で累計1兆円超削減、Should Cost で IBM年間数千万ドル削減
- **メカニズム**: 機能=価値/コストの数式化 + 販売価格逆算の原価目標 + 設計段階での原価織込み
- **派生**: SAVE International、日本VE協会、Boeing/Lockheed DTC

### 領域5: 管理会計・原価計算
- **代表手法**: 標準原価計算(Webner 1920s) / 直接原価計算 / ABC(Kaplan&Cooper 1987) / ABM / BSC(1992) / TOC(Goldratt 1984) / ZBB(Pyhrr 1970) / Kaizen Costing / TCO(Gartner 1987) / LCC / EVA(Stern Stewart 1983)
- **代表数値**: ZBBで SG&A 10-25%削減、Texas Instruments年数十億ドル削減、Cisco CPFRで在庫45%削減
- **メカニズム**: 原価の正確な配賦 + ボトルネック特定 + ライフサイクル全体での意思決定
- **批判**: ABC導入の中途放棄率30-40%、ZBBの研究開発過小評価

### 領域6: アウトソーシング・SCM
- **代表事例**: Kodak-IBM(1989) / Infosys/TCS/Wipro 印度IT / Foxconn EMS / TSMC ファウンドリ(1987) / Walmart直源調達 / マキラドーラ
- **代表数値**: IT外部委託 25-35%減、印度オフショア 40-60%減、Foxconn製造 Apple利幅42%、TSMC設計企業の初期投資90%減
- **理論的支柱**: Prahalad&Hamel コアコンピタンス論(1990)、Coase 1937/Williamson 1975 取引費用経済学
- **批判**: 雇用流出（米IT職50万人減）、Foxconn過労死、TSMC台湾依存92%の地政学リスク、2020s以降リショアリング/フレンドショアリングへ転換

### 領域7: ムーア則・学習曲線
- **代表法則**: Wright's Law(1936) / Experience Curve(Henderson/BCG 1968) / Moore's Law(1965/1975) / Dennard Scaling(1974) / Koomey's Law(2010) / Swanson's Law(2012) / Carlson Curve(2003) / Kryder's Law(2005) / Nielsen's Law(1998)
- **代表数値**: Wright倍加で20%減、Moore 18-24mo倍加、Swanson PV 1977 $76.67/W→2024 $0.11/W(700倍減)、Li-ion 1991 $9200→2024 $78/kWh(99%減)、Carlson curve(DNA配列)はMoore超
- **理論的進化**: Lafond/Farmer 2018 — 51製品で学習曲線と定率進捗が同精度
- **限界**: Dennard scaling終焉(2005)、Kryder減速、CCSの逆学習(40年で改善ゼロ)、原子力の負学習曲線

### 領域8: モジュラー設計・プラットフォーム
- **代表手法**: IBM System/360(1964) / Henderson&Clark建築的イノベーション(1990) / Baldwin&Clark Design Rules(2000) / Meyer&Lehnerd プロダクトプラットフォーム(1997) / Boothroyd-Dewhurst DFMA(1980-91) / Pine マスカスタマイゼーション(1993) / VW MQB(2012) / Toyota TNGA(2015) / Renault-Nissan CMF
- **代表数値**: VW MQB 単価/開発費20%減・エンジニアリング30%減、TNGA製造コスト20%減、トヨタCCC21で1兆円減、DFMA で組立30%・部品29%・原価26%減
- **理論的深化**: 藤本隆宏 インテグラル型 vs モジュラー型 — トレードオフ関係（性能↔汎用性）

### 領域9: ソフトウェア開発手法
- **代表手法**: 構造化プログラミング(Dijkstra 1968) / Waterfall(Royce 1970) / COCOMO(Boehm 1981) / XP(Beck 1999) / Agile Manifesto(2001) / Lean SD(Poppendieck 2003) / CI(Fowler 2006) / DevOps(2009) / SRE(Google) / Microservices+Docker(2013) / IaC / Low-Code / Copilot(2021)
- **代表数値**: Standish 2020 Agile成功率42% vs Waterfall 13%、DORA Elite性能でデプロイ頻度26倍/リードタイム200倍、Copilotタスク55.8%高速化、Low-Code 363% 3年ROI
- **批判**: AIコーディングによるコード複製率増加(2025 GitClear)、大規模Agile(1000人超)の限界、技術債蓄積

### 領域10: OSS・クラウド
- **代表事例**: GNU(Stallman 1983) / GPL / Linux(1991) / LAMP / Salesforce SaaS(1999) / AWS EC2(2006) / Docker(2013) / Kubernetes(2014) / Lambda(2014) / Twilio(2008) / Stripe(2010) / IBM PC x86(1981) / ARM
- **代表数値**: クラウド市場 $0.5B(2006)→$330B(2024) CAGR 28%、Stripe支払総額$1B達成(2021)、Heroku デプロイ時間90%減
- **メカニズム**: CapEx → OpEx転換、複製限界費用ほぼゼロ、API化による標準化
- **批判**: ベンダーロックイン、Log4j等オープンソース脆弱性、AWS等の寡占化

### 領域11: エネルギー学習曲線
- **代表技術**: PV(Swanson 20-24%) / 陸上風力(15-23%) / Li-ion(18-20%) / LED(Haitz 10x/10yr) / 水素PEM電解槽(32.1%) / 原子力(負学習)
- **代表数値**: PV 700倍減・LCOE $0.043/kWh(2024)で化石燃料より41%安、Li-ion 99%減、IRENA 2024 新設PVの91%が化石燃料より経済的
- **政策誘導**: DOE SunShot 2020目標を2017年達成、FIT/ITC効果、Hinkley Point C 16億→34億ポンド(倍増)
- **失敗例**: CCS 40年で学習率ゼロ — 標準化困難・展開数不足・規制不確実

### 領域12: 建設プレハブ・モジュラー
- **代表事例**: Sears Modern Homes(1908-42、70,000棟) / Levittown(1947、$8000→$4000) / 積水/大和ハウス ユニット工法 / Lean Construction Institute(1997) / IPD / BIM / Broad Group Mini Sky City(204m12日) / Modular Building Institute / 3Dプリント建築
- **代表数値**: PC工法 工期1/3短縮・人件費20-30%減、Levittown 50%減、Lean Construction コスト15-30%減・工期30%減、Broad Group工期1/50
- **構造的停滞**: McKinsey 2024 — 建設業生産性 2000-2024年で年率0.4%増、製造業3%・全産業2%との大差。$40兆生産性ギャップ。労働力構造崩壊+一品生産+DX投資障壁+契約制度

### 領域13: R&D効率化
- **代表手法**: Fisher 実験計画法(1935) / Stage-Gate(Cooper 1988) / Concurrent Engineering(DARPA 1988) / 田口ロバスト設計 / DFMA / Set-Based CE(トヨタ) / Open Innovation(Chesbrough 2003) / InnoCentive(2001) / Lean Startup(Ries 2011) / AI創薬(2018-)
- **代表数値**: Stage-Gate企業採用率54%、Boeing 777で開発期間40%短縮、AI創薬で開発期間62.5%短縮・成功率予測 7.9%→90%、Lean Startup燃焼期間12-18→6-9ヶ月、InnoCentive成功率35-50%
- **対 Eroom's Law**: 製薬R&D生産性悪化への対抗。Stage-Gate×AI×Open Innovation三点統合が次世代潮流

### 領域14: 物流・コンテナ化
- **代表事例**: McLean Ideal-X(1956) / ISO 668(1968-70) / FedEx ハブ&スポーク(1971) / Walmart-P&G VMI(1980s) / クロスドック / バーコードUPC(1974)/RFID / CPFR(1990s) / DRP / ECR / ラストワンマイル+ギグ配送
- **代表数値**: コンテナ化で積込費$5.83→$0.16/トン(36倍効率)・荷役コスト40分の1減、Walmart VMI で在庫30%減・棚上げ率98%、Cisco CPFR在庫45%減、クロスドックで保管費40-60%減、ラストマイルが総物流費の53%(2025)
- **構造**: 手作業→標準化→情報共有→AI最適化の四段階。現在はWalmart直源+クロスドック+60%自動化DC+AI需要予測の統合

### 領域15: 自動化・ロボティクス
- **代表事例**: Watt遠心調速機(1788) / Wiener Cybernetics(1948) / MIT NC(1952) / Unimate産業ロボット(1961、GM) / Modicon PLC(1968) / CATIA(1977) / CIM / FMS / GM Saturn過剰投資(1985 $45B/失敗) / RPA(2010s) / Amazon Kiva(2012) / Universal Robots Cobot(2008) / AI検査 / 生成AI(2022-) / 自動運転トラック
- **代表数値**: Modicon PLC プログラム変更 6ヶ月→6日(97%減)、CIM 生産性40-70%向上/設計コスト15-30%減、Kiva ピッキング3-4倍/コスト20%減、Cobot 導入コスト70%減、生成AI実装ROI達成企業6%のみ(2024)、自動運転 走行コスト42%減・年間$3000B削減ポテンシャル
- **教訓**: GM Saturn $45Bで市場シェア1%up — 技術至上主義より組織受容性

---

## 横断分析: 6メカニズムの整理

### M1. 労働の分解と再構成
**起点**: Taylor科学的管理法(1911) / 動作研究
**進化**: Ford組立ライン → トヨタTPS → セル生産 → RPA → 生成AI白カラー自動化
**現在の到達点**: 米カスタマーサービス職 80K減(2022-2024)
**残課題**: 「労働削減」と「組織受容性」のトレードオフ。GM Saturn失敗から40年経ても生成AI投資の60%が同轍を踏む

### M2. 学習効果と規模効果
**起点**: Wright 1936(航空機20%/倍加)
**進化**: BCG経験曲線 → Moore則 → Swanson/Carlson曲線 → EV電池・PV
**現在の到達点**: PV 700倍減・Li-ion 99%減
**残課題**: 物理限界(Dennard scaling終焉)、CCS等の「学習しない技術」の判別基準

### M3. 品質の事前組込み
**起点**: Shewhart SQC(1924)
**進化**: Deming/Juran → 田口メソッド → Six Sigma → DFSS → AI検査
**現在の到達点**: AI検査で品質コスト20-40%減、検出精度95-99%
**残課題**: Six Sigmaのイノベーション阻害(3M事例)、過剰品質投資

### M4. 設計時のコスト織込み
**起点**: Miles VE(1947) / Toyota Target Costing(1960s)
**進化**: FAST → DFMA → DTC → LCC → Should Cost
**現在の到達点**: トヨタCCC21で1兆円超削減、DFMAで原価26%減
**残課題**: 後期変更対応の硬直化、カスタマイズ需要への対応

### M5. 境界の解体と再結合
**起点**: IBM System/360(1964) / コンテナ化(1956)
**進化**: モジュラー化 → アウトソーシング → ファブレス → SaaS/IaaS/Serverless
**現在の到達点**: クラウド市場$330B、TSMC ファウンドリ世界92%、Stripe API経済
**残課題**: 地政学リスク集中、ベンダーロックイン、サプライチェーン脆弱性

### M6. 情報の自動化と知能化
**起点**: Watt調速機(1788) / Wiener Cybernetics(1948) / NC(1952)
**進化**: PLC → CAD/CAM → CIM → BIM → AI/生成AI
**現在の到達点**: DORA Elite企業デプロイ頻度26倍、Copilot 55.8%高速化、自動運転走行コスト42%減
**残課題**: 生成AIのROI達成6%、コード品質劣化、規制成熟度

---

## 横断的発見

### 1. 学習曲線は技術領域の境界を越える
航空機(Wright 1936)、半導体(Moore 1965)、太陽光(Swanson 2012)、DNA(Carlson 2003)、リチウムイオン電池(2010s)など、媒体が異なっても累積生産倍増あたり10-30%減という規則性。Lafond 2018研究では51製品で実証。

### 2. 「失敗例」がメカニズム理解の鍵
- GM Saturn 45B$投資失敗 → 技術導入は組織受容性に依存
- 3M Six Sigma → 効率化とイノベーションは対立しうる
- CCS 40年学習ゼロ → 学習曲線成立の必須条件（標準化・展開数・規制安定性）
- Kodak破産(2012) → コア競争力外部化のリスク
- 建設業生産性停滞 → 技術導入だけでは産業全体の生産性は上がらない

### 3. リバウンド（揺り戻し）の周期性
- 大量生産 → 多品種少量(セル生産)
- グローバル化 → リショアリング/フレンドショアリング
- モノリス → マイクロサービス → モノリス回帰(42%)
- 集中DC → 分散ラストワンマイル
- 標準化 → カスタマイゼーション → マスカスタマイゼーション

### 4. 90年史の累積効果
- 1900年: 馬車の時代、Ford Model Tの前身モデルが2000ドル超
- 2024年: スマートフォン1台で1900年の世界中の計算機を上回る性能
- 累積コスト低減: 10^7オーダー以上（複数領域で7桁減）

---

## DB スキーマ（確定版）

```sql
CREATE TABLE methods (
    method_id      TEXT PRIMARY KEY,    -- CDH-MET-XXXX
    name_ja        TEXT NOT NULL,
    name_en        TEXT NOT NULL,
    domain_code    TEXT NOT NULL,       -- MFG/SW/ENG/SCM/FIN/HW/ENERGY/CONST/RD/LOG/AUTO
    mechanism_axis TEXT,                -- M1-M6（横断メカニズム）
    era_start      INTEGER,
    era_end        INTEGER,
    originator     TEXT,
    origin_org     TEXT,
    origin_country TEXT,
    primary_source_url TEXT NOT NULL,
    mechanism      TEXT NOT NULL,        -- 地の文での説明
    status         TEXT,                 -- active/mature/declining/legacy
    verification   TEXT                  -- verified/unverified/requires_review
);

CREATE TABLE evidence (
    evidence_id    TEXT PRIMARY KEY,
    method_id      TEXT REFERENCES methods,
    metric_type    TEXT NOT NULL,        -- cost_reduction_pct, lead_time, etc
    value          REAL,
    unit           TEXT,
    baseline       TEXT,
    company_case   TEXT,
    year           INTEGER,
    source_url     TEXT NOT NULL
);

CREATE TABLE genealogy (
    rel_id              TEXT PRIMARY KEY,
    parent_method_id    TEXT REFERENCES methods,
    child_method_id     TEXT REFERENCES methods,
    rel_type            TEXT,             -- derives/inspires/integrates/contradicts/supersedes
    year_transition     INTEGER,
    rationale           TEXT
);

CREATE TABLE critiques (
    critique_id    TEXT PRIMARY KEY,
    method_id      TEXT REFERENCES methods,
    critic         TEXT,
    year           INTEGER,
    critique_type  TEXT,                  -- labor_alienation/lock_in/over_engineering/etc
    description    TEXT,
    source_url     TEXT
);

CREATE TABLE domains (
    code           TEXT PRIMARY KEY,
    name_ja        TEXT,
    name_en        TEXT
);
```

**初期投入見込み**:
- methods: 280項目
- evidence: 約400件
- genealogy: 約200件
- critiques: 約150件
- domains: 11項目

---

## 次工程

1. SQLite DB ファイル生成（Python スクリプト）
2. ダッシュボードHTML生成（textbook.htmlスタイル、赤白CI #CC1400、サイドバー目次、ダークモード対応）
3. 領域別教科書HTML作成（必要に応じて）
4. Research Dashboardへ登録（save-research.sh --content-file）
5. GitHub Pages公開（https://yuyanishimura0312.github.io/cost-down-history-db/）
6. /cost-down-history エージェント新設（必要に応じて）

---

## 出典総覧

15領域で約280本の source_url を収集。詳細は各領域別ファイル `regions/region-XX.md` に格納予定。一次資料優先、Wikipedia は補助的。ハルシネーション排除を品質基準とし、未検証項目には `requires_review` フラグを付ける運用。
