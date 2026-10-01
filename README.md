# ⚡ DataTalent Radar - Interactive Dark Theme Dashboard

An interactive, high-performance Streamlit dashboard engineered with an ultramodern dark theme to analyze, explore, and track **41,633+ companies actively hiring for Data & AI roles**.

---

## 🌟 Key Features

### 1. 📊 Executive Market Intelligence & Analytics
- **Top KPIs**: 41,633 Total Verified Companies, 4,350+ AI/ML Natives, 4,300+ Dev/Infra Organizations, YC & Techstars Startups, and 37,600+ Unique Web Domains.
- **Taxonomy Classification Engine**: Real-time NLP categorical grouping across 11 sectors (AI & Machine Learning, Data Infra, FinTech, HealthTech, Staffing, Cloud & CyberSec, E-Commerce, etc.).
- **Top-Level Domain (TLD) Analysis**: Breakdown of top web extensions (`.com`, `.ai`, `.io`, `.org`, `.app`, `.dev`, `.xyz`, `.finance`).
- **Interactive Visualizations**: Interactive Plotly Dark charts including Donut Sector Graphs, Treemaps, Company Name Character Length Histograms, and Alphabetical Distribution Matrices.

### 2. 🔎 Company Explorer & Smart Search
- **Instant Search**: Sub-second full-text searching across company names, domains, and LinkedIn slugs.
- **Dual Display Modes**: Toggle seamlessly between **Data Table View** (with clickable outbound links) and **Interactive Grid Cards**.
- **Data Exporting**: 1-click downloads for filtered subsets in **CSV** and **JSON** formats.

### 3. 🎯 Outreach & Job Application CRM Tracker
- **Session-Persistent Application Pipeline**: Track roles from *Interested 📌* to *Outreach Sent ✉️*, *Interviewing 💬*, and *Offer Received 🎉*.
- **Direct Tracker Integration**: Add companies directly from the Explorer or Discovery Roulette with a single click.
- **Custom Notes & Priority Ratings**: Assign 1–5 star priorities, target job titles, and interview notes.
- **Backup & Portability**: Export your pipeline to JSON / CSV anytime.

### 4. 🎲 Serendipitous Discovery Roulette
- **Opportunity Discovery Engine**: Generates featured company dossiers on demand.
- **Action Shortcuts**: Direct 1-click links to the company website, LinkedIn company profile, and a pre-configured Google search for active data job openings.

### 5. 📈 Deep Comparative Analytics & Query Sandbox
- **Sector vs TLD Cross-Tab Heatmap**: Reveal which industries adopt modern tech extensions (`.ai`, `.io`, `.xyz`).
- **Semantic Keyword Extractor**: Frequency analyzer of the top naming keywords.
- **Custom Sandbox**: Slice and dice companies by character length and initial letters.

---

## 🚀 How to Run

1. Open your terminal in this project directory:
   ```bash
   streamlit run app.py
   ```

2. The dashboard will automatically open in your browser at:
   ```
   http://localhost:8501
   ```

---

## ⚡ Performance Optimization
- **Parquet Caching**: The original Excel dataset (`41,633 rows`) is automatically enriched and cached into `processed_companies.parquet`, speeding up reload and filter operations to **< 30 milliseconds**.
