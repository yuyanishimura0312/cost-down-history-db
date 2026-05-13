#!/usr/bin/env python3
"""Phase 2.1 ingest: 55 new methods from 5 parallel research teams (A/B/C/D/E)."""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "cdh.sqlite"
conn = sqlite3.connect(DB)
c = conn.cursor()

# Get max method_id number
row = c.execute("SELECT method_id FROM methods ORDER BY method_id DESC LIMIT 1").fetchone()
last_n = int(row[0].split("-")[-1])
print(f"Last method_id: {row[0]} (next: CDH-MET-{last_n+1:04d})")

# === A. Biotech R&D vs Eroom's Law (12 methods) ===
biotech = [
    ("高スループット実験スクリーニング", "High-Throughput Screening (HTS)", "RD", "M1", 1990, 9999, "Merck/Pfizer pioneers", "Merck", "USA",
     "https://en.wikipedia.org/wiki/High-throughput_screening",
     "10,000-100,000化合物を1日で自動スクリーニング。微量化・ロボット化で試薬原価と実験時間を劇的に低減", "mature", "verified"),
    ("CRO（受託研究機関）活用", "Contract Research Organization (CRO) Outsourcing", "RD", "M5", 1990, 9999, "Quintiles/IQVIA pioneers", "IQVIA", "USA",
     "https://en.wikipedia.org/wiki/Contract_research_organization",
     "臨床試験・生化学分析・毒性試験を専門CROに委託。インハウス施設削減、スケーラビリティ向上、リスク分散", "mature", "verified"),
    ("AlphaFoldタンパク質構造予測", "AlphaFold Protein Structure Prediction", "RD", "M6", 2020, 9999, "Demis Hassabis et al.", "DeepMind", "GBR",
     "https://deepmind.google/science/alphafold/",
     "従来数年・数十万ドル要したタンパク3D構造予測を92%精度・数分で実現。標的検証〜リード最適化段階の開発時間・実験コスト大幅短縮", "active", "verified"),
    ("分散型臨床試験(DCT)", "Decentralized Clinical Trials (DCT)", "RD", "M5", 2020, 9999, "FDA Guidance (2020-)", "FDA", "USA",
     "https://www.federalregister.gov/documents/2024/09/18/2024-21078/conducting-clinical-trials-with-decentralized-elements",
     "従来集約型治験サイトから患者自宅・地域クリニック・遠隔医療へ。患者リクルート改善、脱落率低減、施設維持コスト削減", "active", "verified"),
    ("実世界根拠(RWE)活用", "Real-World Evidence (RWE) Integration", "RD", "M6", 2018, 9999, "FDA Framework (2018)", "FDA CBER/CDER", "USA",
     "https://www.fda.gov/media/120060/download",
     "電子カルテ・保険請求DB・医療レジストリから実臨床データ取得。従来RCTの対照群を部分置換し治験期間・コスト削減", "active", "verified"),
    ("適応型試験設計(Bayesian)", "Adaptive Trial Design (Bayesian)", "RD", "M3", 2010, 9999, "FDA Guidance + biostatisticians", "FDA", "USA",
     "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry",
     "中間解析データから被験者数・用量を動的調整。Bayesian事前情報活用で不要被験者追加削減、開発期間短縮", "active", "verified"),
    ("クラウドラボ自動化", "Cloud Lab Automation (Strateos/Emerald)", "RD", "M1", 2012, 9999, "Strateos/Emerald Cloud Lab", "Strateos", "USA",
     "https://strateos.com/",
     "リモート制御ロボット実験室でDMTLサイクル自動化。物理化学実験のスケーリングで人件費・スループット改善", "active", "verified"),
    ("医薬品リポジショニング", "Drug Repositioning / Repurposing", "RD", "M5", 2000, 9999, "Pharmaceutical industry", "Multiple", "GLOBAL",
     "https://en.wikipedia.org/wiki/Drug_repositioning",
     "FDA承認既存薬の新適応探索。臨床安全性既知のためPhase I省略可、Phase II-III短縮。開発期間3-12年に圧縮", "mature", "verified"),
    ("CRISPR-Cas9標的検証", "CRISPR-Cas9 Target Validation", "RD", "M3", 2012, 9999, "Doudna/Charpentier", "UC Berkeley", "USA",
     "https://www.nature.com/articles/nature.2015.18190",
     "RNAiより優れた全遺伝子破壊スクリーニング。ゲノムワイドKOライブラリで標的特異性確認、開発初期失敗リスク低減", "mature", "verified"),
    ("AI設計・分子最適化", "AI-Driven Molecular Design (Recursion/Exscientia)", "RD", "M6", 2013, 9999, "Recursion/Exscientia", "Recursion+Exscientia", "USA",
     "https://www.recursion.com/mission",
     "GNN/LLMによる化学空間探索。ヒット同定〜IND導出 42ヶ月→18ヶ月。自動ウェットラボで週間220万サンプル処理", "active", "verified"),
    ("バイオマーカー駆動型治験", "Biomarker-Driven Clinical Trials", "RD", "M3", 2010, 9999, "I-SPY 2 / FDA", "NCI/academic consortia", "USA",
     "https://en.wikipedia.org/wiki/I-SPY_trial",
     "バイオマーカーで患者層別化。適応集団に限定、被験者数削減、統計検出力確保。開発期間圧縮", "active", "verified"),
    ("ベンチャー型リスク分担(Roivant型)", "Venture Risk-Sharing Model", "RD", "M5", 2016, 9999, "Vivek Ramaswamy", "Roivant Sciences", "USA",
     "https://en.wikipedia.org/wiki/Roivant_Sciences",
     "小規模スピンアウト企業に大手製薬の資本・専門知供給。失敗担当者の再投資オプション。初期段階高リスク案件加速", "active", "requires_review"),
]

