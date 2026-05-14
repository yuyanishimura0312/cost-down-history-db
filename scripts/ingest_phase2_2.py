#!/usr/bin/env python3
"""Phase 2.2 ingest: 93 methods from 7 parallel teams (F/G/H/I/J/K/L)."""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "cdh.sqlite"
conn = sqlite3.connect(DB)
c = conn.cursor()

# Get last method_id
row = c.execute("SELECT method_id FROM methods ORDER BY method_id DESC LIMIT 1").fetchone()
last_n = int(row[0].split("-")[-1])
print(f"Last method_id: {row[0]} (next: CDH-MET-{last_n+1:04d})")

# Ensure new domains exist
c.executemany("INSERT OR IGNORE INTO domains VALUES (?,?,?)", [
    ("AGRI", "農業", "Agriculture"),
    ("FOOD", "食品加工・流通", "Food Processing & Distribution"),
    ("HC", "ヘルスケア", "Healthcare"),
    ("EDU", "教育", "Education"),
])

# === F. Precision Agriculture (15) ===
f_methods = [
    ("可変施肥(VRA)", "Variable Rate Application", "AGRI", "M4", 2000, 9999, "USDA pioneers", "USDA", "USA", "https://geopard.tech/blog/variable-rate-application-technology-in-precision-agriculture/", "GPS/GIS連動の処方箋図で施肥・農薬・種子を土壌特性に応じ段階的配分", "active", "verified"),
    ("ドローン農業散布", "Agricultural Spraying Drones", "AGRI", "M6", 2015, 9999, "DJI Agras team", "DJI", "CHN", "https://ag.dji.com/", "GPS同期八軸ドローンで精密農薬散布。従来比80-90%化学薬品削減", "active", "verified"),
    ("AI土壌診断(FarmBeats)", "Microsoft FarmBeats", "AGRI", "M6", 2017, 9999, "Ranveer Chandra", "Microsoft Research", "USA", "https://www.microsoft.com/en-us/research/project/farmbeats-iot-agriculture/", "低コストセンサ+ドローン+ML。水分・pH・温度を予測推定", "active", "verified"),
    ("CRISPR-Edited作物", "CRISPR-Edited GABA Tomato", "AGRI", "M6", 2020, 9999, "Sanatech Seed", "Sanatech Seed Co.", "JPN", "https://sanatech-seed.com/en/20201211-2-2/", "ゲノム編集GABA代謝シャント操作。育種10年→3-5年", "active", "verified"),
    ("エアロポニック垂直農法", "Aeroponic Vertical Farming", "AGRI", "M5", 2004, 9999, "David Rosenberg", "AeroFarms", "USA", "https://www.aerofarms.com/this-vertical-farm-uses-95-less-water-and-no-soil/", "霧状根部灌漑+密閉循環。水95%削減、土壌無使用", "active", "verified"),
    ("Plantix病害虫AI", "Plantix Disease Detection AI", "AGRI", "M6", 2015, 9999, "PEAT", "Plantix/PEAT", "DEU", "https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/programme/agritech/detecting-and-managing-crop-pests-and-diseases-with-ai-insights-from-plantix/", "深層学習60作物800症状識別、診断精度90%+", "active", "verified"),
    ("自律除草レーザー", "Carbon Robotics LaserWeeder", "AGRI", "M1", 2018, 9999, "Carbon Robotics", "Carbon Robotics", "USA", "https://carbonrobotics.com/laserweeder", "30レーザ搭載八輪クローラ、200K雑草/時間、化学除草不要", "active", "verified"),
    ("精密滴灌(Netafim)", "Drip Irrigation Technology", "AGRI", "M4", 1965, 9999, "Simcha Blass", "Netafim", "ISR", "https://www.netafimusa.com/agriculture/drip-irrigation/", "直接根部灌漑で水利用効率95-100%、従来比水50%削減", "mature", "verified"),
    ("衛星リモートセンシング", "Planet Labs Satellite Monitoring", "AGRI", "M6", 2010, 9999, "Planet founders", "Planet Labs", "USA", "https://www.planet.com/", "CubeSat Dove毎日全球画像。植生指数・収量予測リアルタイム", "active", "verified"),
    ("Climate FieldView", "Climate FieldView", "AGRI", "M6", 2014, 9999, "Climate Corporation", "Climate/Bayer", "USA", "https://climate.com/en-us/solutions/analyze-data.html", "衛星+気象+IoT統合需要予測。種子処方箋で+5 bu/ac", "active", "verified"),
    ("マーカー支援選抜育種(MAS)", "Marker-Assisted Selection", "AGRI", "M6", 1990, 9999, "Lande/Thompson", "Multiple breeding programs", "USA", "https://pmc.ncbi.nlm.nih.gov/articles/PMC2610170/", "DNA分子マーカーによる品種選抜。育種期間7-10年短縮", "mature", "verified"),
    ("Apeel食品コーティング", "Apeel Sciences Edible Coating", "FOOD", "M3", 2012, 9999, "James Rogers", "Apeel Sciences", "USA", "https://www.digicomply.com/blog/apeel-sciences-edible-coating-extending-shelf-life-sustainably/", "植物キューティクル模倣で保持期間2倍、冷蔵不要", "active", "verified"),
    ("IBM Food Trust", "IBM Food Trust Blockchain", "FOOD", "M6", 2017, 9999, "Brigid McDermott", "IBM Food Trust", "USA", "https://www.ledgerinsights.com/ibm-food-trust-blockchain-cost-food-traceability/", "Hyperledger Fabric許可型でWalmart等10社参加。マンゴー追跡7日→2.2秒", "active", "verified"),
    ("スマート養殖IoT(AKVA)", "Smart Fish Farming IoT", "FOOD", "M6", 2023, 9999, "AKVA Group", "AKVA Group", "NOR", "https://www.marketsandmarkets.com/Market-Reports/precision-aquaculture-market-242307580.html", "給餌自動化+魚行動センサ。エアレーション35%エネ削減", "active", "verified"),
    ("Naïo農業ロボット", "Naïo Agricultural Robots", "AGRI", "M1", 2011, 9999, "Naïo Technologies", "Naïo Technologies", "FRA", "https://www.naio-technologies.com/en/naio-technologies/", "OZ/Orio/Tedロボット。300kg運搬・除草・耕耘モジュラー", "active", "verified"),
]

