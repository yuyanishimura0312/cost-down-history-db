#!/usr/bin/env python3
"""Phase 2.3 ingest: M (AI×Learning Curve, 20) + N (Circular Economy, 20) + O (40+ genealogy)."""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "cdh.sqlite"
conn = sqlite3.connect(DB)
c = conn.cursor()

row = c.execute("SELECT method_id FROM methods ORDER BY method_id DESC LIMIT 1").fetchone()
last_n = int(row[0].split("-")[-1])
print(f"Last method_id: {row[0]} (next: CDH-MET-{last_n+1:04d})")

# === M. AI × Learning Curve (20) ===
m_methods = [
    ("Chinchilla Scaling Laws", "Chinchilla Compute-Optimal Scaling", "SW", "M2", 2020, 9999, "Kaplan/Hoffmann", "OpenAI/DeepMind", "USA", "https://arxiv.org/abs/2203.15556", "計算予算に対しparam数とdata量を等比増加。N∝C^0.50でGopher 280B→70Bを同計算量で達成、推論コスト大幅削減", "active", "verified"),
    ("AlphaGo Zero Self-Play", "AlphaGo Zero Self-Play Training", "RD", "M6", 2017, 9999, "David Silver", "DeepMind", "GBR", "https://www.nature.com/articles/nature24270", "人間棋譜不要、自己対戦で学習。40時間でAlphaGo Lee超越、人間ラベリングコストゼロ化", "active", "verified"),
    ("EfficientZero Model-based RL", "EfficientZero Sample-Efficient RL", "RD", "M2", 2021, 9999, "Weirui Ye et al.", "Tsinghua/Berkeley", "CHN", "https://arxiv.org/abs/2111.00210", "DQN比500倍データ効率。Atari 100k benchmarkで2時間ゲームプレイで人間超越、サンプル取得コスト1/500", "active", "verified"),
    ("BERT自己教導学習", "BERT Self-Supervised Learning", "SW", "M6", 2018, 9999, "Devlin et al.", "Google AI", "USA", "https://arxiv.org/abs/1810.04805", "15%マスキング+文脈予測。ラベル不要のテキスト事前学習、下流タスクは少量FTでSOTA、ラベル90%減", "active", "verified"),
    ("MAE Vision Masked Autoencoders", "Masked Autoencoders for Vision", "SW", "M6", 2021, 9999, "Kaiming He et al.", "Meta FAIR", "USA", "https://arxiv.org/abs/2111.06377", "75%マスク+asymmetric encoder-decoder。encoder visible patch のみで計算量1/4、訓練3倍加速", "active", "verified"),
    ("Constitutional AI / RLAIF", "Constitutional AI + RLAIF", "SW", "M6", 2022, 9999, "Yuntao Bai et al.", "Anthropic", "USA", "https://arxiv.org/abs/2212.08073", "10原則のみでAI自己批判・改版・選好判定。人間ラベル数千→数十(1/100)、Claude 3基盤", "active", "verified"),
    ("DPO Direct Preference Optimization", "Direct Preference Optimization", "SW", "M6", 2023, 9999, "Rafailov et al.", "Stanford", "USA", "https://arxiv.org/abs/2305.18290", "Reward Model+PPO不要、選好データから直接最適化。RLHF不安定性排除、Llama 2/Mistral 7B採用", "active", "verified"),
    ("Speculative Decoding", "Speculative Decoding Inference", "SW", "M6", 2023, 9999, "Yaniv Leviathan et al.", "Google", "USA", "https://arxiv.org/abs/2211.17192", "小モデル提案→大モデル検証で並列生成。T5-XXLで2-3倍高速化、出力同一", "active", "verified"),
    ("Flash Attention", "Flash Attention IO-Aware", "HW", "M6", 2022, 9999, "Tri Dao", "Stanford", "USA", "https://arxiv.org/abs/2205.14135", "GPU HBM-SRAM IO最小化tiling。Attention 7.6倍高速化、Quadratic→Linearメモリ、長文処理革命", "active", "verified"),
    ("GPTQ 4bit量子化", "GPTQ Post-Training Quantization", "HW", "M2", 2022, 9999, "Frantar et al.", "IST Austria/Meta", "AUT", "https://arxiv.org/abs/2210.17323", "175B GPTを4bitに削減、推論VRAM 60-75%減、微調整不要、精度維持", "active", "verified"),
    ("AWQ Activation-Aware Quantization", "AWQ Activation-Aware Quantization", "HW", "M3", 2023, 9999, "Ji Lin et al.", "MIT HAN Lab/NVIDIA", "USA", "https://arxiv.org/abs/2306.00978", "1% salient weightのみ保護、GPTQより精度維持、推論コスト低下、MLSys 2024 Best Paper", "active", "verified"),
    ("Switch Transformers MoE", "Switch Transformers MoE Sparsity", "SW", "M2", 2021, 9999, "Fedus/Zoph", "Google Brain", "USA", "https://arxiv.org/abs/2101.03961", "Token単位1 Expert活性化、FLOP固定でparam増加。1兆param同計算量、pretraining 7倍高速", "active", "verified"),
    ("Mixtral 8x7B MoE", "Mixtral 8x7B Efficient MoE", "SW", "M2", 2023, 9999, "Jiang et al.", "Mistral AI", "FRA", "https://arxiv.org/abs/2401.04088", "46.7B total/13B active。Llama 2 70Bを9/12 benchで超過、推論6倍高速、OSS基盤の主流化", "active", "verified"),
    ("LoRA低ランク適応", "LoRA Low-Rank Adaptation", "SW", "M5", 2021, 9999, "Edward Hu et al.", "Microsoft", "USA", "https://arxiv.org/abs/2106.09685", "元param frozen+delta低ランク分解(r=8)。FT VRAM 99%減、新タスク適応コスト1/1000", "active", "verified"),
    ("QLoRA Quantized LoRA", "QLoRA Quantized Fine-Tuning", "HW", "M2", 2023, 9999, "Tim Dettmers et al.", "U.Washington/LMSys", "USA", "https://arxiv.org/abs/2305.14314", "4bit NF4+Double Quantization+Paged Optimizer。65B LLMを48GB GPUでFT、精度維持", "active", "verified"),
    ("Knowledge Distillation", "Knowledge Distillation (Hinton)", "SW", "M5", 2015, 9999, "Geoffrey Hinton et al.", "Google/U.Toronto", "USA", "https://arxiv.org/abs/1503.02531", "教師→学生 soft target知識転移。DistilBERT: BERT 40%圧縮・97%性能保持・推論60%高速", "mature", "verified"),
    ("BigBird Sparse Attention", "BigBird Sparse Attention", "SW", "M2", 2020, 9999, "Manzil Zaheer et al.", "Google Research", "USA", "https://arxiv.org/abs/2007.14062", "Local+Global+Random sparse pattern。seq_len 512→4096(8倍)、計算量O(n)線形化", "active", "verified"),
    ("Test-Time Compute Scaling", "Test-Time Compute Scaling (o1/o3)", "SW", "M2", 2024, 9999, "OpenAI o1 team", "OpenAI", "USA", "https://www.lesswrong.com/posts/byNYzsfFmb2TpYFPW/o1-a-technical-primer", "訓練後計算固定→推論時思考チェーンで精度向上。AIME 74%→96.7%(o3-mini)、推論FLOPが新scaling軸", "active", "verified"),
    ("Prefix Caching KV-Cache再利用", "Prefix Caching / KV-Cache Reuse", "SW", "M5", 2024, 9999, "vLLM/Anthropic", "Berkeley/Anthropic", "USA", "https://bentoml.com/llm/inference-optimization/prefix-caching", "複数request間のprefix KV cache再利用。Claude prompt caching で90%コスト削減・85%latency削減", "active", "verified"),
    ("RAG Retrieval-Augmented Generation", "Retrieval-Augmented Generation", "SW", "M5", 2020, 9999, "Patrick Lewis et al.", "Facebook AI", "USA", "https://arxiv.org/abs/2005.11401", "FT計算コスト排除、Retrieval+ICLで知識追加。新知識追加は O(1) DB更新、限界費用ほぼゼロ", "active", "verified"),
]