# === B. Top-tier deepening (10 methods, all派生) ===
top_tier = [
    ("PDSAサイクル", "PDSA Cycle", "MFG", "M3", 1950, 9999, "Deming/Shewhart", "JUSE/Bell Labs", "USA/JPN",
     "https://deming.org/explore/pdsa-cycle/",
     "計画-実施-検証-改善の反復プロセス。統計的仮説検証と学習を組込み。TOC連携で局所改善が全体に波及", "active", "verified"),
    ("Deming 7つの致命的欠陥", "Deming's 7 Deadly Diseases", "MFG", "M3", 1980, 9999, "W. Edwards Deming", "JUSE", "USA",
     "https://deming.org/explore/seven-deadly-diseases/",
     "短期志向・成果主義形骸化・見える数値のみ・部門局所最適化等7組織障害の排除。対症療法不可、経営哲学転換必須", "active", "verified"),
    ("Stage-Gate第3世代", "Stage-Gate Third Generation", "RD", "M3", 2002, 9999, "Robert Cooper (evolution)", "Stage-Gate International", "CAN",
     "https://www.researchgate.net/publication/369378016_The_Stage-Gate_R_System",
     "段階間並列実行+リードタイム短縮+Lean意思決定+ライフサイクルコスト評価+リアルタイムPivot機能。開発期間30-40%短縮", "active", "verified"),
    ("Build-Measure-Learnループ", "Build-Measure-Learn Loop", "RD", "M3", 2008, 9999, "Eric Ries", "IMVU/lean.org", "USA",
     "https://theleanstartup.com/principles",
     "MVP構築→計測→学習→Pivot/Persevere判定。18-24ヶ月開発を6-9ヶ月に短縮。失敗時コスト70-80%削減", "active", "verified"),
    ("Innovation Accounting", "Innovation Accounting", "FIN", "M3", 2011, 9999, "Eric Ries", "lean.org", "USA",
     "https://theleanstartup.com/principles",
     "Validated Learning / Innovation Metrics / Pivot判定の3層学習追跡。6-12ヶ月市場信号遅延を週単位測定", "active", "verified"),
    ("Crystal Methodology", "Crystal Methodology Family", "SW", "M1", 2004, 9999, "Alistair Cockburn", "-", "USA",
     "https://www.toolsqa.com/agile/crystal-method/",
     "チームサイズ別Clear/Yellow/Orange/Red 4段階。通信密度・ドキュメント量を調整。チーム2倍で期間1.3-1.5倍に抑制", "active", "verified"),
    ("Time-Driven ABC", "Time-Driven Activity-Based Costing", "FIN", "M4", 2004, 9999, "Kaplan & Anderson", "HBS", "USA",
     "https://maaw.info/ArticleSummaries/ArtSumKaplanAnderson2007.htm",
     "従来ABCの複雑さを2パラメータに簡略化（供給能力原価率+取引時間）。実装コスト60%減、メンテ工数80%減", "active", "verified"),
    ("BSC戦略マップ統合型", "BSC Strategy Map", "FIN", "M3", 2004, 9999, "Kaplan & Norton", "HBS", "USA",
     "https://www.hbs.edu/ris/Publication%20Files/10-074_0bf3c151-f82b-4592-b885-cdde7f5d97a6.pdf",
     "BSC 4視点を学習→プロセス→顧客→財務の因果鎖に統合。Cascadeで階層化。戦略実行成功率43%→67%", "active", "verified"),
    ("Drum-Buffer-Rope", "Drum-Buffer-Rope Scheduling", "MFG", "M3", 1990, 9999, "Goldratt", "Goldratt Institute", "ISR",
     "https://www.velocityschedulingsystem.com/blog/drum-buffer-rope/",
     "ボトルネック=Drum、前置時間=Buffer、仕事投入=Rope。MRPの全工程容量無視問題を排除、在庫30-50%削減", "active", "verified"),
    ("現地現物・5Why統合", "Genchi Gembutsu + 5 Whys", "MFG", "M3", 1950, 9999, "豊田佐吉/大野耐一", "Toyota", "JPN",
     "https://www.orcalean.com/article/genchi-genbutsu-toyota's-approach-to-quality-and-root-cause-analysis",
     "現場観察→質問の順序。事後レポートを排し物理状態を見てから5Why分析。根本原因到達質問3-4回、再発率15%以下", "active", "verified"),
]