# === G. Healthcare (15) ===
g_methods = [
    ("テレメディシン", "Telemedicine & Virtual Care", "HC", "M5", 2002, 9999, "Teladoc founders", "Teladoc", "USA", "https://www.pennmedicine.org/news/study-finds-telemedicine-visits-cost-far-less-than-office-visits", "遠隔診療で対面医療の1/5コスト(平均$400低減、80%削減)、低所得地域94%", "active", "verified"),
    ("成果払い・バンドル支払い(BPCI)", "Value-Based Care / BPCI", "HC", "M4", 2013, 9999, "CMS Innovation", "CMS", "USA", "https://www.cms.gov/priorities/innovation/innovation-models/bundled-payments", "手術エピソード1件あたり$324削減。BPCI-Advanced(2021)で病院90日支払い最適化", "active", "verified"),
    ("AI診断支援(IDx-DR)", "AI Diagnostic Support (IDx-DR)", "HC", "M6", 2018, 9999, "Michael Abramoff", "Digital Diagnostics/IDx", "USA", "https://www.retina-specialist.com/article/ai-for-dr-screening-where-are-we-in-2025", "2018 FDA初承認AI網膜症診断。検査1患者$2.71-3.82削減、眼科紹介自動化", "active", "verified"),
    ("遠隔患者監視(RPM)", "Remote Patient Monitoring", "HC", "M6", 2017, 9999, "Philips Healthcare", "Philips/CHS", "USA", "https://www.nature.com/articles/s41746-024-01182-w", "心不全・糖尿患者の在宅監視で30-50%再入院削減、CMSペナルティ$22,640/患者回避", "active", "verified"),
    ("精密医学・ゲノム検査", "Precision Medicine Genomic Testing", "HC", "M3", 2010, 9999, "Foundation Medicine/Tempus", "Tempus", "USA", "https://www.tempus.com/oncology/genomic-profiling/", "Oncotype DX等で化学療法不要症例特定、治療コスト30-50%削減", "active", "verified"),
    ("Hospital at Home", "Hospital at Home", "HC", "M5", 1995, 9999, "Johns Hopkins", "JHU", "USA", "https://www.cms.gov/newsroom/fact-sheets/fact-sheet-report-study-acute-hospital-care-home-initiative", "急性期治療を自宅で。LOS短縮+30%再入院低減+医療関連感染防止", "active", "verified"),
    ("Virginia Mason Lean Six Sigma", "Virginia Mason Lean Six Sigma Hospital", "HC", "M3", 2002, 9999, "Virginia Mason team", "Virginia Mason Medical Center", "USA", "https://www.qimacros.com/lean-six-sigma-articles/vmmc-case-study/", "Toyota生産方式を病院統合。検査時間85%短縮、ラボエラー74%減、資本$11M削減", "active", "verified"),
    ("ジェネリック医薬品法(Hatch-Waxman)", "Hatch-Waxman Act Generics", "HC", "M5", 1984, 9999, "US Congress", "FDA", "USA", "https://accessiblemeds.org/resources/press-releases/40-years-hatch-waxman-trillions-savings-patients/", "処方90%がジェネリック・医薬品費の13%。2024年単年$467B削減、累計$3.4T", "active", "verified"),
    ("電子カルテEHR(HITECH)", "Electronic Health Records (HITECH)", "HC", "M6", 2009, 9999, "Epic/Cerner pioneers", "HHS HITECH", "USA", "https://www.ajmc.com/view/association-of-electronic-health-records-with-cost-savings-in-a-national-sample", "EHR採用率3.2%→14.2%。導入病院運営コスト9.66%削減", "active", "verified"),
    ("Group Purchasing Organizations(GPO)", "Group Purchasing Organizations", "HC", "M5", 1990, 9999, "Premier/Vizient", "Premier/Vizient/HealthTrust", "USA", "https://www.supplychainassociation.org/wp-content/uploads/2018/05/Leibowitz_GPO_Report.pdf", "医療用品集団購買で10-18%削減、全医療システム年$55B削減", "mature", "verified"),
    ("Mayo Clinic統合ケア", "Mayo Clinic Integrated Care Model", "HC", "M3", 1990, 9999, "Mayo Clinic", "Mayo Clinic", "USA", "https://www.commonwealthfund.org/sites/default/files/documents/___media_files_publications_case_study_2009_aug_1306_mccarthy_mayo_case_study.pdf", "多職種統合チーム+給与制+患者コーディネーター。共有EHRで重複検査削減", "active", "verified"),
    ("薬剤給付管理(PBM)", "Pharmacy Benefit Managers", "HC", "M5", 1980, 9999, "CVS/Express Scripts/OptumRx", "CVS Caremark", "USA", "https://www.ftc.gov/system/files/ftc_gov/pdf/pharmacy-benefit-managers-staff-report.pdf", "2億7,000万人処方薬カバー。保険者-薬局価格交渉とリベートで中間コスト削減", "active", "requires_review"),
    ("Medicare請求処理効率化", "Medicare Administrative Efficiency", "HC", "M6", 1965, 9999, "CMS", "CMS/MAC", "USA", "https://www.cms.gov/", "Medicare行政コスト年2%伸び(全医療費4.8%対比)。自動化・標準化", "active", "verified"),
    ("参照価格制(EU EURIPID)", "Reference Pricing / External Benchmarking", "HC", "M5", 2010, 9999, "EU/EMA", "EMA/EURIPID", "EU", "https://health.ec.europa.eu/system/files/2016-11/erp_reimbursement_medicinal_products_en.pdf", "EU27カ国の医薬品価格調和で新規薬の過度高価格化回避", "active", "verified"),
    ("投薬アドヒアランスAI監視(Proteus)", "AI-Powered Medication Adherence", "HC", "M6", 2017, 9999, "Proteus Digital Health", "Proteus", "USA", "https://www.sciencedirect.com/science/article/pii/S1544319124003029", "飲込みセンサー+AI監視で6ヶ月26.5%アドヒアランス改善、精神科入院21.3%減", "active", "requires_review"),
]

# === H. Defense COTS (12) ===
h_methods = [
    ("COTS調達(Perry Memo)", "COTS Procurement (Perry Memo)", "SCM", "M5", 1994, 9999, "William Perry", "US DoD", "USA", "https://militaryembedded.com/radar-ew/signal-processing/cots-procurement-years-the-perry-memo", "商用既製品最大限採用指示でFASA法制化、展開時間25-35%削減", "mature", "verified"),
    ("Agile Software Acquisition", "DoD Agile Software Acquisition", "SCM", "M1", 2020, 9999, "DoD FY20 NDAA", "US DoD", "USA", "https://aaf.dau.edu/aaf/software/", "段階的開発+頻繁デリバリー。ソフトリリース周期419日→58日(87%削減)", "active", "verified"),
    ("3D Printing予備部品(RAPTOR)", "3D Printing for Spare Parts (RAPTOR)", "SCM", "M6", 2019, 9999, "US Army CCDC", "US Army/SpaceX", "USA", "https://www.army.mil/article/217433/3d_printing_technology_enhancing_logistics_for_army", "RAPTORレポジトリ140+部品。生産時間80%削減、在庫保有コスト削減", "active", "verified"),
    ("Software Defined Radio(JTRS)", "Software Defined Radio Procurement", "ENG", "M5", 1997, 2007, "DoD JTRS office", "US DoD", "USA", "https://www.govinfo.gov/content/pkg/GAOREPORTS-GAO-06-955/html/GAOREPORTS-GAO-06-955.htm", "SDRで固定化回避狙うも$14.4B→$37Bコスト超過。失敗から要件管理・成熟度検証重要性立証", "legacy", "verified"),
    ("Multi-Year Procurement(MYP)", "Multi-Year Procurement", "FIN", "M2", 1980, 9999, "Reagan-era DoD", "US DoD", "USA", "https://www.congress.gov/crs-product/R41909", "複数年契約で生産スケール経済。経済発注量+生産性インセンティブで5-15%削減", "mature", "verified"),
    ("Modular Open Systems Approach", "Modular Open Systems Approach (MOSA)", "ENG", "M5", 2004, 9999, "DoD CTO", "US DoD", "USA", "https://www.cto.mil/sea/mosa/", "2019 NDAAで全大型調達義務化。モジュール化・疎結合・段階的能力開発で競争促進", "active", "verified"),
    ("IDIQ Contracts", "Indefinite Delivery/Indefinite Quantity", "FIN", "M5", 2000, 9999, "GSA/DoD", "GSA/DoD", "USA", "https://www.congress.gov/crs-product/IF12558", "不確定数量契約で柔軟性確保。FY2024でDoD契約発注の56%がIDV", "mature", "verified"),
    ("Defense Innovation Unit(DIU)", "Defense Innovation Unit", "SCM", "M5", 2015, 9999, "Ash Carter", "US DoD/DIU", "USA", "https://www.diu.mil/about", "民間技術DoD迅速導入。R&D 5-10年→2年以下、プロトタイプ契約450件、民間投資$68B", "active", "verified"),
    ("Other Transaction Authority(OTA)", "Other Transaction Authority Prototyping", "FIN", "M5", 2015, 9999, "DoD/AFWERX", "DoD/AFWERX/SOFWERX", "USA", "https://aida.mitre.org/ota/", "FAR外の迅速契約。AFWERX/SOFWERXイノベ拠点が非伝統的企業協働促進", "active", "verified"),
    ("Performance-Based Logistics(PBL)", "Performance-Based Logistics", "FIN", "M4", 2001, 9999, "DoD QDR", "US DoD/Lockheed", "USA", "https://breakingdefense.com/2021/09/new-f-35-sustainment-deal-creates-path-to-lockheed-multi-year-pbl-contract/", "成果契約型。F-35 Lockheedで飛行時間あたりコスト過去7年で50%削減、さらに35%予測", "active", "verified"),
    ("SBIR/STTR Phase III", "SBIR/STTR Phase III Commercialization", "SCM", "M5", 1982, 9999, "US Congress", "DoD SBIR/STTR", "USA", "https://www.defensesbirsttr.mil/SBIR-STTR/", "Phase III商用化段階。DoD外部資金活用で開発リスク分散・市場導入加速", "active", "verified"),
    ("CMMC 2.0調達統合", "Cybersecurity Maturity Model Certification 2.0", "FIN", "M3", 2024, 9999, "DoD CIO", "DoD CIO", "USA", "https://dodcio.defense.gov/cmmc/About/", "DIB契約者338,000+に3階層サイバー要件。セキュリティ・バイ・デザイン", "active", "verified"),
]