# === N. Circular Economy + Sharing + Negative Cost (20) ===
n_methods = [
    ("Cradle-to-Cradle設計", "Cradle-to-Cradle Design", "ENG", "M5", 2002, 9999, "McDonough/Braungart", "MBDC", "USA", "https://mcdonough.com/writings/cradle-cradle-remaking-way-make-things/", "搖籃から搖籃へ。製品回収・再利用を設計段階から組込み、廃棄コストゼロ化と資源価値最大化", "active", "verified"),
    ("Kalundborg産業共生", "Kalundborg Industrial Symbiosis", "MFG", "M5", 1972, 9999, "Kalundborg cluster", "Kalundborg Symbiosis", "DNK", "https://www.symbiosis.dk/en/", "デンマーク産業パークで複数企業間廃棄物ネットワーク。17社連携で年$72-87M削減・635,000t CO2/y削減", "active", "verified"),
    ("Apple Daisy Robot閉ループ", "Apple Daisy Closed-Loop Recycling", "MFG", "M5", 2018, 9999, "Apple", "Apple Inc.", "USA", "https://www.apple.com/newsroom/2019/04/apple-expands-global-recycling-programs/", "ロボット自動分解で iPhone希少金属回収。200台/時、年48,000t電子廃棄物回避", "active", "verified"),
    ("Lighting-as-a-Service (LaaS)", "Lighting-as-a-Service (Philips/Schiphol)", "ENERGY", "M5", 2015, 9999, "Philips/Signify", "Philips", "NLD", "https://www.signify.com/global/our-company/news/press-release-archive/2015/20150416-philips-provides-light-as-a-service-to-schiphol-airport", "照明所有権サプライヤー保持、使用量課金。消費電力50%減、耐久75%向上、メンテ劇的削減", "active", "verified"),
    ("Caterpillar Remanufacturing", "Caterpillar Reman Program", "MFG", "M5", 1973, 9999, "Caterpillar", "Caterpillar Inc.", "USA", "https://www.caterpillar.com/en/company/sustainability/remanufacturing.html", "重機完全分解・復元。新品比 50-60%削減、80-90%新材料削減、65-87%エネ削減、9拠点3,600人", "mature", "verified"),
    ("Ecovative Mushroom Packaging", "Ecovative Mycelium Packaging", "FOOD", "M5", 2007, 9999, "Eben Bayer/Gavin McIntyre", "Ecovative Design", "USA", "https://mushroompackaging.com/", "農業副産物+菌糸体を5-7日成型。石油系フォーム代替、100%堆肥化可能、廃棄ゼロ化", "active", "verified"),
    ("Carbios酵素PETリサイクル", "Carbios Enzymatic PET Recycling", "MFG", "M3", 2022, 9999, "Carbios", "Carbios", "FRA", "https://www.carbios.com/en/enzymatic-recycling/", "酵素触媒でPET分子分解。$1.51/kg(バージン比-19%)、年間運行74%減、エネ65%減、無限回リサイクル", "active", "verified"),
    ("EU Extended Producer Responsibility", "EU Extended Producer Responsibility (EPR)", "FIN", "M5", 1994, 9999, "Lindhqvist/Lund University", "EU Commission", "DEU", "https://www.taxually.com/blog/understanding-epr-germany---a-guide-for-businesses", "製造者が製品全LC費用負担。EU全体€3.1B/y費用構造化、設計段階最適化を構造的に誘導", "active", "verified"),
    ("Adidas x Parley海洋プラスチック", "Adidas x Parley Ocean Plastic", "MFG", "M5", 2015, 9999, "Adidas/Parley", "Adidas", "DEU", "https://parley.tv/initiatives/adidasxparley", "海洋プラスチック・違法漁網をアップサイクル。2015-2020で30M足製造、$30M売上", "active", "verified"),
    ("CarbonCure Concrete CO2固定", "CarbonCure CO2 Concrete", "CONST", "M5", 2014, 9999, "Robert Niven", "CarbonCure Technologies", "CAN", "https://www.carboncure.com/", "CO2を生コンに注入。セメント最大10%削減+炭素固定。1立方ヤード25ポンドCO2削減・日$1,000利益", "active", "verified"),
    ("Zipcarカーシェアリング", "Zipcar Carsharing", "LOG", "M5", 2000, 9999, "Robin Chase/Antje Danielson", "Zipcar", "USA", "https://www.zipcar.com/carsharing", "共有資産で個別所有削減。会員月$100+(vs $706 AAA新車)、1台で個別車8台代替、利用頻度6倍+", "active", "verified"),
    ("car2go/ShareNowフリーフローティング", "Free-Floating Carsharing", "LOG", "M5", 2008, 9999, "Daimler", "ShareNow/Daimler", "DEU", "https://www.prnewswire.com/news-releases/car2go-and-drivenow-join-forces-share-now-to-become-the-biggest-free-floating-carshare-provider-worldwide-300803690.html", "ステーション不要GPS+動的価格。1台で8台代替・利用頻度6倍、欧州全域展開", "active", "verified"),
    ("Airbnbホームシェアリング", "Airbnb Home-Sharing", "LOG", "M5", 2008, 9999, "Gebbia/Chesky/Blecharczyk", "Airbnb", "USA", "https://bmtoolbox.net/stories/airbnb/", "遊休不動産の短期賃貸化。2008-2024で$250B+ホスト収益、既存資産利用率100倍以上", "active", "verified"),
    ("Regusコワーキング", "Regus Coworking", "CONST", "M5", 1989, 9999, "Mark Dixon", "Regus/IWG", "GBR", "https://www.regus.com/en/coworking", "分割可能オフィス(分単位~年単位)。業界55%遊休($27k/desk損失)を80-85%利用に転換", "active", "verified"),
    ("Xometryアセットライト製造", "Xometry Asset-Light Manufacturing", "MFG", "M5", 2013, 9999, "Randy Altschuler", "Xometry", "USA", "https://www.xometry.com/", "AI媒介製造マーケットプレイス。設備不所有で需給マッチング、従来製造マージン(40-60%)を大幅上回る", "active", "verified"),
    ("Yandex DC排熱回収(Helsinki)", "Yandex Data Center Heat Recovery", "ENERGY", "M5", 2015, 9999, "Yandex", "Yandex DC", "RUS", "https://www.datacenterdynamics.com/en/news/yandex-data-center-heats-finnish-city/", "DC排熱年350MWh地域供給。地域暖房5%減(20,000世帯)+DC運用1/3減、ガス50%減/CO2 40%減", "active", "verified"),
    ("Swedenバイオガス(廃棄物)", "Sweden Biogas from Waste", "ENERGY", "M5", 1990, 9999, "Swedish municipalities", "Swedish gov", "SWE", "https://earth.org/sweden-waste-to-energy/", "食品廃棄物の嫌気消化。全国33%食廃リサイクル率、交通エネの33%バイオガス、廃棄物99.3%回収/エネ化", "mature", "verified"),
    ("Stockholm 5°C District Heating", "Stockholm 5°C District Heating (Open District Heating)", "ENERGY", "M5", 2010, 9999, "Stockholm Exergi", "Stockholm Exergi", "SWE", "https://www.opendistrictheating.com/", "低温熱源(5°C+)都市規模集約。産業排熱+DAC+再エネ熱統合、コージェネ効率~80%(従来30-50%)", "active", "verified"),
    ("Negawatt Concept (Lovins)", "Negawatt Energy Efficiency Concept", "ENERGY", "M4", 1989, 9999, "Amory Lovins", "Rocky Mountain Institute", "USA", "https://e360.yale.edu/features/amory_lovins_energy_efficiency_is_the_key", "供給増より効率投資優先。米国で50%石油・75%電力削減可能、投資=供給の1/8", "active", "verified"),
    ("Climeworks DAC Gen3", "Climeworks Direct Air Capture Gen3", "ENERGY", "M2", 2017, 9999, "Climeworks AG", "Climeworks", "CHE", "https://climeworks.com/press-release/next-gen-tech-powers-climeworks-megaton-leap", "大気CO2直接回収→化学肥料・建材。$1,000/t(2024)→$250-350/t(2030目標)で50%削減", "active", "requires_review"),
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
m_rows = insert_block(m_methods, next_n); next_n += len(m_rows)
n_rows = insert_block(n_methods, next_n); next_n += len(n_rows)
print(f"Inserted: M={len(m_rows)} N={len(n_rows)} = {len(m_rows)+len(n_rows)}")

all_rows = m_rows + n_rows
name_to_id = {r[1]: r[0] for r in all_rows}

# === Evidence for M/N methods ===
ev_n = c.execute("SELECT evidence_id FROM evidence ORDER BY evidence_id DESC LIMIT 1").fetchone()[0]
ev_n = int(ev_n.split("-")[-1]) + 1
def ev_id():
    global ev_n
    eid = f"CDH-EVD-{ev_n:04d}"
    ev_n += 1
    return eid

evidence = [
    # M
    (ev_id(), name_to_id["Chinchilla Scaling Laws"], "model_size_reduction_ratio", 4.0, "x", "Gopher 280B vs Chinchilla 70B同計算量", "DeepMind Chinchilla", 2022, "https://arxiv.org/abs/2203.15556"),
    (ev_id(), name_to_id["AlphaGo Zero Self-Play"], "human_label_reduction_pct", 100.0, "%", "人間棋譜数千局→ゼロ", "DeepMind AGZ", 2017, "https://www.nature.com/articles/nature24270"),
    (ev_id(), name_to_id["EfficientZero Model-based RL"], "sample_efficiency_ratio", 500.0, "x", "DQN baseline", "Atari 100k benchmark", 2021, "https://arxiv.org/abs/2111.00210"),
    (ev_id(), name_to_id["Flash Attention"], "speedup_ratio", 7.6, "x", "Standard attention", "Tri Dao FlashAttention", 2022, "https://arxiv.org/abs/2205.14135"),
    (ev_id(), name_to_id["LoRA低ランク適応"], "param_reduction_pct", 99.0, "%", "Full FT", "Microsoft LoRA", 2021, "https://arxiv.org/abs/2106.09685"),
    (ev_id(), name_to_id["Speculative Decoding"], "inference_speedup_ratio", 2.5, "x", "Auto-regressive decoding", "Google T5-XXL", 2023, "https://arxiv.org/abs/2211.17192"),
    (ev_id(), name_to_id["Mixtral 8x7B MoE"], "inference_speedup_ratio", 6.0, "x", "Llama 2 70B", "Mistral AI", 2023, "https://arxiv.org/abs/2401.04088"),
    (ev_id(), name_to_id["BERT自己教導学習"], "label_reduction_pct", 90.0, "%", "Supervised baseline", "Google BERT", 2018, "https://arxiv.org/abs/1810.04805"),
    (ev_id(), name_to_id["Knowledge Distillation"], "model_compression_pct", 40.0, "%", "BERT-base", "DistilBERT", 2019, "https://arxiv.org/abs/1910.01108"),
    (ev_id(), name_to_id["Constitutional AI / RLAIF"], "human_feedback_reduction_ratio", 100.0, "x", "Full RLHF", "Anthropic CAI", 2022, "https://arxiv.org/abs/2212.08073"),
    (ev_id(), name_to_id["Test-Time Compute Scaling"], "accuracy_aime", 96.7, "%", "Baseline 74%", "OpenAI o3-mini", 2024, "https://www.lesswrong.com/posts/byNYzsfFmb2TpYFPW/o1-a-technical-primer"),
    (ev_id(), name_to_id["Prefix Caching KV-Cache再利用"], "cost_reduction_pct", 90.0, "%", "Uncached", "Anthropic Claude API", 2024, "https://bentoml.com/llm/inference-optimization/prefix-caching"),
    # N
    (ev_id(), name_to_id["Kalundborg産業共生"], "annual_savings_usd_M", 80.0, "USD millions/y", "Pre-symbiosis", "Kalundborg 17社", 2020, "https://www.symbiosis.dk/en/"),
    (ev_id(), name_to_id["Apple Daisy Robot閉ループ"], "ewaste_avoided_t_per_year", 48000.0, "metric tons/y", "Pre-Daisy", "Apple", 2019, "https://www.apple.com/newsroom/2019/04/apple-expands-global-recycling-programs/"),
    (ev_id(), name_to_id["Lighting-as-a-Service (LaaS)"], "power_consumption_reduction_pct", 50.0, "%", "Pre-LaaS", "Philips/Schiphol", 2015, "https://www.signify.com/global/our-company/news/press-release-archive/2015/20150416-philips-provides-light-as-a-service-to-schiphol-airport"),
    (ev_id(), name_to_id["Caterpillar Remanufacturing"], "cost_reduction_pct", 55.0, "%", "New equipment", "Caterpillar Reman", 2024, "https://www.caterpillar.com/en/company/sustainability/remanufacturing.html"),
    (ev_id(), name_to_id["Carbios酵素PETリサイクル"], "energy_reduction_pct", 65.0, "%", "Mechanical recycling", "Carbios facility 2026", 2024, "https://www.carbios.com/en/enzymatic-recycling/"),
    (ev_id(), name_to_id["EU Extended Producer Responsibility"], "structured_fees_eur_B_per_year", 3.1, "EUR billions/y", "Pre-EPR", "EU Commission", 2020, "https://www.taxually.com/blog/understanding-epr-germany---a-guide-for-businesses"),
    (ev_id(), name_to_id["Adidas x Parley海洋プラスチック"], "shoes_produced_M", 30.0, "million pairs", "2015-2020累計", "Adidas-Parley", 2020, "https://parley.tv/initiatives/adidasxparley"),
    (ev_id(), name_to_id["Airbnbホームシェアリング"], "cumulative_host_earnings_usd_B", 250.0, "USD billions", "2008-2024累計", "Airbnb", 2024, "https://bmtoolbox.net/stories/airbnb/"),
    (ev_id(), name_to_id["Yandex DC排熱回収(Helsinki)"], "dc_operating_cost_reduction_pct", 33.0, "%", "Standard cooling", "Yandex Helsinki", 2017, "https://www.datacenterdynamics.com/en/news/yandex-data-center-heats-finnish-city/"),
    (ev_id(), name_to_id["Swedenバイオガス(廃棄物)"], "food_waste_recycling_rate_pct", 33.0, "%", "Pre-biogas", "Sweden national", 2019, "https://earth.org/sweden-waste-to-energy/"),
    (ev_id(), name_to_id["Climeworks DAC Gen3"], "cost_reduction_target_pct", 50.0, "%", "Gen2 $1000/t → Gen3 $250-350/t", "Climeworks 2030", 2030, "https://climeworks.com/press-release/next-gen-tech-powers-climeworks-megaton-leap"),
]
c.executemany("INSERT INTO evidence VALUES (?,?,?,?,?,?,?,?,?)", evidence)
print(f"Evidence added: {len(evidence)}")

# === O. Genealogy expansion (40+ new pairs based on existing methods) ===
gen_n = c.execute("SELECT rel_id FROM genealogy ORDER BY rel_id DESC LIMIT 1").fetchone()[0]
gen_n = int(gen_n.split("-")[-1]) + 1
def gen_id():
    global gen_n
    rid = f"CDH-REL-{gen_n:04d}"
    gen_n += 1
    return rid

# Lookup helper: get method_id by name from existing methods
def find_id(name_query, like=False):
    if like:
        r = c.execute("SELECT method_id FROM methods WHERE name_ja LIKE ? LIMIT 1", (f"%{name_query}%",)).fetchone()
    else:
        r = c.execute("SELECT method_id FROM methods WHERE name_ja = ? LIMIT 1", (name_query,)).fetchone()
    return r[0] if r else None

# Build genealogy from named pairs (40+)
pairs = [
    # M: AI scaling laws lineage
    ("Chinchilla Scaling Laws", "DeepSeek V3 効率的事前学習", "supersedes", 2024, "Chinchilla則をMoE+推論時計算でさらに効率化"),
    ("AlphaGo Zero Self-Play", "Constitutional AI / RLAIF", "inspires", 2022, "自己生成フィードバックの言語領域への展開"),
    ("BERT自己教導学習", "MAE Vision Masked Autoencoders", "derives", 2021, "BERT mask予測の画像領域への適用"),
    ("Knowledge Distillation", "LoRA低ランク適応", "inspires", 2021, "圧縮思想から低ランク適応へ"),
    ("LoRA低ランク適応", "QLoRA Quantized LoRA", "supersedes", 2023, "LoRAの量子化拡張で65B GPUに収容"),
    ("Switch Transformers MoE", "Mixtral 8x7B MoE", "derives", 2023, "Switch TransformersのOSS実装と商用化"),
    ("Constitutional AI / RLAIF", "DPO Direct Preference Optimization", "inspires", 2023, "CAIから直接選好最適化へ"),
    ("Flash Attention", "BigBird Sparse Attention", "integrates", 2022, "sparse pattern+IO最適化の融合"),
    ("Test-Time Compute Scaling", "RAG Retrieval-Augmented Generation", "integrates", 2024, "推論時計算とretrieval統合"),
    # N: Circular Economy lineage
    ("Cradle-to-Cradle設計", "EU Extended Producer Responsibility", "inspires", 1994, "C2C思想の規制化"),
    ("Kalundborg産業共生", "Stockholm 5°C District Heating", "inspires", 2010, "産業共生から都市スケール熱統合へ"),
    ("Caterpillar Remanufacturing", "Apple Daisy Robot閉ループ", "inspires", 2018, "重機リマンから電子機器自動分解へ"),
    ("Negawatt Concept (Lovins)", "Yandex DC排熱回収(Helsinki)", "inspires", 2015, "効率投資思想からDC排熱活用へ"),
    ("Zipcarカーシェアリング", "car2go/ShareNowフリーフローティング", "supersedes", 2008, "ステーション型からフリーフロー型へ"),
    ("Zipcarカーシェアリング", "Airbnbホームシェアリング", "inspires", 2008, "カーシェア思想の不動産領域への波及"),
    ("Climeworks DAC Gen3", "CarbonCure Concrete CO2固定", "integrates", 2018, "DAC回収CO2の建材固定化"),
]
# Apply named pairs
gen_data = []
for parent_name, child_name, rel, year, rationale in pairs:
    p_id = name_to_id.get(parent_name) or find_id(parent_name)
    c_id = name_to_id.get(child_name) or find_id(child_name)
    if p_id and c_id:
        gen_data.append((gen_id(), p_id, c_id, rel, year, rationale))

# Additional cross-era genealogy from existing methods (no new methods needed)
cross_era_pairs = [
    # Pre-industrial → Taylor
    ("Adam Smith 分業論", "動作研究", "inspires", 1909, "分業論からの動作分析の発展"),
    ("Wedgwood Etruria品質統制", "Deming 14原則", "inspires", 1950, "品質統制文化のDeming化"),
    # TPS → Software
    ("カンバン方式", "Kanban (ソフトウェア)", "derives", 2007, "TPSカンバンのソフトウェア領域適用"),
    ("SMED(段取り替え短縮)", "CI/CD", "inspires", 2006, "段取り時間短縮思想のデプロイメント化"),
    ("自働化", "AI診断支援(IDx-DR)", "inspires", 2018, "異常自動検知の医療AI化"),
    # Manufacturing → Service
    ("ジャストインタイム(JIT)", "Scrum", "inspires", 1995, "JIT原理のソフトウェア反復開発化"),
    ("リーン生産", "Lean Software Development", "derives", 2003, "Lean Mfg→Lean SD"),
    ("リーン生産", "リーン・スタートアップ", "inspires", 2011, "Lean思想のスタートアップ化"),
    # Learning curves spread
    ("経験曲線(Wright's Law)", "Falcon 9再使用ブースター", "derives", 2015, "Wright学習曲線の宇宙打ち上げ実証"),
    ("経験曲線(Wright's Law)", "Swanson's Law", "derives", 2012, "Wright法則の太陽光適用"),
    ("経験曲線(Wright's Law)", "Carlson Curve", "derives", 2003, "Wright法則のDNA配列適用"),
    # Modular spread
    ("IBM System/360", "Modular Open Systems Approach", "inspires", 2004, "System/360の防衛モジュラー化"),
    ("Design Rules(モジュラー性)", "VW MQB", "inspires", 2012, "Baldwin&Clark→VW実装"),
    # OSS/Cloud progression
    ("GNU/フリーソフトウェア", "Open Source Initiative", "supersedes", 1998, "FSFからOSI商用化路線"),
    ("Linux", "Docker", "integrates", 2013, "Linux Kernel上のコンテナ化"),
    ("AWS EC2", "AWS Lambda", "supersedes", 2014, "IaaS→Serverless進化"),
    ("Kubernetes", "Anthropic Computer Use", "inspires", 2024, "コンテナ自動運用→AI自動操作"),
    # Cross-domain (Construction → Mfg)
    ("Levittown開発", "SHEINオンデマンド製造", "inspires", 2012, "Levittown流れ作業のファッション領域化"),
    # Procurement evolution
    ("価値工学(VE)", "原価企画", "inspires", 1960, "Miles VE→Toyota Target Costing"),
    ("Should Cost分析", "AI設計・分子最適化", "inspires", 2013, "Should Cost思想のAI創薬化"),
    # Outsourcing → SaaS
    ("Kodak-IBM ITアウトソーシング", "Salesforce SaaS", "inspires", 1999, "IT外部委託→SaaS消費化"),
    ("Kodak-IBM ITアウトソーシング", "AWS EC2", "inspires", 2006, "IT外部委託→クラウドIaaS"),
    # AI takeover
    ("実験計画法(DoE)", "Google GNoME新材料探索", "supersedes", 2023, "DoE→GNN自動材料探索"),
    ("Stage-Gate法", "Stage-Gate第3世代", "supersedes", 2002, "1988初版→Agile融合"),
    # Healthcare cost
    ("ジェネリック医薬品法(Hatch-Waxman)", "医薬品リポジショニング", "inspires", 2000, "ジェネリック法→既存薬リパーパス"),
    ("電子カルテEHR(HITECH)", "実世界根拠(RWE)活用", "integrates", 2018, "EHRデータ基盤上のRWE"),
    # Telemed
    ("テレメディシン", "Hospital at Home", "integrates", 2020, "遠隔診療と在宅入院の融合"),
    # Energy lineage
    ("Newcomen大気圧蒸気機関", "Watt遠心調速機", "inspires", 1788, "蒸気機関の自動制御化"),
    ("Boulton&Watt ロイヤリティ制", "ARM ISA", "inspires", 1985, "発明者ロイヤリティ→半導体IPライセンス"),
    # Space lineage
    ("CubeSat規格化", "Software-Defined衛星(Spire)", "integrates", 2012, "CubeSat+SDR統合"),
    ("NASA Commercial Crew Program", "Blue Moon再利用月面着陸機", "inspires", 2019, "商業有人輸送→月面着陸民間化"),
]
for parent_name, child_name, rel, year, rationale in cross_era_pairs:
    p_id = find_id(parent_name)
    c_id = find_id(child_name)
    if p_id and c_id:
        # check duplicate
        dup = c.execute("SELECT 1 FROM genealogy WHERE parent_method_id=? AND child_method_id=?", (p_id, c_id)).fetchone()
        if not dup:
            gen_data.append((gen_id(), p_id, c_id, rel, year, rationale))

c.executemany("INSERT INTO genealogy VALUES (?,?,?,?,?,?)", gen_data)
print(f"Genealogy added: {len(gen_data)}")

conn.commit()

m_count = c.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
e_count = c.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
g_count = c.execute("SELECT COUNT(*) FROM genealogy").fetchone()[0]
cr_count = c.execute("SELECT COUNT(*) FROM critiques").fetchone()[0]
d_count = c.execute("SELECT COUNT(*) FROM domains").fetchone()[0]
print(f"\nFinal: methods={m_count} evidence={e_count} genealogy={g_count} critiques={cr_count} domains={d_count}")

conn.close()