# === C. 21st century latest (8 methods) ===
c21 = [
    ("生成AI支援コード開発(Cursor/Devin)", "Generative AI Code Assistants (Cursor/Devin)", "SW", "M6", 2023, 9999, "Cursor.ai/Cognition", "Cursor/Cognition AI", "USA",
     "https://sacra.com/research/cursor-at-65m-arr/",
     "Cursor IDE統合・Devin自律エージェント。Copilotから派生し開発者意図予測・自律タスク実行で生産性126%向上", "active", "verified"),
    ("DeepSeek V3 効率的事前学習", "DeepSeek V3 Efficient Pre-training", "SW", "M2", 2024, 9999, "DeepSeek-AI", "DeepSeek", "CHN",
     "https://arxiv.org/abs/2412.19437",
     "MoE+推論時計算スケーリングで$5.6M学習コスト。GPT-4比較で1/20以下、Llama 3.1にも肉薄する性能", "active", "verified"),
    ("Google GNoME新材料探索", "Google GNoME Materials Discovery", "RD", "M6", 2023, 9999, "DeepMind", "Google DeepMind", "GBR",
     "https://www.nature.com/articles/s41586-023-06735-9",
     "GNN基盤の結晶構造予測で220万構造を一括発見。Li-ion電池候補25倍増、新材料発見800年分相当を達成", "active", "verified"),
    ("Anthropic Computer Use", "Anthropic Computer Use (Agentic RPA)", "AUTO", "M6", 2024, 9999, "Anthropic", "Anthropic", "USA",
     "https://www.anthropic.com/news/3-5-models-and-computer-use",
     "Claude 3.5 Sonnetが画面認識→クリック→入力を自律実行。従来RPA固定フローを適応的自動化へ転換", "active", "verified"),
    ("量子最適化(QAOA/QAMOO)", "Quantum Optimization (QAOA/QAMOO)", "SCM", "M2", 2017, 9999, "Farhi et al. + IBM/Q-CTRL", "IBM Quantum", "USA",
     "https://research.ibm.com/projects/quantum-optimization",
     "量子近似最適化で組合最適化問題の高速求解。IBM Heron 330,000 CLOPS、Q-CTRLで4倍スケーラビリティ", "active", "requires_review"),
    ("McKinsey QuantumBlack Horizon", "McKinsey QuantumBlack Horizon", "FIN", "M4", 2023, 9999, "McKinsey", "QuantumBlack/AI by McKinsey", "USA",
     "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-2024",
     "生成AI支援の経営コンサル。ProC→本実装期間1-4ヶ月（従来6-18ヶ月）。Gen AI定期使用企業65%（2024）", "active", "verified"),
    ("小型言語モデル(SLM/Phi-3)", "Small Language Models (SLM/Phi-3)", "SW", "M2", 2024, 9999, "Microsoft", "Microsoft", "USA",
     "https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/",
     "3.8Bパラメータで8-13Bモデル相当性能。蒸留+量子化で推論コスト10倍削減、エッジAI実装可能化", "active", "verified"),
    ("OSSファウンデーションモデル戦略", "Open-Source Foundation Models (Llama/DeepSeek)", "SW", "M5", 2023, 9999, "Meta/DeepSeek", "Meta/DeepSeek-AI", "USA/CHN",
     "https://github.com/meta-llama/llama-models",
     "Llama/DeepSeekオープン化で学習コスト$50M→ファインチューニング$100K-1M。市場投入18-24mo→3-6mo", "active", "verified"),
]