# === I. DeFi/DAO (14) ===
i_methods = [
    ("Bitcoin分散決済", "Bitcoin Decentralized Payment", "FIN", "M5", 2009, 9999, "Satoshi Nakamoto", "Bitcoin protocol", "GLOBAL", "https://bitcoin.org/en/bitcoin-paper", "P2P電子決済でSWIFT国際送金($10-50)の95%削減、信頼コストゼロ化", "active", "verified"),
    ("Ethereumスマートコントラクト", "Ethereum Smart Contracts", "FIN", "M5", 2015, 9999, "Vitalik Buterin", "Ethereum Foundation", "GLOBAL", "https://ethereum.org/whitepaper/", "プログラム可能ブロックチェーン。弁護士・エスクロー・清算機関を自動化排除", "active", "verified"),
    ("Uniswap AMM", "Uniswap Automated Market Maker", "FIN", "M6", 2018, 9999, "Hayden Adams", "Uniswap Labs", "USA", "https://blog.uniswap.org/what-is-an-automated-market-maker", "x*y=k数式で自動相場形成。ディーラー人件費排除、0.3%固定手数料", "active", "verified"),
    ("Layer 2ロールアップ", "Layer 2 Rollups (Arbitrum/Optimism/Polygon)", "FIN", "M2", 2021, 9999, "Arbitrum/Optimism/Polygon", "Offchain Labs/Optimism/Polygon", "USA", "https://l2fees.info/", "複数取引をオフチェーン圧縮。ガス代90-95%削減、マイクロトランザクション可能化", "active", "verified"),
    ("DAO分散自律組織", "Decentralized Autonomous Organization", "FIN", "M5", 2016, 9999, "Slock.it (The DAO)", "Aragon/Slock.it", "GLOBAL", "https://en.wikipedia.org/wiki/Decentralized_autonomous_organization", "スマコン投票でCFO・取締役・監査人を排除。管理人件費・法務・監査費削減", "active", "requires_review"),
    ("ステーブルコイン(USDC/Tether/DAI)", "Stablecoins", "FIN", "M5", 2014, 9999, "Tether/Circle/MakerDAO", "Tether/Circle/MakerDAO", "USA", "https://www.circle.com/en/usdc", "FX変動を排除したオンチェーン法定通貨。FXスプレッド1-3%→0.1%以下", "active", "verified"),
    ("Ripple国際送金(XRP)", "Ripple Cross-Border Payments", "FIN", "M5", 2012, 9999, "David Schwartz et al.", "Ripple Labs", "USA", "https://www.exp.science/education/what-is-ripple-challenging-banks-with-blockchain-payments-infrastructure", "Interledger Protocol+XRP。手数料$0.0002でSWIFT($10-50)の1/50,000、3-5秒決済", "active", "verified"),
    ("Stellar途上国送金", "Stellar Cross-Border Payments", "FIN", "M5", 2014, 9999, "Jed McCaleb", "Stellar Foundation", "USA", "https://stellar.org/learn/cross-border-payments", "オープンソース・非営利。SWIFT比手数料99%削減、貧困層送金コスト(GDP6-8%)を1%未満", "active", "verified"),
    ("EU PSD2オープンバンキング", "EU PSD2 Open Banking", "FIN", "M5", 2018, 9999, "European Commission", "ECB/EBA", "EU", "https://www.ecb.europa.eu/press/intro/mip-online/2018/html/1803_revisedpsd.en.html", "統一API仕様で銀行サイロ解除。FinTech直接アクセス、接続構築・保守30-50%削減", "active", "verified"),
    ("PlaidオープンファイナンスAPI", "Plaid Open Finance API", "FIN", "M5", 2013, 9999, "Zach Perret/William Hockey", "Plaid", "USA", "https://plaid.com/resources/open-finance/open-banking-api/", "8,000+ FinTechアプリが12,000+金融機関アクセス。冗長APIコールを1回圧縮", "active", "verified"),
    ("CBDC デジタル人民元", "Digital Yuan (DCEP)", "FIN", "M5", 2020, 9999, "PBOC", "People's Bank of China", "CHN", "https://inca.digital/intelligence/china-cbdc/", "深圳等パイロット$300M/400万トランザクション。二層構造で銀行互換性保持+追跡効率", "active", "verified"),
    ("ロボアドバイザー", "Robo-Advisors (Betterment/Wealthfront)", "FIN", "M6", 2010, 9999, "Dan Egan/Adam Nash", "Betterment/Wealthfront", "USA", "https://www.nerdwallet.com/investing/reviews/betterment", "ソフトウェア自動ポートフォリオ。人間アドバイザー(0.75-1.5%)→0.25%、75%削減", "active", "verified"),
    ("Mambuクラウドコアバンキング", "Mambu Cloud Core Banking", "FIN", "M5", 2011, 9999, "Eugene Danilkis", "Mambu", "DEU", "https://mambu.com/en", "COBOLレガシー代替のクラウドネイティブSaaS。ライセンス・保守50%削減、開発6-12mo→2-4w", "active", "verified"),
    ("ECBデジタルユーロ", "ECB Digital Euro", "FIN", "M5", 2021, 9999, "ECB Governing Council", "ECB", "EU", "https://www.ecb.eu/euro/digital_euro/progress/html/index.en.html", "ユーロ圏CBDC。系統別カスタマイズ($4-6B)→標準実装($1.3B)、決済手数料50%+削減", "active", "verified"),
]

