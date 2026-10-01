import os
import re
import html
import pandas as pd
import streamlit as st

DATA_EXCEL = "Companies hiring data related roles.xlsx"
DATA_PARQUET = "processed_companies.parquet"

def extract_clean_domain(url: str) -> str:
    if not url or pd.isna(url):
        return ""
    url = str(url).strip().lower()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url.split("/")[0].split("?")[0].split(":")[0]

def extract_tld(domain: str) -> str:
    if not domain or pd.isna(domain):
        return "N/A"
    parts = str(domain).split(".")
    if len(parts) > 1:
        ext = "." + parts[-1].lower()
        if len(ext) <= 10 and not ext[-1].isdigit():
            return ext
    return ".other"

def extract_linkedin_handle(url: str) -> str:
    if not url or pd.isna(url):
        return ""
    m = re.search(r"linkedin\.com/company/([^/?#]+)", str(url), re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""

def clean_brand_from_domain_or_handle(domain: str, handle: str) -> str:
    domain_clean = str(domain).lower().replace("www.", "").strip()
    handle_clean = str(handle).strip()
    
    if handle_clean and handle_clean.lower() not in ["", "unknown", "none", "recruit", "careers", "entrance-book", "company"]:
        clean = handle_clean.replace("-", " ").replace("_", " ")
        clean = re.sub(r"\b(inc|ltd|corp|co|llc|gmbh|pvt)\b", "", clean, flags=re.IGNORECASE)
        clean = re.sub(r"\s+", " ", clean).strip()
        if len(clean) >= 2:
            return clean.title()
            
    if domain_clean and domain_clean.lower() not in ["", "unknown", "none"]:
        root = domain_clean.split("/")[0].split("?")[0].split(":")[0]
        parts = root.split(".")
        main_part = parts[0]
        if main_part in ["corp", "careers", "recruit", "docs", "info", "jp", "api", "app", "portal", "residence", "corporate", "foil"] and len(parts) > 2:
            main_part = parts[1]
        clean = main_part.replace("-", " ").replace("_", " ")
        return clean.title()
        
    return "Unknown Company"

def clean_company_name(name: str, domain: str = "", li_handle: str = "") -> str:
    if not name or pd.isna(name):
        name = ""
    
    name = str(name).strip()
    domain_clean = str(domain).lower().replace("www.", "").strip()
    handle_clean = str(li_handle).strip()
    
    # Unescape HTML entities
    name = html.unescape(name)
    
    # 1. Clean Markdown syntax artifacts (e.g. ![badge](url), ## Header, **bold**, etc.)
    name = re.sub(r"^!\[(.*?)\](?:\(.*?\))?", r"\1", name)
    name = re.sub(r"^\[(.*?)\](?:\(.*?\))?", r"\1", name)
    name = re.sub(r"^!\[", "", name)
    name = re.sub(r"^[#*_\-`~+=/\\|>@]+\s*", "", name)
    name = re.sub(r"\s*[#*_\-`~+=/\\|<]+$", "", name)
    
    # 2. Known specific brand overrides
    if "felix" in name.lower() or "flix pago" in name.lower() or "felixpago" in domain_clean:
        return "Félix Pago"
    if "zaz" in name.lower() and ("os" in name.lower() or "zazos" in domain_clean):
        return "Zazos"
    if "eursap" in name.lower():
        return "Eursap - Europe's #1 SAP Recruitment Agency"
    if "mocomoco" in domain_clean or "ai moco voice" in name.lower():
        return "Moco Voice"
    if "yumenosora" in domain_clean or "虎" in name or "toranoana" in name.lower():
        return "Toranoana Lab (虎の穴ラボ)"
    if "syoya.com" in domain_clean or "笑屋" in name:
        return "Syoya (笑屋株式会社)"
    if "nikkei.co.jp" in domain_clean or "日本経済" in name:
        return "Nikkei (日本経済新聞社)"
    if "as-child.com" in domain_clean or "エース" in name:
        return "As-Child (エースチャイルド)"
    if "theport.jp" in domain_clean or "port" in domain_clean:
        return "Port Inc. (ポート株式会社)"
    if "remoterocketship" in domain_clean or "rocketship" in name.lower():
        return "Remote Rocketship"
    if "fig.io" in domain_clean or "fig" in handle_clean.lower():
        return "Fig"
    if "untitled" in domain_clean or "untitled" in name.lower():
        return "Untitled"
    if "olelohonua.com" in domain_clean or "olelo" in name.lower():
        return "Olelo Honua"
    if "angstrom-ai" in domain_clean or "ngstr" in name.lower():
        return "Angstrom AI"
    if "u-wave.net" in domain_clean or ("wave" in name.lower() and "u-wave" in domain_clean):
        return "U-Wave"
    if "oebb" in domain_clean:
        return "ÖBB"
        
    # 3. Known Scraper junk / generic domains mapping
    scraper_domain_map = {
        "wantedly.com": "Wantedly",
        "prtimes.jp": "PR TIMES",
        "hrmos.co": "HRMOS",
        "zenn.dev": "Zenn",
        "theport.jp": "Port Inc.",
        "careerpark.jp": "CareerPark",
        "syukatsu-kaigi.jp": "Syukatsu Kaigi",
        "nikki.ne.jp": "Minshu",
        "techbookfest.org": "TechBookFest",
        "hamee.co.jp": "Hamee",
        "portal.socialdog.jp": "SocialDog",
        "socialdog.jp": "SocialDog",
        "rakko.inc": "Rakko",
        "rakkokeyword.com": "Rakko Keyword",
        "rakkoma.com": "Rakko M&A",
        "rakko.tools": "Rakko Tools",
        "speakerdeck.com": "Speaker Deck",
        "snowplowanalytics.com": "Snowplow Analytics",
        "jsdelivr.net": "jsDelivr",
        "appveyor.com": "AppVeyor",
        "drone.io": "Drone CI",
        "shields.io": "Shields.io",
        "creativecommons.org": "Creative Commons",
        "netlify.com": "Netlify",
        "bestpractices.dev": "OpenSSF Best Practices",
        "securityscorecards.dev": "OpenSSF Scorecard",
        "trackawesomelist.com": "TrackAwesomeList",
        "firstleads.net": "FirstLeads",
        "tryandai.com": "AndAI",
        "nvolume.com": "NVolume",
        "trunktools.com": "Trunk Tools",
        "rippling.com": "Govly",
        "dotwave.ai": "DotWave",
        "play0ad.com": "0 A.D.",
        "8am.com": "8am",
        "herp.careers": "HERP Careers",
        "recruit.fenrir-inc.com": "Fenrir Inc.",
        "fenrir-inc.com": "Fenrir Inc.",
        "itmedia.co.jp": "ITmedia",
        "recruit-mp.co.jp": "Recruit Marketing Partners",
        "auctions.yahoo.co.jp": "Yahoo! Auctions",
        "ai-monitoring.shaperon-inc.com": "Shaperon AI Monitoring",
        "bodoge.hoobby.net": "Bodoge",
        "info.spacely.co.jp": "Spacely",
        "spacely.co.jp": "Spacely",
        "street-academy.com": "Street Academy",
        "residence.xincere.jp": "Xincere Residence",
        "xincere.jp": "Xincere",
        "cybozu.co.jp": "Cybozu",
        "crowdworks.jp": "CrowdWorks",
        "kaminashi.jp": "Kaminashi",
        "leaner.co.jp": "Leaner Technologies",
        "greff.co.jp": "Greff",
        "kickflow.com": "Kickflow",
        "canary-app.jp": "Canary",
        "irsc.jp": "Inner Resource",
        "asobica.co.jp": "Asobica",
        "ap-com.co.jp": "AP Communications",
        "enechange.co.jp": "ENECHANGE",
        "qubena.com": "Compass (Qubena)",
        "raccoon.ne.jp": "Raccoon Holdings",
        "timetreeapp.com": "TimeTree",
        "mntsq.co.jp": "MNTSQ",
        "unext.co.jp": "U-NEXT",
        "layerx.co.jp": "LayerX",
        "bakuraku.jp": "Bakuraku (LayerX)",
        "in-g.jp": "Ing Co.",
        "smilesurvey.jp": "Smile Survey",
        "hoobby.net": "Hoobby",
        "spacemarket.co.jp": "Spacemarket",
        "lazuli.ninja": "Lazuli",
        "enito.co.jp": "Enito Group (Omiai)",
        "bringout.biz": "BringOut",
        "quo-digital.jp": "QUO Card",
        "kaonavi.jp": "Kaonavi",
        "eustylelab.co.jp": "Eustyle Lab",
        "tsukulink.co.jp": "Tsukulink",
        "aeon-st.co.jp": "AEON Smart Technology",
        "aeon.com": "AEON",
        "hacomono.jp": "Hacomono",
        "hello.ai": "Hello AI",
        "trustbank.co.jp": "Trust Bank",
        "furusato-tax.jp": "Furusato Choice",
        "publitech.fun": "LoGo Chat (Publitech)",
        "japan-d2.com": "Japan Digital Design",
        "uzumaki-inc.jp": "Uzumaki",
        "timee.co.jp": "Timee",
        "yamaneco.co.jp": "Yamaneco",
        "openlogi.com": "OpenLogi",
        "mi-6.co.jp": "MI-6",
        "smartround.com": "Smartround",
        "wamazing.com": "WAmazing",
        "creditengine.jp": "Credit Engine",
        "sios.jp": "SIOS Technology",
        "pepabo.com": "GMO Pepabo",
        "photoruction.com": "Photoruction",
        "crevo.jp": "Crevo",
        "graat.co.jp": "GRA&T",
        "joyz.co.jp": "Joyz",
        "paiza.jp": "Paiza",
        "eventhub.jp": "EventHub",
        "bizer.jp": "Bizer",
        "cureapp.co.jp": "CureApp",
        "everyleaf.com": "Everyleaf",
        "tam-bourine.co.jp": "Tambourine",
        "ntt.com": "NTT Communications",
        "creationline.com": "Creationline",
        "unscene.jp": "Unscene",
        "autify.com": "Autify",
        "cluster.mu": "Cluster",
        "mobilefactory.jp": "Mobile Factory",
        "pin-japan.com": "PIN Japan",
        "oisixradaichi.co.jp": "Oisix ra daichi",
        "uzabase.com": "Uzabase",
        "esm.co.jp": "Eiwa System Management",
        "serverworks.co.jp": "Serverworks",
        "codmon.com": "Codmon",
        "correc.co.jp": "Correc",
        "globis.co.jp": "Globis",
        "studist.jp": "Studist",
        "springboard.co.jp": "Springboard",
        "3-shake.com": "3-shake",
        "shaperon-inc.com": "Shaperon",
        "yumemi.co.jp": "Yumemi",
        "mobalab.net": "Mobalab",
    }

    for d_key, brand in scraper_domain_map.items():
        if d_key in domain_clean:
            return brand

    # 4. If name has corrupted mojibake bytes or hex escape sequences
    if "_x00" in name or any(s in name for s in ["æ", "ã", "å", "ç", "è", "é", "ì", "ð", "Ã", "Â"]):
        brand = clean_brand_from_domain_or_handle(domain_clean, handle_clean)
        if brand and brand != "Unknown Company":
            return brand

    # 5. Remove Trademark & Registered Symbols: ®, ™, ©, ℠, etc.
    name = re.sub(r"[®™©℠]", "", name)
    
    # 6. Remove all Emojis and graphic symbols:
    name = re.sub(r"[\U00010000-\U0010ffff]", "", name)
    name = re.sub(r"[\u2600-\u27ff]", "", name)
    name = re.sub(r"[\u25a0-\u25ff]", "", name)
    name = re.sub(r"[\u2300-\u23ff]", "", name)
    name = re.sub(r"[\u2460-\u24ff\u2b50-\u2b55]", "", name)
    name = re.sub(r"[\u2500-\u257f]", "", name)
    name = re.sub(r"[•·§¶†‡\u00a0\u00ad\ufffd]", " ", name)
    
    # 7. Standardize quotes and dashes
    name = name.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    name = name.replace("–", "-").replace("—", "-")
    
    # 8. Clean up any invalid control characters
    name = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", name)
    
    # 9. Normalize whitespace
    name = re.sub(r"\s+", " ", name).strip()
    
    # 10. Clean leading/trailing punctuation left behind after symbol removal
    name = re.sub(r"^[,\-\s/\\|#*!:;\[\]()<>]+", "", name)
    name = re.sub(r"[,\-\s/\\|#*!:;\[\]()<>]+$", "", name)
    
    # 11. Fallback if empty or purely non-alphanumeric
    if not name or name.lower() in ["", "unknown", "nan", "none", "null"] or not re.search(r"\w", name):
        name = clean_brand_from_domain_or_handle(domain_clean, handle_clean)
            
    return name.strip()

def classify_industry(name: str, domain: str, handle: str, tld: str) -> str:
    text = f"{name} {domain} {handle}".lower()
    tld = tld.lower()
    
    if tld == ".ai" or re.search(r"\b(ai|ml|gpt|bot|robot|deep|vision|neural|cognit|synthet|intelligence|autonomous|llm|genai|vector|agentic)\b", text):
        return "Artificial Intelligence & ML"
    elif re.search(r"\b(data|analytics|insight|metric|lake|warehouse|pipeline|bi|query|snowflake|databricks|dbt|etl|bigdata)\b", text):
        return "Data & Analytics Infra"
    elif tld in [".finance", ".crypto"] or re.search(r"\b(fin|pay|bank|capital|fund|crypto|coin|invest|wealth|lend|credit|insur|finance|trading|defi|blockchain|wallet|fintech)\b", text):
        return "FinTech & Capital"
    elif re.search(r"\b(health|med|bio|care|pharma|clinic|therap|genom|doctor|cure|life sciences|diagnostics|telehealth|biotech)\b", text):
        return "HealthTech & Bio"
    elif re.search(r"\b(staff|recruit|talent|hire|career|hr|job|headhunt|workforce|staffing|placement|recruiting|hiring)\b", text):
        return "Staffing & Talent Solutions"
    elif tld in [".dev", ".app"] or re.search(r"\b(cloud|sec|cyber|guard|shield|auth|devops|infra|scale|host|server|network|security|kubernetes|docker|saas)\b", text):
        return "Cloud, DevOps & CyberSec"
    elif re.search(r"\b(shop|store|cart|retail|market|commerce|brand|goods|d2c|ecommerce|marketplace)\b", text):
        return "E-Commerce & Retail"
    elif re.search(r"\b(edu|learn|academy|school|tutor|course|campus|study|edtech|student|training)\b", text):
        return "EdTech & Learning"
    elif re.search(r"\b(game|play|media|studio|entertain|film|music|sound|vr|ar|stream|creator|video)\b", text):
        return "Media, Gaming & Creative"
    elif re.search(r"\b(consult|group|partner|advis|solution|solutions|agency|lab|labs|venture|associates|global|services|technologies|systems|enterprises)\b", text):
        return "Enterprise & Consulting"
    else:
        return "Software & Emerging Tech"

def detect_tags(name: str, tld: str) -> str:
    name_l = str(name).lower()
    tld_l = str(tld).lower()
    tags = []
    if "yc " in name_l or "(yc" in name_l or "y combinator" in name_l or "w21" in name_l or "s21" in name_l or "w22" in name_l or "s22" in name_l:
        tags.append("🚀 YC Backed")
    if "stealth" in name_l:
        tags.append("🕶️ Stealth")
    if "techstars" in name_l:
        tags.append("⭐ Techstars")
    if "500 global" in name_l or "500 startups" in name_l:
        tags.append("🌐 500 Startups")
    if tld_l == ".ai":
        tags.append("🤖 AI Native")
    elif tld_l in [".io", ".dev"]:
        tags.append("💻 Dev Native")
    elif tld_l in [".xyz", ".finance"]:
        tags.append("⚡ Web3/Fin")
    
    return ", ".join(tags) if tags else "General"

@st.cache_data(show_spinner=False)
def load_and_enrich_data() -> pd.DataFrame:
    # Check if pre-processed parquet cache exists and is fresh
    if os.path.exists(DATA_PARQUET):
        try:
            df = pd.read_parquet(DATA_PARQUET)
            if "Company_Name" in df.columns and "Industry" in df.columns:
                return df
        except Exception:
            pass

    if not os.path.exists(DATA_EXCEL):
        raise FileNotFoundError(f"Could not find dataset at {DATA_EXCEL}")

    raw_df = pd.read_excel(DATA_EXCEL)

    # Build clean dataframe
    name_col = raw_df["Name"] if "Name" in raw_df.columns else raw_df.iloc[:, 0]
    web_col = raw_df["Website"] if "Website" in raw_df.columns else raw_df.iloc[:, 1]
    li_col = raw_df["LinkedIn URL"] if "LinkedIn URL" in raw_df.columns else raw_df.iloc[:, 2]
    loc_col = raw_df["Unnamed: 3"] if "Unnamed: 3" in raw_df.columns else (raw_df.iloc[:, 3] if raw_df.shape[1] > 3 else pd.Series([""] * len(raw_df)))

    df = pd.DataFrame()
    df["Website"] = web_col.fillna("").astype(str).str.strip()
    df["LinkedIn_URL"] = li_col.fillna("").astype(str).str.strip()
    df["Location"] = loc_col.fillna("Global / Remote").astype(str).str.strip()
    df["Location"] = df["Location"].replace({"nan": "Global / Remote", "": "Global / Remote", "None": "Global / Remote"})

    # Extract Domains & TLDs
    df["Domain"] = df["Website"].apply(extract_clean_domain)
    df["TLD"] = df["Domain"].apply(extract_tld)
    df["LinkedIn_Handle"] = df["LinkedIn_URL"].apply(extract_linkedin_handle)

    # Clean Company Name thoroughly (removing emojis, mojibake, trademark symbols, escapes, markdown prefixes)
    raw_names = name_col.fillna("").astype(str).str.strip()
    df["Company_Name"] = [
        clean_company_name(n, d, h)
        for n, d, h in zip(raw_names, df["Domain"], df["LinkedIn_Handle"])
    ]

    # Industry classification
    df["Industry"] = [
        classify_industry(n, d, h, t)
        for n, d, h, t in zip(df["Company_Name"], df["Domain"], df["LinkedIn_Handle"], df["TLD"])
    ]

    # Tags
    df["Tags"] = [
        detect_tags(n, t)
        for n, t in zip(df["Company_Name"], df["TLD"])
    ]

    # Name Length & First Letter
    df["Name_Length"] = df["Company_Name"].str.len().astype(int)
    df["First_Letter"] = df["Company_Name"].apply(
        lambda n: n[0].upper() if n and n[0].isalpha() else "#"
    )

    # Ensure all string columns are object/str
    for col in ["Company_Name", "Website", "LinkedIn_URL", "Location", "Domain", "TLD", "LinkedIn_Handle", "Industry", "Tags", "First_Letter"]:
        df[col] = df[col].astype(str)

    # Save to parquet for ultra fast subsequent loads
    try:
        df.to_parquet(DATA_PARQUET, index=False)
    except Exception as e:
        print(f"Warning: Could not save parquet: {e}")

    return df