# === D. China + Germany + India (15 methods) ===
d_methods = [
    ("山寨(Shanzhai)コスト複製", "Shanzhai Rapid Replication", "HW", "M5", 1995, 2020, "Shenzhen manufacturers", "Shenzhen cluster", "CHN",
     "https://lab.cccb.org/en/the-maker-culture-in-china-ii-shanzhai-emerging-innovation-in-an-open-manufacturing-ecosystem/",
     "設計共有・反復速度向上・既存製品の低コスト複製と段階改善。製造ネットワーク密集で組立労働20-30%削減", "mature", "verified"),
    ("Huawei売上比R&D投資", "Huawei Revenue-Proportional R&D Investment", "RD", "M2", 1998, 9999, "Huawei", "Huawei", "CHN",
     "https://www.huawei.com/en/news/2025/3/annual-report-2024",
     "売上の20-22%を継続的にR&Dに投入。モジュール化と設計反復でNRE削減、制裁下の自給化圧力で加速", "active", "verified"),
    ("深圳ハードウェア高速プロトタイピング", "Shenzhen Rapid Prototyping Ecosystem", "HW", "M5", 2000, 9999, "Shenzhen cluster", "Shenzhen district", "CHN",
     "https://www.diamandis.com/blog/shenzhen-global-hardware-capital",
     "数百サプライヤー地理集中でPCB設計→製造→試作リードタイム3-5日。欧州比1/20コストで多バリ並列試作", "active", "verified"),
    ("BYD垂直統合EV製造", "BYD Vertical Integration", "AUTO", "M5", 2003, 9999, "BYD", "BYD Co.", "CHN",
     "https://evboosters.com/ev-charging-news/the-blueprint-of-an-empire-how-byd-built-global-dominance-through-vertical-integration/",
     "電池・モーター・パワエレ75%内製化。BOM 20-25%削減、設計反復加速、調達不確実性排除", "active", "verified"),
    ("SHEINオンデマンド製造", "SHEIN On-Demand Small-Batch", "MFG", "M6", 2012, 9999, "SHEIN", "SHEIN International", "CHN",
     "https://www.joininflow.io/blogs/shein-and-on-demand-manufacturing-revolutionizing-the-fast-fashion-industry",
     "AI需要予測+50-200着小ロット試作。リードタイム3-7日(Zara 14-21日比)、月3万SKU投入、過剰在庫排除", "active", "verified"),
    ("Industrie 4.0デジタル統合製造", "Industrie 4.0", "MFG", "M6", 2011, 9999, "Acatech/Plattform Industrie 4.0", "Plattform Industrie 4.0", "DEU",
     "https://www.emerald.com/insight/content/doi/10.1108/jmtm-08-2018-0270/full/html",
     "IoT・クラウド・データ分析で資材効率・エネルギー消費・廃棄物削減。サプライチェーン統合最適化、KMU段階導入", "active", "verified"),
    ("Hidden Championsニッチ世界一", "Hidden Champions Niche Strategy", "MFG", "M5", 1996, 9999, "Hermann Simon", "Mittelstand cluster", "DEU",
     "https://en.wikipedia.org/wiki/Hidden_champions",
     "狭ニッチ市場で世界NO.1。スケール効率より専業効率、保守的財務、顧客密着で開発・製造リードタイム短縮", "active", "verified"),
    ("Manufacturing-X データ共有基盤", "Manufacturing-X Digital Data Ecosystem", "MFG", "M5", 2023, 9999, "BMWK/VDMA/Acatech", "Plattform Industrie 4.0", "DEU",
     "https://www.bundeswirtschaftsministerium.de/Redaktion/EN/Dossier/manufacturing-x.html",
     "産業間データ交換セキュア化でバリューチェーン最適化。€150M政府投資で基盤整備、段階別冗長削減", "active", "verified"),
    ("Bauhaus機能追従設計", "Bauhaus Form Follows Function", "ENG", "M4", 1919, 9999, "Bauhaus school", "Bauhaus", "DEU",
     "https://en.wikipedia.org/wiki/Bauhaus",
     "装飾排除・機能忠実設計で部品数・素材種削減、製造工程簡素化。VE・DFMAの先駆思想", "mature", "verified"),
    ("Jugaadイノベーション", "Jugaad Innovation", "RD", "M4", 1990, 9999, "Navi Radjou et al.", "IIT/IIM diaspora", "IND",
     "https://www.naviradjou.com/bookjugaadinnovation",
     "資源制約下の創意工夫。既存部品再利用・簡潔設計でNRE削減。逆境機会化/少で多く/柔軟思考の6原則", "active", "verified"),
    ("Reverse Innovation", "Reverse Innovation", "RD", "M5", 2009, 9999, "Govindarajan/Trimble", "Dartmouth Tuck/GE", "IND",
     "https://hbr.org/2009/10/how-ge-is-disrupting-itself",
     "新興国制約条件を逆活用し最小機能製品を先行開発。低価格を内在化、先進国市場へ機能追加展開", "active", "verified"),
    ("GE Healthcare $500 ECG", "GE Healthcare $500 Portable ECG", "RD", "M4", 2006, 9999, "GE Healthcare India Lab", "GE Healthcare", "IND",
     "https://knowledge.wharton.upenn.edu/article/reverse-innovation-ge-makes-india-a-lab-for-global-markets/",
     "インド農村制約に応じて軽量・バッテリー駆動・1検査10セント。最小機能セットで原価90%削減", "mature", "verified"),
    ("BoP底辺層市場戦略", "Bottom of the Pyramid (BoP) Strategy", "RD", "M5", 2004, 9999, "C.K. Prahalad/Stuart Hart", "U.Michigan/Cornell", "IND",
     "https://saylordotorg.github.io/text_international-business/s17-05-innovation-for-the-bottom-of-t.html",
     "1日$2以下層を価値訴求消費者と再認識。最小機能・材料で生活課題解決、$13T市場（PPP）獲得", "active", "verified"),
    ("UPI ゼロコスト決済基盤", "UPI Zero-Cost Payment Infrastructure", "FIN", "M5", 2016, 9999, "NPCI/RBI", "NPCI", "IND",
     "https://en.wikipedia.org/wiki/Unified_Payments_Interface",
     "金融基盤をデジタル公共財として設計、決済手数料0円。経済全体の決済コスト1/100、$67B経済節約(累計)", "active", "verified"),
    ("Infosys/TCS グローバルデリバリー", "Infosys/TCS Global Network Delivery Model", "SW", "M5", 1999, 9999, "Infosys/TCS", "Infosys/TCS", "IND",
     "https://www.researchgate.net/publication/220500684_Managing_Dispersed_Expertise_in_IT_Offshore_Outsourcing_Lessons_from_Tata_Consultancy_Services",
     "オンショア+ニアショア+オフショアの時間帯・コスト・スキル最適化。24時間開発リレーで30-50%削減", "active", "verified"),
]