# === J. Space exploration (15) ===
j_methods = [
    ("Falcon 9再使用ブースター", "SpaceX Falcon 9 Reusable Booster", "ENG", "M2", 2015, 9999, "Elon Musk/SpaceX", "SpaceX", "USA", "https://spacenews.com/spacex-booster-reusability-cuts-falcon-9-launch-cost/", "海上回収・着陸でブースター10-30フライト再使用。$/kg LEO 10,000→2,700(73%減)", "active", "verified"),
    ("CubeSat規格化", "CubeSat Standard", "ENG", "M5", 1999, 9999, "Puig-Suari/Twiggs", "Cal Poly/Stanford", "USA", "https://www.cubesat.org/about", "10cm立方体1U基本単位。従来$100M衛星→$200-300K(1/500)", "mature", "verified"),
    ("SpaceX Rideshare共同打ち上げ", "SpaceX Transporter Rideshare", "SCM", "M5", 2021, 9999, "SpaceX", "SpaceX", "USA", "https://www.spacex.com/rideshare", "複数小型衛星をFalcon 9で共同輸送。$/kg 25,000→6,000(75-90%削減)", "active", "verified"),
    ("Relativity 3D印刷ロケット", "Relativity Space 3D Printed Rocket", "ENG", "M6", 2023, 9999, "Tim Ellis", "Relativity Space", "USA", "https://www.relativityspace.com/technology", "85%メタル3D印刷。部品10万→1,000(99%削減)、製造期間18-24mo→3-6mo目標", "active", "verified"),
    ("OneWeb Airbus衛星量産", "OneWeb Airbus Mass Production", "HW", "M2", 2019, 9999, "OneWeb/Airbus JV", "Airbus OneWeb Satellites", "USA", "https://airbusus.com/small-satellite-manufacturing/", "1日2機ペースで衛星量産。従来比90-95%コスト削減、4年で700機出荷", "active", "verified"),
    ("軌道上サービスMEV", "Mission Extension Vehicle (MEV-1)", "ENG", "M5", 2020, 9999, "Northrop Grumman", "Space Logistics LLC", "USA", "https://www.northropgrumman.com/what-we-do/space/satellite-services-in-space/", "軌道上ドッキングで衛星5年延寿命。新規購入($200-400M)→サービス($50-100M)で50-75%削減", "active", "verified"),
    ("NASA Commercial Crew Program", "NASA Commercial Crew Program", "SCM", "M5", 2014, 9999, "NASA HEOMD", "NASA/SpaceX/Boeing", "USA", "https://www.nasa.gov/commercial-crew-program/", "マイルストーン支払いでSpaceX Crew Dragon $55-72M/座席(Shuttle $100M+から40-55%減)", "active", "verified"),
    ("Starship反復試験開発", "SpaceX Starship Iterative Development", "ENG", "M6", 2018, 9999, "Elon Musk", "SpaceX", "USA", "https://www.spacex.com/starship/", "失敗データからAI支援設計最適化反復。打ち上げコスト目標$2-3M、ペイロード100-150t", "active", "requires_review"),
    ("NASA COTS商業貨物", "NASA Commercial Orbital Transportation Services", "SCM", "M5", 2012, 9999, "NASA", "NASA/SpaceX/Orbital", "USA", "https://www.nasa.gov/commercial-resupply-services/", "Dragon/Cygnus貨物輸送。Shuttle($10K-数万/kg)→Dragon($2-3K/kg)で75-90%削減", "active", "verified"),
    ("ISS軌道上3D製造", "Made In Space ISS 3D Printing", "ENG", "M6", 2014, 9999, "Made In Space", "Made In Space", "USA", "https://issnationallab.org/upward/the-new-gold-rush-3d-printing-in-micro-g/", "ISS微重力環境で3Dプリント。衛星修理部品打ち上げコスト60-80%削減", "active", "verified"),
    ("Blue Moon再利用月面着陸機", "Blue Origin Blue Moon Lander", "ENG", "M5", 2019, 9999, "Jeff Bezos", "Blue Origin", "USA", "https://www.blueorigin.com/blue-moon/", "再利用設計+燃料補給で複数ミッション対応。NASA HLS契約$579M", "active", "requires_review"),
    ("衛星自動軌道回避AI", "Starlink Auto Collision Avoidance", "AUTO", "M6", 2023, 9999, "SpaceX", "SpaceX", "USA", "https://www.space.com/spacex-starlink-collision-avoidance", "AI/MLで衝突リスク自動計算・回避。秒単位実行、燃料5-10%削減", "active", "verified"),
    ("Software-Defined衛星(Spire)", "Software-Defined Satellites (Spire Global)", "HW", "M5", 2012, 9999, "Spire Global", "Spire Global", "USA", "https://spire.com/space-services/constellation-management-platform/", "SDR搭載でソフト更新による機能変更。AIS/RDS/GNSS-Rを同一HW実装", "active", "verified"),
    ("衛星地上管制AI自動化", "Constellation Operations AI Automation", "AUTO", "M6", 2020, 9999, "Planet/Spire/SpaceX", "Planet Labs", "USA", "https://www.planet.com/business/", "300+衛星を50-100名で運用(従来1-2機で10-20名)。運用コスト75-90%削減", "active", "verified"),
    ("月火星ISRU現地資源活用", "In-Situ Resource Utilization (ISRU)", "ENG", "M5", 2020, 9999, "NASA Artemis", "NASA/JAXA/ESA", "USA", "https://www.nasa.gov/artemis/", "月面水・火星CO2から燃料・酸素生成。月面1kg輸送$100K+→$1K-10Kへ90%削減", "active", "requires_review"),
]

