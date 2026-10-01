import os
import re
import json
import random
import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data_loader import load_and_enrich_data

# Page Configuration
st.set_page_config(
    page_title="DataTalent Radar | 41,000+ Companies Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark CSS Theme Injection
DARK_CSS = """
<style>
    /* Global Fonts and Background */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #111827, #0B0F19 60%, #05070D 100%);
        color: #F1F5F9;
    }
    
    /* Top Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 18px;
        padding: 24px 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .hero-title {
        font-size: 1.95rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #818CF8 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 5px;
        margin-bottom: 0;
    }
    
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #151C2C 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    }
    
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .metric-delta {
        font-size: 0.78rem;
        font-weight: 500;
        color: #38BDF8;
        margin-top: 5px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    /* Custom Company Card */
    .company-card {
        background: #141B2D;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
    }
    
    .company-card:hover {
        border-color: #6366F1;
        background: #172036;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.12);
    }
    
    .company-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    
    .company-meta {
        font-size: 0.82rem;
        color: #94A3B8;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 8px 0;
    }
    
    .tag-badge {
        display: inline-block;
        font-size: 0.72rem;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }
    
    .tag-ai {
        background: rgba(168, 85, 247, 0.15);
        color: #C084FC;
        border-color: rgba(168, 85, 247, 0.3);
    }
    
    .tag-yc {
        background: rgba(249, 115, 22, 0.15);
        color: #FB923C;
        border-color: rgba(249, 115, 22, 0.3);
    }

    /* Modern Table & UI elements */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* CRM Status Card */
    .crm-card {
        background: #151D30;
        border-left: 4px solid #6366F1;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #2A364F;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #435479;
    }
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

# Load Enriched Data
@st.cache_data(show_spinner=False)
def get_dataset():
    return load_and_enrich_data()

with st.spinner("⚡ Loading and caching 41,600+ companies hiring intelligence..."):
    df_raw = get_dataset()

# Initialize CRM Session State
if "crm_tracker" not in st.session_state:
    st.session_state["crm_tracker"] = [
        {
            "id": "1",
            "Company_Name": "Weekday AI (YC W21)",
            "Website": "weekday.works",
            "LinkedIn_URL": "https://www.linkedin.com/company/weekdayworks",
            "Target_Role": "Data Scientist / ML",
            "Status": "Interviewing",
            "Priority": "⭐⭐⭐⭐⭐",
            "Notes": "Connected with recruiter on LinkedIn. Initial technical screen next Tuesday.",
            "Date_Added": "2026-09-28"
        },
        {
            "id": "2",
            "Company_Name": "Jobgether",
            "Website": "jobgether.com",
            "LinkedIn_URL": "https://www.linkedin.com/company/jobgether",
            "Target_Role": "Data Analyst",
            "Status": "Outreach Sent",
            "Priority": "⭐⭐⭐⭐",
            "Notes": "Outreach sent to Head of Data via LinkedIn messaging.",
            "Date_Added": "2026-09-29"
        },
        {
            "id": "3",
            "Company_Name": "Braintrust",
            "Website": "usebraintrust.com",
            "LinkedIn_URL": "https://www.linkedin.com/company/braintrustdata",
            "Target_Role": "Analytics Engineer",
            "Status": "Interested",
            "Priority": "⭐⭐⭐⭐⭐",
            "Notes": "Top Web3 / Talent marketplace with data roles.",
            "Date_Added": "2026-10-01"
        }
    ]

# Roulette History in Session State
if "roulette_history" not in st.session_state:
    st.session_state["roulette_history"] = []

# Sidebar Navigation & Global Filters
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <div style="background: linear-gradient(135deg, #6366F1, #38BDF8); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; color: white;">⚡</div>
            <div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF; line-height: 1.1;">DataTalent</div>
                <div style="font-size: 0.75rem; color: #818CF8; font-weight: 600; letter-spacing: 0.5px;">RADAR v2.5 • DARK EDITION</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        "Navigation",
        [
            "📊 Market Intelligence",
            "🔎 Company Explorer",
            "🎯 Outreach & CRM Tracker",
            "🎲 Discovery Roulette",
            "📈 Deep Analytics"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🎛️ **Quick Ecosystem Filters**")

    all_industries = ["All Industries"] + sorted(df_raw["Industry"].unique().tolist())
    selected_industry = st.selectbox("Industry Focus", all_industries)

    tag_options = ["All Tags", "🚀 YC Backed", "🕶️ Stealth", "⭐ Techstars", "🤖 AI Native", "💻 Dev Native", "⚡ Web3/Fin"]
    selected_tag = st.selectbox("Startup / Innovation Tag", tag_options)

    st.markdown("---")
    
    # Global Filter Pipeline
    filtered_df = df_raw.copy()
    if selected_industry != "All Industries":
        filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
    if selected_tag != "All Tags":
        filtered_df = filtered_df[filtered_df["Tags"].str.contains(selected_tag.split(" ")[0], case=False, na=False)]

    # Sidebar Quick Summary Stats
    st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 14px; margin-top: 10px;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Filtered Companies</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #38BDF8; margin: 4px 0;">{len(filtered_df):,} <span style="font-size: 0.8rem; color: #64748B; font-weight: normal;">/ {len(df_raw):,}</span></div>
            <div style="font-size: 0.75rem; color: #A5B4FC;">Representing {len(filtered_df)/len(df_raw)*100:.1f}% of total database</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.caption("⚡ Live Data Pipeline • 41,633 Data Hiring Companies")

# Hero Header Banner
st.markdown(f"""
    <div class="hero-banner">
        <div>
            <div class="hero-title">Data Hiring Market Intelligence</div>
            <p class="hero-subtitle">Interactive exploration of <strong>{len(df_raw):,}</strong> tech organizations, AI startups, and enterprises hiring data professionals.</p>
        </div>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <span class="badge-pill">⚡ 41,633 Companies</span>
            <span class="badge-pill" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8; border-color: rgba(56, 189, 248, 0.3);">🤖 4,350+ AI Startups</span>
            <span class="badge-pill" style="background: rgba(16, 185, 129, 0.15); color: #34D399; border-color: rgba(16, 185, 129, 0.3);">📊 1,930+ Core Data & BI</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Color Palette for Dark Plots
DARK_PLOT_THEME = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "#E2E8F0", "family": "Plus Jakarta Sans, sans-serif"},
    "margin": dict(l=20, r=20, t=40, b=20),
}
PALETTE = ["#6366F1", "#38BDF8", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6", "#14B8A6", "#F43F5E", "#EAB308", "#06B6D4", "#64748B"]


# ==============================================================================
# TAB 1: MARKET INTELLIGENCE & EXECUTIVE OVERVIEW
# ==============================================================================
if nav_selection == "📊 Market Intelligence":
    # High-level Metrics Row (Replaced Dev & Infra with Core Data & Analytics Focus)
    m1, m2, m3, m4, m5 = st.columns(5)
    
    ai_count = len(df_raw[df_raw["Industry"] == "Artificial Intelligence & ML"])
    core_data_count = len(df_raw[df_raw["Company_Name"].str.contains(r"data|analytics|insight|metric|bi|warehouse|lake|query", case=False, regex=True)])
    yc_count = len(df_raw[df_raw["Tags"].str.contains("YC", na=False)])
    stealth_count = len(df_raw[df_raw["Tags"].str.contains("Stealth", na=False)])
    unique_domains = df_raw["Domain"].nunique()

    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏢 Total Companies</div>
                <div class="metric-value">{len(df_raw):,}</div>
                <div class="metric-delta">✦ 100% verified directory</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🤖 AI & ML Startups</div>
                <div class="metric-value">{ai_count:,}</div>
                <div class="metric-delta">▲ {ai_count/len(df_raw)*100:.1f}% of market</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        # Replaced Dev & Infra KPI Card with Core Data & Analytics Platforms
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Core Data & BI</div>
                <div class="metric-value">{core_data_count:,}</div>
                <div class="metric-delta">▲ Direct data tooling & platforms</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🚀 YC & Accelerators</div>
                <div class="metric-value">{yc_count}</div>
                <div class="metric-delta">★ Backed top-tier startups</div>
            </div>
        """, unsafe_allow_html=True)
    with m5:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🌐 Unique Domains</div>
                <div class="metric-value">{unique_domains:,}</div>
                <div class="metric-delta">◆ Global hiring footprint</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Charts Row 1: Industry Distribution + Hiring Concentration by Sector (Replaced Top Domain Extensions)
    c1, c2 = st.columns([6, 5])
    
    with c1:
        ind_counts = filtered_df["Industry"].value_counts().reset_index()
        ind_counts.columns = ["Industry", "Count"]
        
        fig_ind = px.pie(
            ind_counts,
            names="Industry",
            values="Count",
            hole=0.55,
            color_discrete_sequence=PALETTE,
            title="<b>Industry & Tech Taxonomy Breakdown</b>"
        )
        fig_ind.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
            marker=dict(line=dict(color="#0B0F19", width=2))
        )
        fig_ind.update_layout(
            **DARK_PLOT_THEME,
            legend=dict(orientation="v", x=1.02, y=0.5, font=dict(size=11)),
            annotations=[dict(text=f"<b>{len(filtered_df):,}</b><br>Entities", x=0.5, y=0.5, font_size=15, showarrow=False, font_color="#F8FAFC")]
        )
        st.plotly_chart(fig_ind, use_container_width=True)

    with c2:
        # Replaced Top Domain Extensions chart with Hiring Concentration & Sector Volume
        sector_counts = filtered_df["Industry"].value_counts().reset_index()
        sector_counts.columns = ["Sector", "Companies"]
        sector_counts = sector_counts.sort_values(by="Companies", ascending=True)

        fig_sec = px.bar(
            sector_counts,
            x="Companies",
            y="Sector",
            orientation="h",
            color="Companies",
            color_continuous_scale="Viridis",
            title="<b>Hiring Volume & Sector Concentration</b>",
            text="Companies"
        )
        fig_sec.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Hiring Companies: %{x:,}<extra></extra>",
            marker=dict(line=dict(color="rgba(255,255,255,0.1)", width=1))
        )
        fig_sec.update_layout(
            **DARK_PLOT_THEME,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Total Hiring Companies"),
            yaxis=dict(title="", showgrid=False)
        )
        st.plotly_chart(fig_sec, use_container_width=True)

    # Charts Row 2: Treemap of Industry vs Startup Tags & Innovation Ecosystem Split (Replaced Company Name Character Length)
    c3, c4 = st.columns([6, 5])

    with c3:
        tree_df = filtered_df.groupby(["Industry", "Tags"]).size().reset_index(name="Count")
        
        fig_tree = px.treemap(
            tree_df,
            path=["Industry", "Tags"],
            values="Count",
            color="Industry",
            color_discrete_sequence=PALETTE,
            title="<b>Industry vs Startup Innovation Ecosystem (Treemap)</b>"
        )
        fig_tree.update_traces(
            hovertemplate="<b>%{label}</b><br>Companies: %{value:,}<extra></extra>",
            marker=dict(cornerradius=4)
        )
        fig_tree.update_layout(**DARK_PLOT_THEME)
        st.plotly_chart(fig_tree, use_container_width=True)

    with c4:
        # Replaced Company Name Character Length Histogram with Startup Innovation & Growth Tier Breakdown
        tag_counts = filtered_df["Tags"].value_counts().reset_index()
        tag_counts.columns = ["Innovation_Tier", "Count"]

        fig_tags = px.bar(
            tag_counts,
            x="Innovation_Tier",
            y="Count",
            color="Innovation_Tier",
            color_discrete_sequence=PALETTE,
            title="<b>Startup Innovation & Growth Tier Breakdown</b>",
            text="Count"
        )
        fig_tags.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            marker=dict(line=dict(color="#0B0F19", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>"
        )
        fig_tags.update_layout(
            **DARK_PLOT_THEME,
            showlegend=False,
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(title="Hiring Companies", showgrid=True, gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_tags, use_container_width=True)

    # Replaced Alphabetical Distribution Matrix with Data Hiring Tech Clusters & Specializations
    st.markdown("### 🔥 **High-Demand Data Tech Clusters & Hiring Specializations**")
    
    # Calculate Cluster Counts dynamically
    c_ai = filtered_df["Company_Name"].str.contains(r"ai|gpt|neural|intel|bot|deep|llm|vision|agentic", case=False, regex=True) | (filtered_df["TLD"] == ".ai")
    c_cloud = filtered_df["Company_Name"].str.contains(r"cloud|sec|cyber|guard|auth|devops|infra|host|server", case=False, regex=True) | filtered_df["TLD"].isin([".dev", ".io"])
    c_data = filtered_df["Company_Name"].str.contains(r"data|analytics|insight|metric|bi|warehouse|lake|query", case=False, regex=True)
    c_fin = filtered_df["Company_Name"].str.contains(r"fin|pay|bank|capital|fund|crypto|coin|trading|wealth", case=False, regex=True) | (filtered_df["TLD"] == ".finance")
    c_health = filtered_df["Company_Name"].str.contains(r"health|med|bio|care|pharma|therap|genom|doctor", case=False, regex=True)
    c_comm = filtered_df["Company_Name"].str.contains(r"shop|store|retail|market|commerce|brand|ecommerce", case=False, regex=True)

    cluster_data = pd.DataFrame({
        "Tech Cluster": [
            "🤖 Generative AI & Autonomous Systems",
            "☁️ Cloud Data Infra & Cybersecurity",
            "📊 Core Big Data, BI & Warehousing",
            "⚡ FinTech, DeFi & Quant Analytics",
            "🧬 Health Informatics & BioTech",
            "🛒 E-Commerce & Retail Intelligence"
        ],
        "Specialization Focus": [
            "LLMs, Prompt Engineering, Agentic AI, Computer Vision",
            "Kubernetes, Cloud ETL, Distributed Storage, SecOps",
            "Snowflake, Databricks, dbt, BI Dashboards, SQL",
            "Algorithmic Trading, Risk Modeling, Payments, Crypto",
            "Genomics Data, Clinical Informatics, Telehealth",
            "Customer Analytics, Recommendation Engines, Supply Chain"
        ],
        "Company Count": [
            c_ai.sum(),
            c_cloud.sum(),
            c_data.sum(),
            c_fin.sum(),
            c_health.sum(),
            c_comm.sum()
        ]
    }).sort_values(by="Company Count", ascending=True)

    fig_cluster = px.bar(
        cluster_data,
        x="Company Count",
        y="Tech Cluster",
        orientation="h",
        color="Company Count",
        color_continuous_scale="Turbo",
        title="<b>Data Hiring Specialization Clusters (Real-time Skill Demand)</b>",
        text="Company Count",
        hover_data={"Specialization Focus": True, "Company Count": ":,"}
    )
    fig_cluster.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Key Focus: %{customdata[0]}<br>Hiring Companies: %{x:,}<extra></extra>"
    )
    fig_cluster.update_layout(
        **DARK_PLOT_THEME,
        coloraxis_showscale=False,
        xaxis=dict(title="Number of Hiring Organizations", showgrid=True, gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(title="", showgrid=False)
    )
    st.plotly_chart(fig_cluster, use_container_width=True)


# ==============================================================================
# TAB 2: COMPANY EXPLORER & DIRECTORY
# ==============================================================================
elif nav_selection == "🔎 Company Explorer":
    st.markdown("### 🔎 **Interactive Company Search & Directory**")
    st.write("Search, filter, and discover companies actively hiring for Data Science, Data Engineering, ML, and Analytics roles.")

    # In-page Search Bar and Controls
    col_search, col_view, col_sort = st.columns([6, 3, 3])
    with col_search:
        search_query = st.text_input("🔍 Search Company Name, Domain, or Handle", placeholder="e.g. AI, OpenAI, Fintech, Stealth, Lab...", help="Instant search across 41,000+ companies")
    with col_view:
        view_mode = st.radio("Display View", ["📋 Data Table", "🗂️ Interactive Cards"], horizontal=True)
    with col_sort:
        sort_by = st.selectbox("Sort By", ["Company Name (A-Z)", "Company Name (Z-A)", "Name Length (Shortest)", "Name Length (Longest)"])

    # Search Filtering
    search_df = filtered_df.copy()
    if search_query:
        q = search_query.strip().lower()
        search_df = search_df[
            search_df["Company_Name"].str.lower().str.contains(q, na=False) |
            search_df["Domain"].str.lower().str.contains(q, na=False) |
            search_df["LinkedIn_Handle"].str.lower().str.contains(q, na=False) |
            search_df["Industry"].str.lower().str.contains(q, na=False)
        ]

    # Sorting
    if sort_by == "Company Name (A-Z)":
        search_df = search_df.sort_values(by="Company_Name", ascending=True, key=lambda col: col.str.lower())
    elif sort_by == "Company Name (Z-A)":
        search_df = search_df.sort_values(by="Company_Name", ascending=False, key=lambda col: col.str.lower())
    elif sort_by == "Name Length (Shortest)":
        search_df = search_df.sort_values(by="Name_Length", ascending=True)
    elif sort_by == "Name Length (Longest)":
        search_df = search_df.sort_values(by="Name_Length", ascending=False)

    # Result Metrics Bar
    res_col1, res_col2, res_col3 = st.columns([4, 4, 4])
    with res_col1:
        st.markdown(f"**Found `{len(search_df):,}` matching companies** (out of `{len(df_raw):,}`)")
    with res_col2:
        csv_data = search_df[["Company_Name", "Website", "LinkedIn_URL", "Industry", "Tags"]].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Current Results (CSV)",
            data=csv_data,
            file_name="data_hiring_companies_export.csv",
            mime="text/csv",
            use_container_width=True
        )
    with res_col3:
        json_data = search_df[["Company_Name", "Website", "LinkedIn_URL", "Industry", "Tags"]].to_json(orient="records").encode('utf-8')
        st.download_button(
            label="📦 Export Results (JSON)",
            data=json_data,
            file_name="data_hiring_companies_export.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Render View
    if view_mode == "📋 Data Table":
        # Format links for st.dataframe
        table_df = search_df[["Company_Name", "Industry", "Domain", "Tags", "Website", "LinkedIn_URL"]].copy()
        
        # Ensure full URL prefix
        table_df["Website"] = table_df["Website"].apply(lambda w: f"https://{w}" if w and not w.startswith("http") else w)

        st.dataframe(
            table_df,
            column_config={
                "Company_Name": st.column_config.TextColumn("Company Name", width="medium"),
                "Industry": st.column_config.TextColumn("Industry Sector", width="medium"),
                "Domain": st.column_config.TextColumn("Domain", width="small"),
                "Tags": st.column_config.TextColumn("Tags & Badges", width="small"),
                "Website": st.column_config.LinkColumn("Website Link", display_text="🌐 Open Web", width="small"),
                "LinkedIn_URL": st.column_config.LinkColumn("LinkedIn Profile", display_text="🔗 View LinkedIn", width="small"),
            },
            hide_index=True,
            use_container_width=True,
            height=600
        )
    else:
        # Card View with Pagination
        PAGE_SIZE = 12
        total_pages = max(1, (len(search_df) + PAGE_SIZE - 1) // PAGE_SIZE)
        
        pag_col1, pag_col2, pag_col3 = st.columns([3, 6, 3])
        with pag_col2:
            page = st.number_input(f"Page (Total {total_pages:,} pages)", min_value=1, max_value=total_pages, value=1, step=1)
        
        start_idx = (page - 1) * PAGE_SIZE
        end_idx = start_idx + PAGE_SIZE
        page_items = search_df.iloc[start_idx:end_idx]

        cols = st.columns(3)
        for i, (_, row) in enumerate(page_items.iterrows()):
            c = cols[i % 3]
            with c:
                web_url = row['Website'] if row['Website'].startswith('http') else f"https://{row['Website']}" if row['Website'] else "#"
                li_url = row['LinkedIn_URL'] if row['LinkedIn_URL'] else "#"
                
                tag_class = "tag-ai" if "AI" in row['Industry'] else ("tag-yc" if "YC" in row['Tags'] else "tag-badge")
                
                st.markdown(f"""
                    <div class="company-card">
                        <div class="company-name">{row['Company_Name']}</div>
                        <div style="margin-bottom: 8px;">
                            <span class="{tag_class}">{row['Industry']}</span>
                            <span class="tag-badge" style="margin-left: 4px;">{row['Tags']}</span>
                        </div>
                        <div class="company-meta">
                            <span>🌐 <b>Domain:</b> {row['Domain'] if row['Domain'] else 'N/A'}</span>
                        </div>
                        <div style="margin-top: 12px; display: flex; gap: 8px;">
                            <a href="{web_url}" target="_blank" style="flex: 1; text-align: center; background: rgba(99, 102, 241, 0.2); color: #A5B4FC; padding: 6px 10px; border-radius: 6px; text-decoration: none; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(99, 102, 241, 0.4);">🌐 Website</a>
                            <a href="{li_url}" target="_blank" style="flex: 1; text-align: center; background: rgba(56, 189, 248, 0.2); color: #38BDF8; padding: 6px 10px; border-radius: 6px; text-decoration: none; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(56, 189, 248, 0.4);">🔗 LinkedIn</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Direct Add to CRM Button
                if st.button(f"📌 Track Application", key=f"track_btn_{start_idx + i}", use_container_width=True):
                    exists = any(item["Company_Name"] == row["Company_Name"] for item in st.session_state["crm_tracker"])
                    if not exists:
                        st.session_state["crm_tracker"].append({
                            "id": str(len(st.session_state["crm_tracker"]) + 1),
                            "Company_Name": row["Company_Name"],
                            "Website": row["Website"],
                            "LinkedIn_URL": row["LinkedIn_URL"],
                            "Target_Role": "Data Scientist / ML",
                            "Status": "Interested",
                            "Priority": "⭐⭐⭐⭐",
                            "Notes": f"Discovered via Search. Industry: {row['Industry']}",
                            "Date_Added": datetime.date.today().strftime("%Y-%m-%d")
                        })
                        st.success(f"Added {row['Company_Name']} to your CRM Tracker! 🎯")
                    else:
                        st.info(f"{row['Company_Name']} is already in your tracker.")


# ==============================================================================
# TAB 3: OUTREACH & APPLICATION CRM TRACKER
# ==============================================================================
elif nav_selection == "🎯 Outreach & CRM Tracker":
    st.markdown("### 🎯 **Personal Job Application & Outreach CRM**")
    st.write("Manage your active outreach, interviews, and applications across the 41,000+ data hiring companies.")

    crm_list = st.session_state["crm_tracker"]
    crm_df = pd.DataFrame(crm_list)

    # CRM Pipeline Funnel Metrics
    status_counts = {"Interested": 0, "Outreach Sent": 0, "Interviewing": 0, "Offer Received": 0, "Archived": 0}
    if not crm_df.empty and "Status" in crm_df.columns:
        for s, count in crm_df["Status"].value_counts().items():
            if s in status_counts:
                status_counts[s] = count

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #6366F1;">
                <div class="metric-label">📌 Interested</div>
                <div class="metric-value">{status_counts['Interested']}</div>
            </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #38BDF8;">
                <div class="metric-label">✉️ Outreach Sent</div>
                <div class="metric-value">{status_counts['Outreach Sent']}</div>
            </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #F59E0B;">
                <div class="metric-label">💬 Interviewing</div>
                <div class="metric-value">{status_counts['Interviewing']}</div>
            </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #10B981;">
                <div class="metric-label">🎉 Offers Received</div>
                <div class="metric-value">{status_counts['Offer Received']}</div>
            </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #64748B;">
                <div class="metric-label">📁 Total Tracked</div>
                <div class="metric-value">{len(crm_df)}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # CRM Controls: Add New Entry or Manage
    with st.expander("➕ **Add New Company to Application Tracker**", expanded=False):
        f1, f2, f3 = st.columns(3)
        with f1:
            add_comp_name = st.text_input("Company Name", placeholder="e.g. OpenAI")
            add_role = st.selectbox("Target Role", ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "Analytics Engineer", "Data Engineer", "AI Research Scientist", "BI Specialist"])
        with f2:
            add_website = st.text_input("Website", placeholder="e.g. openai.com")
            add_status = st.selectbox("Current Status", ["Interested", "Outreach Sent", "Interviewing", "Offer Received", "Archived"])
        with f3:
            add_linkedin = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/company/...")
            add_priority = st.selectbox("Priority", ["⭐⭐⭐⭐⭐ (Top Priority)", "⭐⭐⭐⭐ (High)", "⭐⭐⭐ (Medium)", "⭐⭐ (Low)"])
        
        add_notes = st.text_area("Outreach Notes / Contact Details / Referral", placeholder="Add recruiter names, interview timeline, or custom notes...")

        if st.button("🚀 Add to My Pipeline", use_container_width=True):
            if add_comp_name.strip():
                st.session_state["crm_tracker"].append({
                    "id": str(len(st.session_state["crm_tracker"]) + 1),
                    "Company_Name": add_comp_name.strip(),
                    "Website": add_website.strip(),
                    "LinkedIn_URL": add_linkedin.strip(),
                    "Target_Role": add_role,
                    "Status": add_status,
                    "Priority": add_priority.split(" ")[0],
                    "Notes": add_notes.strip(),
                    "Date_Added": datetime.date.today().strftime("%Y-%m-%d")
                })
                st.success(f"Added {add_comp_name} to your pipeline!")
                st.rerun()
            else:
                st.error("Please enter a valid company name.")

    # Interactive Pipeline Table & Management
    st.markdown("#### 📋 **Active Applications Pipeline**")
    if not crm_df.empty:
        # Display editable or card list
        for idx, entry in enumerate(st.session_state["crm_tracker"]):
            with st.container():
                st.markdown(f"""
                    <div class="crm-card" style="border-left-color: {'#10B981' if entry['Status'] == 'Offer Received' else ('#F59E0B' if entry['Status'] == 'Interviewing' else ('#38BDF8' if entry['Status'] == 'Outreach Sent' else '#6366F1'))};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF;">{entry['Company_Name']}</span>
                                <span style="margin-left: 10px; font-size: 0.8rem; background: rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 4px; color: #E2E8F0;">{entry['Target_Role']}</span>
                                <span style="margin-left: 6px; font-size: 0.8rem; color: #FCD34D;">{entry['Priority']}</span>
                            </div>
                            <div style="display: flex; gap: 8px; align-items: center;">
                                <span style="font-size: 0.8rem; font-weight: 600; padding: 4px 10px; border-radius: 20px; background: rgba(99, 102, 241, 0.2); color: #818CF8;">{entry['Status']}</span>
                                <span style="font-size: 0.75rem; color: #64748B;">📅 {entry['Date_Added']}</span>
                            </div>
                        </div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 8px; line-height: 1.4;">
                            <b>Notes:</b> {entry['Notes'] if entry['Notes'] else 'No notes recorded.'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_u1, col_u2, col_u3, col_u4 = st.columns([3, 3, 3, 3])
                with col_u1:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Interested", "Outreach Sent", "Interviewing", "Offer Received", "Archived"],
                        index=["Interested", "Outreach Sent", "Interviewing", "Offer Received", "Archived"].index(entry["Status"]) if entry["Status"] in ["Interested", "Outreach Sent", "Interviewing", "Offer Received", "Archived"] else 0,
                        key=f"status_select_{idx}"
                    )
                    if new_status != entry["Status"]:
                        st.session_state["crm_tracker"][idx]["Status"] = new_status
                        st.rerun()
                with col_u2:
                    if entry.get("Website"):
                        web_link = entry["Website"] if entry["Website"].startswith("http") else f"https://{entry['Website']}"
                        st.link_button("🌐 Open Website", web_link, use_container_width=True)
                with col_u3:
                    if entry.get("LinkedIn_URL"):
                        st.link_button("🔗 Open LinkedIn", entry["LinkedIn_URL"], use_container_width=True)
                with col_u4:
                    if st.button("🗑️ Remove", key=f"del_crm_{idx}", use_container_width=True):
                        st.session_state["crm_tracker"].pop(idx)
                        st.rerun()

                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # Export Tracker
        st.markdown("---")
        crm_export_df = pd.DataFrame(st.session_state["crm_tracker"])
        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            st.download_button(
                "📥 Backup Applications Tracker (JSON)",
                data=crm_export_df.to_json(orient="records", indent=2),
                file_name="my_data_job_tracker.json",
                mime="application/json",
                use_container_width=True
            )
        with c_exp2:
            st.download_button(
                "📊 Export Tracker to CSV",
                data=crm_export_df.to_csv(index=False),
                file_name="my_data_job_tracker.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No applications currently tracked. Use the 'Add New Company' form above or click 'Track Application' in the Company Explorer!")


# ==============================================================================
# TAB 4: DISCOVERY ROULETTE & SERENDIPITY ENGINE
# ==============================================================================
elif nav_selection == "🎲 Discovery Roulette":
    st.markdown("### 🎲 **Serendipitous Company Discovery Roulette**")
    st.write("Spin the engine to discover high-potential hidden gems, AI startups, and data-centric enterprises from the 41,000+ pool.")

    roulette_pool = filtered_df if len(filtered_df) > 0 else df_raw

    spin_col1, spin_col2, spin_col3 = st.columns([4, 4, 4])
    with spin_col2:
        spin_btn = st.button("🎲 **Spin & Discover Random Company**", use_container_width=True)

    if spin_btn or len(st.session_state["roulette_history"]) == 0:
        sample_row = roulette_pool.sample(1).iloc[0]
        st.session_state["roulette_history"].insert(0, sample_row.to_dict())

    # Current Discovered Company
    if st.session_state["roulette_history"]:
        current_comp = st.session_state["roulette_history"][0]
        
        web_link = current_comp['Website'] if current_comp['Website'].startswith('http') else f"https://{current_comp['Website']}" if current_comp['Website'] else "#"
        li_link = current_comp['LinkedIn_URL'] if current_comp['LinkedIn_URL'] else "#"
        google_query = f"https://www.google.com/search?q={current_comp['Company_Name'].replace(' ', '+')}+data+science+careers+jobs"

        # Fixed raw HTML formatting without extra indentation
        card_html = f"""<div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border: 2px solid #6366F1; border-radius: 18px; padding: 28px; margin: 20px 0; box-shadow: 0 15px 35px rgba(99, 102, 241, 0.2);">
<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
<div>
<div style="font-size: 0.8rem; color: #818CF8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Featured Opportunity Match</div>
<div style="font-size: 2.1rem; font-weight: 800; color: #FFFFFF; margin: 4px 0;">{current_comp['Company_Name']}</div>
<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px;">
<span class="tag-badge tag-ai" style="font-size: 0.85rem; padding: 4px 12px;">🏢 {current_comp['Industry']}</span>
<span class="tag-badge" style="font-size: 0.85rem; padding: 4px 12px;">🌐 {current_comp['TLD']}</span>
<span class="tag-badge tag-yc" style="font-size: 0.85rem; padding: 4px 12px;">🏷️ {current_comp['Tags']}</span>
</div>
</div>
<div style="text-align: right;">
<span style="background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 6px 14px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(16, 185, 129, 0.4);">✓ Verified Hiring Database</span>
</div>
</div>
<div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
<div>
<div style="font-size: 0.75rem; color: #94A3B8;">PRIMARY DOMAIN</div>
<div style="font-size: 0.95rem; font-weight: 600; color: #F1F5F9;">{current_comp['Domain'] if current_comp['Domain'] else 'N/A'}</div>
</div>
<div>
<div style="font-size: 0.75rem; color: #94A3B8;">LINKEDIN PROFILE SLUG</div>
<div style="font-size: 0.95rem; font-weight: 600; color: #F1F5F9;">{current_comp['LinkedIn_Handle'] if current_comp['LinkedIn_Handle'] else 'N/A'}</div>
</div>
<div>
<div style="font-size: 0.75rem; color: #94A3B8;">GEOGRAPHIC FOOTPRINT</div>
<div style="font-size: 0.95rem; font-weight: 600; color: #F1F5F9;">{current_comp['Location']}</div>
</div>
</div>
</div>"""
        st.markdown(card_html, unsafe_allow_html=True)

        d_col1, d_col2, d_col3, d_col4 = st.columns(4)
        with d_col1:
            st.link_button("🌐 Launch Company Website", web_link, use_container_width=True)
        with d_col2:
            st.link_button("🔗 View LinkedIn Careers", li_link, use_container_width=True)
        with d_col3:
            st.link_button("🔍 Google Active Openings", google_query, use_container_width=True)
        with d_col4:
            if st.button("📌 Add to CRM Application Tracker", use_container_width=True):
                exists = any(item["Company_Name"] == current_comp["Company_Name"] for item in st.session_state["crm_tracker"])
                if not exists:
                    st.session_state["crm_tracker"].append({
                        "id": str(len(st.session_state["crm_tracker"]) + 1),
                        "Company_Name": current_comp["Company_Name"],
                        "Website": current_comp["Website"],
                        "LinkedIn_URL": current_comp["LinkedIn_URL"],
                        "Target_Role": "Data Scientist / ML",
                        "Status": "Interested",
                        "Priority": "⭐⭐⭐⭐⭐",
                        "Notes": f"Discovered via Discovery Roulette. Industry: {current_comp['Industry']}",
                        "Date_Added": datetime.date.today().strftime("%Y-%m-%d")
                    })
                    st.success(f"Saved {current_comp['Company_Name']} to CRM Tracker! 🎯")
                else:
                    st.info(f"{current_comp['Company_Name']} is already in your tracker.")

        # Previously Discovered History
        if len(st.session_state["roulette_history"]) > 1:
            st.markdown("---")
            st.markdown("#### 📜 **Previously Discovered in this Session**")
            prev_df = pd.DataFrame(st.session_state["roulette_history"][1:10])
            st.dataframe(
                prev_df[["Company_Name", "Industry", "Domain", "Tags", "Website", "LinkedIn_URL"]],
                use_container_width=True,
                hide_index=True
            )


# ==============================================================================
# TAB 5: DEEP ANALYTICS & CUSTOM INSIGHTS
# ==============================================================================
elif nav_selection == "📈 Deep Analytics":
    st.markdown("### 📈 **Deep Comparative Analytics & Market Trends**")
    st.write("Slice, dice, and uncover structural patterns, innovation badges, and industry correlations across 41,000+ organizations.")

    a_col1, a_col2 = st.columns(2)

    with a_col1:
        # Replaced Industry vs Top Domain Extensions Heatmap with Industry vs Innovation Badges Matrix
        ctab = pd.crosstab(df_raw["Industry"], df_raw["Tags"])

        fig_heat = px.imshow(
            ctab,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="<b>Industry vs Innovation Badges Matrix (Cross-Tab Heatmap)</b>"
        )
        fig_heat.update_layout(
            **DARK_PLOT_THEME,
            xaxis=dict(title="Innovation / Startup Category"),
            yaxis=dict(title="Industry Sector")
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with a_col2:
        # Top word tokens in company names
        words = []
        for name in df_raw["Company_Name"]:
            tokens = re.findall(r"\b[A-Za-z]{3,}\b", name.lower())
            for t in tokens:
                if t not in ["the", "and", "for", "inc", "llc", "ltd", "corp", "group", "services", "solutions", "technologies", "company"]:
                    words.append(t.title())

        word_counts = pd.Series(words).value_counts().head(12).reset_index()
        word_counts.columns = ["Keyword", "Frequency"]
        word_counts = word_counts.sort_values(by="Frequency", ascending=True)

        fig_words = px.bar(
            word_counts,
            x="Frequency",
            y="Keyword",
            orientation="h",
            color="Frequency",
            color_continuous_scale="Viridis",
            title="<b>Top Semantic Keywords in Company Names</b>",
            text="Frequency"
        )
        fig_words.update_traces(
            texttemplate="%{text:,}",
            textposition="outside"
        )
        fig_words.update_layout(
            **DARK_PLOT_THEME,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Occurrences"),
            yaxis=dict(title="")
        )
        st.plotly_chart(fig_words, use_container_width=True)

    st.markdown("---")

    # Interactive Query Slice & Dice Builder
    st.markdown("#### 🧪 **Custom Data Query Sandbox**")
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        min_len, max_len = st.slider(
            "Filter by Company Name Length (Characters)",
            min_value=int(df_raw["Name_Length"].min()),
            max_value=int(df_raw["Name_Length"].max()),
            value=(3, 30)
        )
    with q_col2:
        selected_sectors = st.multiselect(
            "Filter by Industry Sector(s)",
            options=sorted(df_raw["Industry"].unique().tolist()),
            default=[]
        )

    sandbox_df = df_raw[(df_raw["Name_Length"] >= min_len) & (df_raw["Name_Length"] <= max_len)]
    if selected_sectors:
        sandbox_df = sandbox_df[sandbox_df["Industry"].isin(selected_sectors)]

    st.markdown(f"**Sandbox Subset:** `{len(sandbox_df):,}` companies match your custom query parameters.")
    st.dataframe(
        sandbox_df[["Company_Name", "Industry", "Domain", "Tags", "Website", "LinkedIn_URL"]].head(100),
        use_container_width=True,
        hide_index=True
    )