# === E. Pre-industrial revolution (10 methods) ===
pre_ind = [
    ("Newcomen大気圧蒸気機関", "Newcomen Atmospheric Engine", "ENERGY", "M6", 1712, 1769, "Thomas Newcomen", "Conygree Coalworks", "GBR",
     "https://en.wikipedia.org/wiki/Newcomen_atmospheric_engine",
     "蒸気凝縮で部分真空生成、大気圧でピストン推動。馬力・人力比で炭鉱排水コスト40%削減、英欧で数百台稼働", "legacy", "verified"),
    ("Smeaton蒸気機関改良", "Smeaton Steam Engine Improvements", "ENERGY", "M3", 1770, 1790, "John Smeaton", "Austhorpe Experimental", "GBR",
     "https://collection.sciencemuseumgroup.org.uk/objects/co50899/atmospheric-engine-by-john-smeaton-1772-models-atmospheric-engines-newcomen-engines",
     "Newcomen機を130回の実験で体系改善。Long Benton Colliery(1774)で従来比効率25%向上。科学的計測・改善のプロト", "legacy", "verified"),
    ("Boulton&Watt ロイヤリティ制", "Boulton & Watt Royalty Licensing", "FIN", "M5", 1775, 1800, "Boulton/Watt", "Soho Works", "GBR",
     "https://en.wikipedia.org/wiki/Boulton_and_Watt",
     "エンジン売却でなくライセンス+ロイヤリティ方式。顧客が削減した燃料コストの1/3を支払うインセンティブ一致モデル", "mature", "verified"),
    ("Adam Smith 分業論", "Adam Smith Division of Labor", "MFG", "M1", 1776, 1850, "Adam Smith", "U.Glasgow", "GBR",
     "https://www.adamsmithworks.org/pin_factory.html",
     "国富論ピン工場例：18細分化作業で10人1日4.8万本（1人4800本）。独立者1-20本/日比240倍超の産出", "active", "verified"),
    ("Wedgwood Etruria品質統制", "Wedgwood Etruria Quality Control", "MFG", "M3", 1769, 1900, "Josiah Wedgwood", "Etruria Works", "GBR",
     "https://en.wikipedia.org/wiki/Etruria_Works",
     "労働分化・機械化・厳格品質基準・打刻時間規律。高級市場と量産プロセスの両立、欧州陶磁器近代化テンプレート", "legacy", "verified"),
    ("Arkwright水力紡績工場", "Arkwright Water-Powered Factory System", "MFG", "M1", 1769, 1830, "Richard Arkwright", "Cromford Mill", "GBR",
     "https://en.wikipedia.org/wiki/Cromford_Mill",
     "96本紡錘同時の水力フレーム+24時間2班シフト制。機械力×時間規律=近代工場制度の源流", "legacy", "verified"),
    ("Flying Shuttle 飛び梭機", "Flying Shuttle", "MFG", "M1", 1733, 1780, "John Kay", "Bury Lancashire", "GBR",
     "https://en.wikipedia.org/wiki/Flying_shuttle",
     "横糸自動往復装置で1人織人で広幅布織成可能化。生産性2倍。糸不足の危機を惹起しSpinning Jennyを刺激", "legacy", "verified"),
    ("Spinning Jenny", "Spinning Jenny", "MFG", "M2", 1764, 1780, "James Hargreaves", "Stanhill Lancashire", "GBR",
     "https://en.wikipedia.org/wiki/Spinning_jenny",
     "8本紡錘同時（後120本）。単一操者で従来比8倍産出。家内手工業範囲内の劇的増産", "legacy", "verified"),
    ("Wilkinson孔径加工機", "Wilkinson Boring Machine", "MFG", "M3", 1774, 1850, "John Wilkinson", "Bradley Ironworks", "GBR",
     "https://en.wikipedia.org/wiki/John_Wilkinson_(industrialist)",
     "両端支持で剛性向上、シリンダー孔の高精度加工。Watt蒸気機関の漏洩低減→効率向上を可能化、最初の工作機械", "active", "verified"),
    ("Josiah Wedgwood 高級ブランド戦略", "Wedgwood Premium Brand Strategy", "MFG", "M4", 1769, 1900, "Josiah Wedgwood", "Etruria Works", "GBR",
     "https://www.vam.ac.uk/articles/wedgwood-an-introduction",
     "「Wedgwood & Bentley」マークと王室御用達戦略で高単価×量産両立。コスト削減でなく価値向上による利益最大化のモデル", "legacy", "verified"),
]