# === K. Education (10) ===
k_methods = [
    ("MOOC大規模公開講座", "MOOC (Coursera/edX/Khan Academy)", "EDU", "M5", 2008, 9999, "Salman Khan/Andrew Ng/Anant Agarwal", "Khan Academy/Coursera/edX", "USA", "https://blog.khanacademy.org/multiple-studies-show-khan-academy-drives-learning-gains-evidence-for-our-platforms-effectiveness/", "年間学習コスト従来の1/50-1/30($39/year vs $2000)、Coursera/edX修了率30%", "active", "verified"),
    ("Open Educational Resources(OpenStax)", "Open Educational Resources", "EDU", "M5", 2012, 9999, "Richard Baraniuk", "Rice University/OpenStax", "USA", "https://news.rice.edu/news/2025/openstax-surpasses-3b-student-savings-grows-beyond-textbooks", "教科書無料化。4330万学生で累計$3.4B削減(年$78/学生)、米大学72%採用", "active", "verified"),
    ("AI適応学習(Squirrel AI)", "Squirrel AI Adaptive Learning", "EDU", "M6", 2014, 9999, "Derek Li", "Squirrel AI", "CHN", "https://www.technologyreview.com/2019/08/02/131198/china-squirrel-has-started-a-grand-experiment-in-ai-education-it-could-reshape-how-the-world-learns/", "個別AI家庭教師。1ヶ月で習得率56→89%、年間$200-400/生徒(個別講師$2000+比1/5-1/10)", "active", "verified"),
    ("BloomTech ISA再教育", "BloomTech ISA Bootcamp", "EDU", "M5", 2017, 2024, "Austen Allred", "BloomTech (旧Lambda School)", "USA", "https://www.fullstackeconomics.com/p/a-famous-coding-bootcamp-is-changing-its-financing-options", "$30,000+給与14%×48mo(max$40K)、4年制大学$50K比75%削減のISAモデル", "declining", "requires_review"),
    ("Mastery Learning習熟度別", "Mastery Learning", "EDU", "M3", 1968, 9999, "Benjamin Bloom", "U.Chicago", "USA", "https://www.researchforteachers.org.uk/sites/default/files/Docs/Bloom%20(1968)%20Learning%20for%20Mastery_0.pdf", "全生徒が基準到達まで再学習。教材開発コスト償却、効果量0.59", "mature", "verified"),
    ("Khanmigo生成AI家庭教師", "Khanmigo Generative AI Tutor", "EDU", "M6", 2023, 9999, "Sal Khan", "Khan Academy", "USA", "https://www.khanmigo.ai/", "GPT-4駆動ソクラテス対話。学区向け$35/学生/年(従来$60から41%減)、24/7対応", "active", "verified"),
    ("VR没入型研修(STRIVR)", "Walmart STRIVR VR Training", "EDU", "M6", 2017, 9999, "Walmart/STRIVR", "Walmart/STRIVR", "USA", "https://www.strivr.com/customers/walmart", "従来集約型人事研修8h→VR 15分(96%短縮)、評価スコア10-15%上昇", "active", "verified"),
    ("LinkedIn Learning企業学習", "LinkedIn Learning Corporate", "EDU", "M5", 2017, 9999, "LinkedIn/Microsoft", "LinkedIn Learning", "USA", "https://learning.linkedin.com/compare-plans", "従来外部研修$300-1000/人→$32/人/月。企業全体40-60%削減、Fortune 100大半が導入", "active", "verified"),
    ("Duolingoゲーミフィケーション学習", "Duolingo Gamification", "EDU", "M6", 2011, 9999, "Luis von Ahn", "Duolingo", "USA", "https://blog.duolingo.com/results-duolingo-efficacy-studies/", "日常15分で大学5学期相当の言語習得。完全無料モデルで講師人件費50-70%削減", "active", "verified"),
    ("Google Career Certificates", "Google Career Certificates", "EDU", "M5", 2020, 9999, "Google", "Google", "USA", "https://ihatecollege.com/blog/google-career-certificates-worth-it", "3-6ヶ月$300×複数で取得可能。4年学位($40-60K)比1/100以下、150企業認定", "active", "verified"),
]

# === L. Shipping/Aviation (12) ===
l_methods = [
    ("Yield Management収益管理", "Yield Management (Airlines)", "LOG", "M6", 1985, 9999, "Robert Crandall", "American Airlines", "USA", "https://www.hbs.edu/leadership/20th-century-leaders/details?profile=robert_l_crandall", "SABRE需要予測+動的価格連動。同一便で多層価格、American Airlines利益40%成長", "mature", "verified"),
    ("Slow Steaming低速航行", "Slow Steaming Strategy", "LOG", "M2", 2007, 9999, "Maersk", "Maersk Line", "DNK", "https://www.rivieramm.com/news-content-hub/news-content-hub/slow-down-and-count-the-savings-41683", "巡航速度18-20→14-16ノット。燃料消費30-40%削減、CO2 50%減", "active", "verified"),
    ("Mega-Ship大型化(Triple-E)", "Mega-Ship Economies of Scale (Triple-E)", "LOG", "M2", 2013, 9999, "Maersk", "Maersk/Daewoo", "DNK", "https://www.greencarcongress.com/2011/02/maersk-20110221.html", "20K TEU超大型コンテナ船。単位輸送コスト30%減、燃料$333→$218/TEU(35%減)", "active", "verified"),
    ("Fuel Hedging燃料先物", "Airline Fuel Hedging (Southwest)", "LOG", "M5", 1994, 2020, "Gary Kelly", "Southwest Airlines", "USA", "https://southwest50.com/our-stories/the-southwest-jet-fuel-hedge-strategy/", "ジェット燃料先物の6mo-複年購入。1998-2008累計$3.5B節減、競合比25-40%低廉", "legacy", "verified"),
    ("航空機燃料効率(787/737MAX)", "Aircraft Fuel Efficiency (CFRP/LEAP)", "LOG", "M4", 2011, 9999, "Boeing/Airbus/CFM", "Boeing/Airbus/CFM Intl.", "USA", "https://simpleflying.com/why-boeing-787-misunderstood/", "CFRP複合材50%+CFM LEAPで燃料15-25%削減、787は20-25%減実証", "active", "verified"),
    ("船舶共有アライアンス(VSA)", "Vessel-Sharing Alliances (2M/Ocean)", "LOG", "M5", 2015, 9999, "Maersk/MSC/CMA CGM", "2M Alliance/Ocean Alliance", "DNK/FRA", "https://www.flexport.com/blog/ocean-alliances-everything-you-need-to-know/", "複数キャリアが船団統一運用。東西貿易容量率77-96%、投資負担1/3-1/2減", "active", "verified"),
    ("Hub-and-Spoke進化", "Hub-and-Spoke Network Evolution", "LOG", "M5", 1975, 9999, "Delta/United/Emirates", "Delta Air Lines", "USA", "https://www.myticketstoindia.com/blog/major-delta-airlines-hubs/", "Atlanta/ORD/EWR/DXBグローバルハブ。ルート数1/3-1/2、燃料・労働20-30%削減", "active", "verified"),
    ("Code-Sharing Alliances", "Code-Sharing Airline Alliances", "LOG", "M5", 1997, 9999, "Star/Oneworld/SkyTeam", "Star Alliance/Oneworld/SkyTeam", "GLOBAL", "https://www.liligo.co.uk/travel-magazine/airline-alliances-star-alliance-sky-team-and-oneworld", "複数キャリアが同便にコード付与。営業費・CRS・ラウンジ共有で15-25%削減", "active", "verified"),
    ("FAA NextGen/EU SES", "FAA NextGen & Single European Sky", "LOG", "M6", 2007, 9999, "FAA/EU Commission", "FAA/SESAR", "USA", "https://www.transportation.gov/testimony/benefits-next-generation-air-transportation-system", "衛星航法+動的経路でデータ通信。2030年までに28億ガロン燃料削減見込み", "active", "verified"),
    ("Container Port自動化", "Container Port Terminal Automation", "LOG", "M1", 2015, 9999, "PSA/APMT/Shanghai Port", "PSA Singapore/Maersk", "SGP/NLD/CHN", "https://www.dnv.com/services/maritime-digital-transformation-strategy/", "5G遠隔操作で人件費30-50%減、ターンアラウンドタイム40%改善、処理能力40M TEU/y", "active", "verified"),
    ("自動運航電動船(Yara Birkeland)", "Autonomous Electric Cargo (Yara Birkeland)", "LOG", "M6", 2021, 9999, "Yara International", "Yara/DNV", "NOR", "https://www.yara.com/knowledge-grows/game-changer-for-the-environment/", "120TEU完全電動・自動運航。ディーゼル牽引4万往復/年削減、排出ゼロ", "active", "requires_review"),
    ("デジタルツイン船舶最適化", "Digital Twin Vessel Optimization", "LOG", "M6", 2018, 9999, "DNV/Maersk Tankers", "DNV/Maersk Tankers", "NOR/DNK", "https://www.dnv.com/expert-story/maritime-impact/Digital-twins-and-sensor-monitoring/", "船舶仮想モデル+リアルタイムセンサー。AI燃料最適化で10%削減、運用費8-15%減", "active", "verified"),
]


def insert_block(records, start_n):
    rows = []
    n = start_n
    for r in records:
        mid = f"CDH-MET-{n:04d}"
        rows.append((mid, *r))
        n += 1
    c.executemany("INSERT INTO methods VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    return rows


next_n = last_n + 1
f_rows = insert_block(f_methods, next_n); next_n += len(f_rows)
g_rows = insert_block(g_methods, next_n); next_n += len(g_rows)
h_rows = insert_block(h_methods, next_n); next_n += len(h_rows)
i_rows = insert_block(i_methods, next_n); next_n += len(i_rows)
j_rows = insert_block(j_methods, next_n); next_n += len(j_rows)
k_rows = insert_block(k_methods, next_n); next_n += len(k_rows)
l_rows = insert_block(l_methods, next_n); next_n += len(l_rows)

total = len(f_rows)+len(g_rows)+len(h_rows)+len(i_rows)+len(j_rows)+len(k_rows)+len(l_rows)
print(f"Inserted: F={len(f_rows)} G={len(g_rows)} H={len(h_rows)} I={len(i_rows)} J={len(j_rows)} K={len(k_rows)} L={len(l_rows)} = {total}")

all_rows = f_rows + g_rows + h_rows + i_rows + j_rows + k_rows + l_rows
name_to_id = {r[1]: r[0] for r in all_rows}

# === Evidence (selected key numbers across all 7 teams) ===
ev_n = c.execute("SELECT evidence_id FROM evidence ORDER BY evidence_id DESC LIMIT 1").fetchone()[0]
ev_n = int(ev_n.split("-")[-1]) + 1
def ev_id():
    global ev_n
    eid = f"CDH-EVD-{ev_n:04d}"
    ev_n += 1
    return eid

evidence = [
    # F. Agriculture
    (ev_id(), name_to_id["可変施肥(VRA)"], "cost_reduction_per_acre_usd", 25.0, "USD/acre", "従来均一施肥", "USDA corn growers", 2020, "https://geopard.tech/blog/variable-rate-application-technology-in-precision-agriculture/"),
    (ev_id(), name_to_id["ドローン農業散布"], "chemical_reduction_pct", 85.0, "%", "地上散布", "DJI Agras global", 2024, "https://ag.dji.com/"),
    (ev_id(), name_to_id["エアロポニック垂直農法"], "water_reduction_pct", 95.0, "%", "露地農業", "AeroFarms", 2017, "https://www.aerofarms.com/this-vertical-farm-uses-95-less-water-and-no-soil/"),
    (ev_id(), name_to_id["Plantix病害虫AI"], "diagnostic_accuracy_pct", 90.0, "%", "ベンチマーク", "Plantix 135M downloads", 2024, "https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/programme/agritech/detecting-and-managing-crop-pests-and-diseases-with-ai-insights-from-plantix/"),
    (ev_id(), name_to_id["自律除草レーザー"], "weed_management_cost_reduction_pct", 80.0, "%", "化学除草", "Carbon Robotics", 2023, "https://carbonrobotics.com/laserweeder"),
    (ev_id(), name_to_id["精密滴灌(Netafim)"], "water_reduction_pct", 50.0, "%", "flood irrigation", "Netafim Spain case", 2020, "https://www.netafimusa.com/agriculture/drip-irrigation/"),
    (ev_id(), name_to_id["IBM Food Trust"], "traceability_time_reduction_pct", 99.97, "%", "従来7日", "Walmart mango trial", 2018, "https://www.ledgerinsights.com/ibm-food-trust-blockchain-cost-food-traceability/"),
    (ev_id(), name_to_id["Apeel食品コーティング"], "shelf_life_extension_ratio", 2.0, "x", "従来保存", "Apeel avocado/citrus", 2019, "https://www.digicomply.com/blog/apeel-sciences-edible-coating-extending-shelf-life-sustainably/"),
    # G. Healthcare
    (ev_id(), name_to_id["テレメディシン"], "cost_reduction_pct", 80.0, "%", "対面医療", "Penn Medicine study", 2025, "https://www.pennmedicine.org/news/study-finds-telemedicine-visits-cost-far-less-than-office-visits"),
    (ev_id(), name_to_id["成果払い・バンドル支払い(BPCI)"], "savings_per_episode_usd", 324.0, "USD", "従来出来高払い", "CMS BPCI evaluation", 2021, "https://www.cms.gov/priorities/innovation/innovation-models/bundled-payments"),
    (ev_id(), name_to_id["遠隔患者監視(RPM)"], "readmission_reduction_pct", 50.0, "%", "ベースライン", "Philips/CHS", 2023, "https://www.nature.com/articles/s41746-024-01182-w"),
    (ev_id(), name_to_id["ジェネリック医薬品法(Hatch-Waxman)"], "annual_savings_usd_B", 467.0, "USD billions", "従来先発薬価", "Generic Pharmaceutical Association", 2024, "https://accessiblemeds.org/resources/press-releases/40-years-hatch-waxman-trillions-savings-patients/"),
    (ev_id(), name_to_id["電子カルテEHR(HITECH)"], "operating_cost_reduction_pct", 9.66, "%", "non-EHR baseline", "AJMC national sample", 2023, "https://www.ajmc.com/view/association-of-electronic-health-records-with-cost-savings-in-a-national-sample"),
    (ev_id(), name_to_id["Virginia Mason Lean Six Sigma"], "capital_savings_usd_M", 11.0, "USD millions", "従来", "Virginia Mason", 2012, "https://www.qimacros.com/lean-six-sigma-articles/vmmc-case-study/"),
    # H. Defense
    (ev_id(), name_to_id["Agile Software Acquisition"], "release_cycle_reduction_pct", 87.0, "%", "419日", "DoD program metric", 2023, "https://aaf.dau.edu/aaf/software/"),
    (ev_id(), name_to_id["3D Printing予備部品(RAPTOR)"], "production_time_reduction_pct", 80.0, "%", "従来製造", "US Army C-130/F-16 props", 2020, "https://www.army.mil/article/217433/3d_printing_technology_enhancing_logistics_for_army"),
    (ev_id(), name_to_id["Performance-Based Logistics(PBL)"], "cost_per_flight_hour_reduction_pct", 50.0, "%", "7年前", "F-35 Lockheed Martin", 2023, "https://breakingdefense.com/2021/09/new-f-35-sustainment-deal-creates-path-to-lockheed-multi-year-pbl-contract/"),
    (ev_id(), name_to_id["Defense Innovation Unit(DIU)"], "acquisition_time_reduction_pct", 75.0, "%", "5-10年", "DIU prototype data", 2023, "https://www.diu.mil/about"),
    # I. DeFi
    (ev_id(), name_to_id["Bitcoin分散決済"], "fee_reduction_pct", 95.0, "%", "SWIFT", "Bitcoin protocol", 2023, "https://bitcoin.org/en/bitcoin-paper"),
    (ev_id(), name_to_id["Ripple国際送金(XRP)"], "fee_reduction_ratio", 50000.0, "x", "SWIFT $10-50 vs $0.0002", "Ripple XRP Ledger", 2023, "https://www.exp.science/education/what-is-ripple-challenging-banks-with-blockchain-payments-infrastructure"),
    (ev_id(), name_to_id["Layer 2ロールアップ"], "gas_cost_reduction_pct", 92.0, "%", "Ethereum mainnet", "Arbitrum L2", 2023, "https://l2fees.info/"),
    (ev_id(), name_to_id["ロボアドバイザー"], "advisory_fee_reduction_pct", 75.0, "%", "人間1.0%", "Betterment 0.25%", 2024, "https://www.nerdwallet.com/investing/reviews/betterment"),
    (ev_id(), name_to_id["Mambuクラウドコアバンキング"], "cost_reduction_pct", 50.0, "%", "COBOLレガシー", "Mambu customers", 2024, "https://mambu.com/en"),
    # J. Space
    (ev_id(), name_to_id["Falcon 9再使用ブースター"], "cost_per_kg_leo_usd", 2700.0, "USD/kg", "2015 $10,000/kg", "SpaceX Falcon 9", 2025, "https://www.nextbigfuture.com/2026/02/spacex-falcon-9-true-cost-to-launch-is-about-300-per-pound-which-is-25-of-selling-price-to-customers.html"),
    (ev_id(), name_to_id["CubeSat規格化"], "cost_reduction_ratio", 500.0, "x", "$100M衛星", "Cal Poly/Stanford", 2020, "https://www.cubesat.org/about"),
    (ev_id(), name_to_id["Relativity 3D印刷ロケット"], "part_count_reduction_pct", 99.0, "%", "従来10万部品", "Terran 1", 2023, "https://www.aerospacedefensereview.com/news/relativity-space-to-3d-print-95-percent-of-terran1-rocket-nwid-200.html"),
    (ev_id(), name_to_id["OneWeb Airbus衛星量産"], "satellite_unit_cost_reduction_pct", 92.0, "%", "従来カスタム", "Airbus OneWeb Satellites", 2020, "https://airbusus.com/small-satellite-manufacturing/"),
    (ev_id(), name_to_id["NASA Commercial Crew Program"], "seat_cost_reduction_pct", 50.0, "%", "Shuttle $100M+", "SpaceX Crew Dragon", 2021, "https://en.wikipedia.org/wiki/Commercial_Crew_Program"),
    # K. Education
    (ev_id(), name_to_id["MOOC大規模公開講座"], "cost_ratio_vs_traditional", 50.0, "x", "従来$2000/year", "Khan Academy/Coursera", 2024, "https://blog.khanacademy.org/multiple-studies-show-khan-academy-drives-learning-gains-evidence-for-our-platforms-effectiveness/"),
    (ev_id(), name_to_id["Open Educational Resources(OpenStax)"], "cumulative_savings_usd_B", 3.4, "USD billions", "従来有償教科書", "OpenStax 4330万学生", 2025, "https://news.rice.edu/news/2025/openstax-surpasses-3b-student-savings-grows-beyond-textbooks"),
    (ev_id(), name_to_id["AI適応学習(Squirrel AI)"], "mastery_rate_increase_pct", 33.0, "pp", "従来56%", "Squirrel AI 1ヶ月", 2019, "https://www.technologyreview.com/2019/08/02/131198/china-squirrel-has-started-a-grand-experiment-in-ai-education-it-could-reshape-how-the-world-learns/"),
    (ev_id(), name_to_id["VR没入型研修(STRIVR)"], "training_time_reduction_pct", 96.0, "%", "従来8h", "Walmart STRIVR", 2018, "https://corporate.walmart.com/news/2018/09/20/how-vr-is-transforming-the-way-we-train-associates/"),
    # L. Shipping
    (ev_id(), name_to_id["Yield Management収益管理"], "profit_growth_pct", 40.0, "%", "Pre-yield mgmt", "American Airlines 1985-90", 1990, "https://www.hbs.edu/leadership/20th-century-leaders/details?profile=robert_l_crandall"),
    (ev_id(), name_to_id["Slow Steaming低速航行"], "fuel_consumption_reduction_pct", 35.0, "%", "18-20 knots", "Maersk Line", 2010, "https://shipandbunker.com/news/world/449879-maersk-line-says-slow-steaming-will-continue-as-we-want-to-be-as-energy-efficient-as-possible"),
    (ev_id(), name_to_id["Mega-Ship大型化(Triple-E)"], "unit_cost_reduction_pct", 30.0, "%", "13,100 TEU", "Maersk Triple-E", 2013, "https://www.marinelink.com/news/container-economies358220"),
    (ev_id(), name_to_id["Fuel Hedging燃料先物"], "total_savings_usd_B", 3.5, "USD billions", "Industry avg", "Southwest Airlines 1998-2008", 2008, "https://auronomics.com/southwest-airlines-jet-fuel-hedge-strategy-a-case-study-in-risk-management/"),
    (ev_id(), name_to_id["航空機燃料効率(787/737MAX)"], "fuel_consumption_reduction_pct", 22.0, "%", "前世代機", "Boeing 787", 2015, "https://simpleflying.com/why-boeing-787-misunderstood/"),
    (ev_id(), name_to_id["Container Port自動化"], "throughput_increase_pct", 40.0, "%", "manual ops", "PSA Singapore Tuas", 2020, "https://www.edb.gov.sg/en/business-insights/insights/singapore-named-top-container-port-under-new-global-benchmark.html"),
    (ev_id(), name_to_id["デジタルツイン船舶最適化"], "fuel_reduction_pct", 10.0, "%", "非最適化運航", "Maersk Tankers", 2022, "https://maersktankers.com/newsroom/maersk-tankers-uses-vessels-digital-twin-to-slash-emissions"),
]
c.executemany("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?)", evidence)
print(f"Evidence added: {len(evidence)}")

# === Genealogy ===
gen_n = c.execute("SELECT rel_id FROM genealogy ORDER BY rel_id DESC LIMIT 1").fetchone()[0]
gen_n = int(gen_n.split("-")[-1]) + 1
def gen_id():
    global gen_n
    rid = f"CDH-REL-{gen_n:04d}"
    gen_n += 1
    return rid

existing = {
    "TPS": "CDH-MET-0010",
    "Lean": "CDH-MET-0017",
    "Container": "CDH-MET-0260",
    "Wright": "CDH-MET-0005",
    "Hub": "CDH-MET-0262",  # FedEx hub-and-spoke
    "AI_drug": "CDH-MET-0247",  # AI Drug Discovery
}

genealogy_data = [
    # F. Agriculture genealogy
    (gen_id(), name_to_id["精密滴灌(Netafim)"], name_to_id["可変施肥(VRA)"], "inspires", 2000, "ドリップ灌漑のGPS精密化への発展"),
    (gen_id(), name_to_id["可変施肥(VRA)"], name_to_id["AI土壌診断(FarmBeats)"], "integrates", 2017, "VRAデータ+AI予測推定で精密化"),
    (gen_id(), name_to_id["マーカー支援選抜育種(MAS)"], name_to_id["CRISPR-Edited作物"], "supersedes", 2020, "マーカー選抜→直接ゲノム編集"),
    # G. Healthcare genealogy
    (gen_id(), existing["TPS"], name_to_id["Virginia Mason Lean Six Sigma"], "inspires", 2002, "Toyota生産方式の病院適用"),
    (gen_id(), name_to_id["電子カルテEHR(HITECH)"], name_to_id["AI診断支援(IDx-DR)"], "integrates", 2018, "EHRデータ基盤上のAI診断"),
    (gen_id(), existing["AI_drug"], name_to_id["精密医学・ゲノム検査"], "integrates", 2010, "AI創薬と精密医学の補完関係"),
    (gen_id(), name_to_id["Hospital at Home"], name_to_id["テレメディシン"], "integrates", 2020, "在宅急性期治療と遠隔診療の融合"),
    # H. Defense genealogy
    (gen_id(), name_to_id["COTS調達(Perry Memo)"], name_to_id["Defense Innovation Unit(DIU)"], "supersedes", 2015, "COTS思想を民間技術全般に拡張"),
    (gen_id(), name_to_id["Modular Open Systems Approach"], name_to_id["Software Defined Radio(JTRS)"], "derives", 2004, "JTRSの失敗からMOSAへ"),
    # I. DeFi genealogy
    (gen_id(), name_to_id["Bitcoin分散決済"], name_to_id["Ethereumスマートコントラクト"], "supersedes", 2015, "送金プロトコルから汎用計算プラットフォーム"),
    (gen_id(), name_to_id["Ethereumスマートコントラクト"], name_to_id["Uniswap AMM"], "derives", 2018, "スマコン上の自動マーケットメイク"),
    (gen_id(), name_to_id["Ethereumスマートコントラクト"], name_to_id["DAO分散自律組織"], "derives", 2016, "スマコンによる組織ガバナンス"),
    (gen_id(), name_to_id["Ethereumスマートコントラクト"], name_to_id["Layer 2ロールアップ"], "derives", 2021, "Ethereumのスケーラビリティ解決"),
    (gen_id(), name_to_id["Bitcoin分散決済"], "CDH-MET-0413", "inspires", 2014, "Bitcoin思想がCBDC設計に影響"),
    # J. Space genealogy
    (gen_id(), existing["Wright"], name_to_id["Falcon 9再使用ブースター"], "derives", 2015, "Wright学習曲線の宇宙打ち上げ実証"),
    (gen_id(), name_to_id["Falcon 9再使用ブースター"], name_to_id["Starship反復試験開発"], "supersedes", 2018, "部分再使用→完全再使用"),
    (gen_id(), name_to_id["CubeSat規格化"], name_to_id["SpaceX Rideshare共同打ち上げ"], "integrates", 2021, "小型衛星共同輸送の標準化"),
    (gen_id(), name_to_id["NASA COTS商業貨物"], name_to_id["NASA Commercial Crew Program"], "supersedes", 2014, "貨物から有人へ商業化拡張"),
    # K. Education genealogy
    (gen_id(), name_to_id["Mastery Learning習熟度別"], name_to_id["AI適応学習(Squirrel AI)"], "integrates", 2014, "Bloomの習熟理論+AI個別化"),
    (gen_id(), name_to_id["AI適応学習(Squirrel AI)"], name_to_id["Khanmigo生成AI家庭教師"], "supersedes", 2023, "適応学習→生成AI対話"),
    (gen_id(), name_to_id["MOOC大規模公開講座"], name_to_id["Google Career Certificates"], "derives", 2020, "MOOC基盤上の職能認定"),
    # L. Shipping genealogy
    (gen_id(), existing["Container"], name_to_id["Mega-Ship大型化(Triple-E)"], "derives", 2013, "コンテナ化の大型化進化"),
    (gen_id(), existing["Hub"], name_to_id["Hub-and-Spoke進化"], "supersedes", 1990, "FedExモデルのグローバル拡張"),
    (gen_id(), name_to_id["Hub-and-Spoke進化"], name_to_id["Code-Sharing Alliances"], "integrates", 1997, "ハブ統合の航空連合化"),
    (gen_id(), name_to_id["Yield Management収益管理"], name_to_id["FAA NextGen/EU SES"], "inspires", 2007, "需要管理から空域管理最適化"),
]
c.executemany("INSERT INTO genealogy VALUES (?,?,?,?,?,?)", genealogy_data)
print(f"Genealogy added: {len(genealogy_data)}")

# === Critiques ===
crt_n = c.execute("SELECT critique_id FROM critiques ORDER BY critique_id DESC LIMIT 1").fetchone()[0]
crt_n = int(crt_n.split("-")[-1]) + 1
def crt_id():
    global crt_n
    cid = f"CDH-CRT-{crt_n:04d}"
    crt_n += 1
    return cid

critiques = [
    (crt_id(), name_to_id["薬剤給付管理(PBM)"], "FTC Staff Report", 2024, "spread_pricing_concerns", "PBM spread pricing で透明性欠如、独立薬局支払い不公正", "https://www.ftc.gov/system/files/ftc_gov/pdf/pharmacy-benefit-managers-staff-report.pdf"),
    (crt_id(), name_to_id["BloomTech ISA再教育"], "Career Karma analysts", 2024, "outcome_decline", "BloomTech初期91%就職率から公表停止。市場飽和とニーズ乖離", "https://careerkarma.com/schools/bloomtech/"),
    (crt_id(), name_to_id["DAO分散自律組織"], "The DAO Hack 2016", 2016, "smart_contract_vulnerability", "The DAOで$70Mのスマコン脆弱性によるハック、ETH ハードフォーク必要に", "https://en.wikipedia.org/wiki/Decentralized_autonomous_organization"),
    (crt_id(), name_to_id["Starship反復試験開発"], "Space industry analysts", 2024, "schedule_optimism", "Musk経済予測$2-3M/打ち上げに業界懐疑、IFT試験7回中軌道未達多数", "https://www.space.com/spacex-starship-flight-passenger-cost-elon-musk.html"),
    (crt_id(), name_to_id["AI診断支援(IDx-DR)"], "Medical regulators", 2024, "bias_and_validation", "AI診断のバイアス・人種差・施設外汎化性能未確立。FDAは継続的監視要求", "https://www.retina-specialist.com/article/ai-for-dr-screening-where-are-we-in-2025"),
    (crt_id(), name_to_id["MOOC大規模公開講座"], "Education researchers", 2020, "completion_rate_plateau", "MOOC修了率30%停滞が15年継続。スケーリングは量に効くが質に限界", "https://www.encoura.org/resources/wake-up-call/the-big-three-platforms-revisited-the-latest-on-coursera-edx-udemy/"),
]
c.executemany("INSERT INTO critiques VALUES (?,?,?,?,?,?,?)", critiques)
print(f"Critiques added: {len(critiques)}")

conn.commit()

m_count = c.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
e_count = c.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
g_count = c.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0]
cr_count = c.execute("SELECT COUNT(*) FROM critiques").fetchone()[0]
d_count = c.execute("SELECT COUNT(*) FROM domains").fetchone()[0]
print(f"\nFinal: methods={m_count} evidence={e_count} genealogy={g_count} critiques={cr_count} domains={d_count}")

conn.close()