def insert_methods(records, start_n):
    rows = []
    n = start_n
    for r in records:
        mid = f"CDH-MET-{n:04d}"
        rows.append((mid, *r))
        n += 1
    c.executemany("INSERT INTO methods VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    return rows


next_n = last_n + 1
a_rows = insert_methods(biotech, next_n); next_n += len(a_rows)
b_rows = insert_methods(top_tier, next_n); next_n += len(b_rows)
c_rows = insert_methods(c21, next_n); next_n += len(c_rows)
d_rows = insert_methods(d_methods, next_n); next_n += len(d_rows)
e_rows = insert_methods(pre_ind, next_n); next_n += len(e_rows)

print(f"Inserted: A={len(a_rows)} B={len(b_rows)} C={len(c_rows)} D={len(d_rows)} E={len(e_rows)} = {len(a_rows)+len(b_rows)+len(c_rows)+len(d_rows)+len(e_rows)}")

# Build name → id map for genealogy/evidence
all_rows = a_rows + b_rows + c_rows + d_rows + e_rows
name_to_id = {r[1]: r[0] for r in all_rows}

# === Evidence (selected key numbers) ===
ev_n = c.execute("SELECT evidence_id FROM evidence ORDER BY evidence_id DESC LIMIT 1").fetchone()[0]
ev_n = int(ev_n.split("-")[-1]) + 1

def ev_id():
    global ev_n
    eid = f"CDH-EVD-{ev_n:04d}"
    ev_n += 1
    return eid

evidence = [
    # Biotech
    (ev_id(), name_to_id["AlphaFoldタンパク質構造予測"], "structure_db_growth", 214000000.0, "proteins", "2021年35万構造", "AlphaFold DB", 2024, "https://academic.oup.com/nar/article/52/D1/D368/7337620"),
    (ev_id(), name_to_id["分散型臨床試験(DCT)"], "retention_rate_improvement", 96.0, "%", "従来70-80%", "Medable DCT Phase 4", 2020, "https://www.castoredc.com/insight-briefs/decentralized-clinical-trial-platforms-in-2025-a-practical-guide-for-clinical-operations/"),
    (ev_id(), name_to_id["クラウドラボ自動化"], "cost_savings_usd_annual", 40000000.0, "USD/yr", "従来インハウス", "Exscientia post-merge", 2024, "https://www.cio.inc/how-exscientia-reduces-drug-discovery-time-with-gen-ai-a-23015"),
    (ev_id(), name_to_id["AI設計・分子最適化"], "timeline_reduction_pct", 57.1, "%", "従来42ヶ月", "Recursion 18ヶ月", 2024, "https://www.cnbc.com/2024/05/10/recursion-pharmaceuticals-ceo-says-ai-speeds-up-new-drug-development.html"),
    (ev_id(), name_to_id["医薬品リポジショニング"], "approval_rate_pct", 30.0, "%", "従来11%", "Repurposed drug pathway", 2024, "https://en.wikipedia.org/wiki/Drug_repositioning"),
    # Top-tier
    (ev_id(), name_to_id["Time-Driven ABC"], "implementation_cost_reduction_pct", 60.0, "%", "従来ABC", "Kaplan&Anderson industry surveys", 2007, "https://maaw.info/ArticleSummaries/ArtSumKaplanAnderson2007.htm"),
    (ev_id(), name_to_id["Drum-Buffer-Rope"], "inventory_reduction_pct", 45.0, "%", "従来MRP", "Industry TOC case studies", 2000, "https://www.velocityschedulingsystem.com/blog/drum-buffer-rope/"),
    (ev_id(), name_to_id["BSC戦略マップ統合型"], "execution_success_rate_pct", 67.0, "%", "未導入43%", "Global survey", 2010, "https://www.hbs.edu/ris/Publication%20Files/10-074_0bf3c151-f82b-4592-b885-cdde7f5d97a6.pdf"),
    # 21C
    (ev_id(), name_to_id["生成AI支援コード開発(Cursor/Devin)"], "productivity_increase_pct", 126.0, "%", "ベースライン", "Cursor users", 2024, "https://sacra.com/research/cursor-at-65m-arr/"),
    (ev_id(), name_to_id["DeepSeek V3 効率的事前学習"], "training_cost_usd_M", 5.576, "USD millions", "GPT-4推定$100M", "DeepSeek V3", 2024, "https://arxiv.org/abs/2412.19437"),
    (ev_id(), name_to_id["Google GNoME新材料探索"], "structures_discovered", 2200000.0, "crystals", "従来年間50-100件", "GNoME 2023", 2023, "https://www.nature.com/articles/s41586-023-06735-9"),
    (ev_id(), name_to_id["小型言語モデル(SLM/Phi-3)"], "inference_cost_reduction_ratio", 10.0, "x", "従来8-13Bモデル", "Phi-3-mini", 2024, "https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/"),
    # D regions
    (ev_id(), name_to_id["Huawei売上比R&D投資"], "rd_pct_revenue", 21.8, "%", "業界平均5-10%", "Huawei 2025 Annual Report", 2025, "https://techafricanews.com/2026/04/07/huawei-invests-27-5bn-in-rd-in-2025-accounting-for-21-8-of-revenue/"),
    (ev_id(), name_to_id["深圳ハードウェア高速プロトタイピング"], "lead_time_days", 4.0, "days", "欧州60-90日", "Shenzhen typical", 2022, "https://innovationlabasia.dk/en/shenzhen-the-spot-for-rapid-prototyping/"),
    (ev_id(), name_to_id["BYD垂直統合EV製造"], "battery_cost_reduction_pct", 40.0, "%", "業界平均", "BYD LFP battery", 2024, "https://www.linkedin.com/pulse/super-low-lfp-battery-costs-byds-advantage-through-vertical-hesami-hqebf"),
    (ev_id(), name_to_id["SHEINオンデマンド製造"], "lead_time_days", 5.0, "days", "Zara 14-21日", "SHEIN typical", 2023, "https://www.peterfisk.com/gamechanger/shein/"),
    (ev_id(), name_to_id["Industrie 4.0デジタル統合製造"], "annual_productivity_growth_pct", 3.6, "%/yr", "EU平均1.5%", "German manufacturing", 2018, "https://downloads.unido.org/ot/11/71/11712839/WP_22.pdf"),
    (ev_id(), name_to_id["GE Healthcare $500 ECG"], "cost_reduction_pct", 90.0, "%", "従来ECG $5000+", "GE India MAC 400", 2009, "https://knowledge.wharton.upenn.edu/article/reverse-innovation-ge-makes-india-a-lab-for-global-markets/"),
    (ev_id(), name_to_id["UPI ゼロコスト決済基盤"], "economic_savings_usd_B_cumulative", 67.0, "USD billions", "2016年比", "ADB analysis", 2024, "https://www.adb.org/sites/default/files/publication/964626/adb-brief-299-india-unified-payments-interface.pdf"),
    # Pre-industrial
    (ev_id(), name_to_id["Newcomen大気圧蒸気機関"], "operating_cost_reduction_pct", 40.0, "%", "馬力・人力", "英国炭鉱(Tipton)", 1715, "https://www.britannica.com/technology/Newcomen-steam-engine"),
    (ev_id(), name_to_id["Smeaton蒸気機関改良"], "efficiency_improvement_pct", 25.0, "%", "Newcomen標準", "Long Benton Colliery", 1774, "https://www.ice.org.uk/news-views-insights/inside-infrastructure/smeaton-vs-watt-the-steam-engine-rivalry"),
    (ev_id(), name_to_id["Boulton&Watt ロイヤリティ制"], "total_royalty_gbp", 180000.0, "GBP", "Cornwall累計", "B&W Cornwall licenses", 1800, "https://en.wikipedia.org/wiki/Boulton_and_Watt"),
    (ev_id(), name_to_id["Adam Smith 分業論"], "productivity_ratio", 240.0, "x", "独立者1-20本/日", "Pin factory example", 1776, "https://www.marxists.org/reference/archive/smith-adam/works/wealth-of-nations/book01/ch01.htm"),
    (ev_id(), name_to_id["Arkwright水力紡績工場"], "spindle_parallelization", 96.0, "spindles", "手紡ぎ1本", "Cromford Mill", 1771, "https://en.wikipedia.org/wiki/Water_frame"),
    (ev_id(), name_to_id["Spinning Jenny"], "spindle_parallelization", 8.0, "spindles", "手紡ぎ1本", "Hargreaves initial", 1764, "https://en.wikipedia.org/wiki/Spinning_jenny"),
]
c.executemany("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?)", evidence)
print(f"Evidence added: {len(evidence)}")

# === Genealogy (linking new to existing) ===
gen_n = c.execute("SELECT rel_id FROM genealogy ORDER BY rel_id DESC LIMIT 1").fetchone()[0]
gen_n = int(gen_n.split("-")[-1]) + 1

def gen_id():
    global gen_n
    rid = f"CDH-REL-{gen_n:04d}"
    gen_n += 1
    return rid

# Lookup helpers for existing methods (by method_id)
existing = {
    "AI創薬": "CDH-MET-0247",  # existing
    "Stage-Gate法": "CDH-MET-0241",
    "リーン・スタートアップ": "CDH-MET-0246",
    "ABC": "CDH-MET-0062",
    "BSC": "CDH-MET-0063",
    "TOC": "CDH-MET-0064",
    "TPS": "CDH-MET-0010",
    "Deming14": "CDH-MET-0021",
    "Agile": "CDH-MET-0144",
    "Watt": "CDH-MET-0280",
    "TPM": "CDH-MET-0015",
}

genealogy_data = [
    # A. Biotech
    (gen_id(), existing["AI創薬"], name_to_id["AI設計・分子最適化"], "derives", 2013, "AI創薬の産業応用形態（Recursion/Exscientia統合）"),
    # B. Top-tier deepening
    (gen_id(), existing["Deming14"], name_to_id["PDSAサイクル"], "derives", 1950, "14原則の実装プロセス"),
    (gen_id(), existing["Deming14"], name_to_id["Deming 7つの致命的欠陥"], "integrates", 1980, "14原則達成の前提条件としての欠陥排除"),
    (gen_id(), existing["Stage-Gate法"], name_to_id["Stage-Gate第3世代"], "supersedes", 2002, "初版1988→Agile融合の第3世代"),
    (gen_id(), existing["リーン・スタートアップ"], name_to_id["Build-Measure-Learnループ"], "derives", 2008, "Lean Startupの中核反復ループ"),
    (gen_id(), name_to_id["Build-Measure-Learnループ"], name_to_id["Innovation Accounting"], "integrates", 2011, "BMLループの計測体系"),
    (gen_id(), existing["Agile"], name_to_id["Crystal Methodology"], "derives", 2004, "Agile思想のチームサイズ別実装"),
    (gen_id(), existing["ABC"], name_to_id["Time-Driven ABC"], "supersedes", 2004, "ABC複雑性解決の進化形"),
    (gen_id(), existing["BSC"], name_to_id["BSC戦略マップ統合型"], "integrates", 2004, "4視点を因果鎖に統合"),
    (gen_id(), existing["TOC"], name_to_id["Drum-Buffer-Rope"], "derives", 1990, "TOCのスケジューリング実装"),
    (gen_id(), existing["TPS"], name_to_id["現地現物・5Why統合"], "integrates", 1950, "TPS品質改善の中核手法"),
    # C. 21st century
    (gen_id(), "CDH-MET-0154", name_to_id["生成AI支援コード開発(Cursor/Devin)"], "derives", 2023, "Copilot(2021)の派生：Cursor/Devin"),
    # E. Pre-industrial
    (gen_id(), name_to_id["Newcomen大気圧蒸気機関"], name_to_id["Smeaton蒸気機関改良"], "derives", 1770, "Newcomenの実験的改良"),
    (gen_id(), name_to_id["Smeaton蒸気機関改良"], existing["Watt"], "inspires", 1769, "Smeaton改良に並行しWattが分離凝縮器で根本解決"),
    (gen_id(), existing["Watt"], name_to_id["Boulton&Watt ロイヤリティ制"], "integrates", 1775, "技術発明をビジネスモデル化"),
    (gen_id(), name_to_id["Adam Smith 分業論"], name_to_id["Arkwright水力紡績工場"], "inspires", 1771, "分業理論の工場制度実装"),
    (gen_id(), name_to_id["Flying Shuttle 飛び梭機"], name_to_id["Spinning Jenny"], "derives", 1764, "Shuttle による糸不足危機への応答"),
    (gen_id(), name_to_id["Wilkinson孔径加工機"], existing["Watt"], "integrates", 1774, "高精度シリンダ加工がWatt機の実用化を可能化"),
    # Adam Smith → Taylor scientific management
    (gen_id(), name_to_id["Adam Smith 分業論"], "CDH-MET-0001", "inspires", 1911, "分業論からTaylor科学的管理法への発展"),
]
c.executemany("INSERT INTO genealogy VALUES (?,?,?,?,?,?)", genealogy_data)
print(f"Genealogy added: {len(genealogy_data)}")

# === Critiques (selected) ===
crt_n = c.execute("SELECT critique_id FROM critiques ORDER BY critique_id DESC LIMIT 1").fetchone()[0]
crt_n = int(crt_n.split("-")[-1]) + 1

def crt_id():
    global crt_n
    cid = f"CDH-CRT-{crt_n:04d}"
    crt_n += 1
    return cid

critiques = [
    (crt_id(), name_to_id["実世界根拠(RWE)活用"], "Regulatory science community", 2022, "data_quality_variability", "EHRシステム間のRWEデータ品質不均一、因果推論妥当性に未解決議論", "https://sciencedirect.com/article/pii/S1098301520322026"),
    (crt_id(), name_to_id["CRISPR-Cas9標的検証"], "Off-target safety critics", 2023, "off_target_effects", "CRISPRスケーリング時のoff-target効果、in vivo送達の複雑性", "https://pubmed.ncbi.nlm.nih.gov/25572406/"),
    (crt_id(), name_to_id["ベンチャー型リスク分担(Roivant型)"], "Pharma integration analysts", 2023, "cultural_integration_risk", "スピンアウト文化と大手製薬官僚体制の衝突", "https://adus.substack.com/p/how-does-roivant-work"),
    (crt_id(), name_to_id["量子最適化(QAOA/QAMOO)"], "Quantum computing realists", 2024, "noisy_nisq_limitation", "NISQ段階(エラー率10^-3)、古典アルゴリズムとの実質的優位性が限定的", "https://q-ctrl.com/blog/q-ctrl-transforms-quantum-advantage-outlook-breaking-previous-records-for-optimization-problems-and-outperforming-competitive-technologies-for-optimization-problems-and-outperforming-competitive-technologies/"),
    (crt_id(), name_to_id["山寨(Shanzhai)コスト複製"], "IP enforcement community", 2010, "intellectual_property_violation", "知的財産侵害問題、ブランド希釈、貿易摩擦の起点", "https://lab.cccb.org/en/the-maker-culture-in-china-ii-shanzhai-emerging-innovation-in-an-open-manufacturing-ecosystem/"),
    (crt_id(), name_to_id["SHEINオンデマンド製造"], "Sustainability researchers", 2023, "environmental_labor_concerns", "超ファストファッションによる環境負荷増加、労働条件問題", "https://www.peterfisk.com/gamechanger/shein/"),
    (crt_id(), name_to_id["BoP底辺層市場戦略"], "Development economists", 2015, "limited_poverty_alleviation", "BoP戦略は市場アクセス改善はするが、貧困削減効果は限定的", "https://saylordotorg.github.io/text_international-business/s17-05-innovation-for-the-bottom-of-t.html"),
]
c.executemany("INSERT INTO critiques VALUES (?,?,?,?,?,?,?)", critiques)
print(f"Critiques added: {len(critiques)}")

conn.commit()

# Verify
m_count = c.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
e_count = c.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
g_count = c.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0]
cr_count = c.execute("SELECT COUNT(*) FROM critiques").fetchone()[0]
print(f"\nFinal: methods={m_count} evidence={e_count} genealogy={g_count} critiques={cr_count}")

conn.close()
