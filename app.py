# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from io import BytesIO

st.set_page_config(
    page_title="Dhrubo Bhattacharjee — Future Skills Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Resume text (used for download)
# ----------------------------
RESUME_TEXT = """
Dhrubo Bhattacharjee
Email: dhrubob026@gmail.com
Github: github.com/Dhrubo2003
Mobile: +91-9881453253

Education
• Symbiosis Institute Of Technology Pune, India
  Bachelor of Technology - Artificial Intelligence and Machine Learning; GPA: 7.3
  Courses: Artificial Intelligence, Machine Learning, Data Analytics, Databases

Skills Summary
• Languages: Python, SQL.
• Frameworks: Pytorch, TensorFlow, Keras.
• Tools: PowerBI, Excel, Looker Studio, MySQL, Ansible, Elasticsearch, Logstash, Kibana.
• Certification: MySQL, Data Visualization with PowerBI, Python for Data Science, Google’s Data Analytics Certification.
• Skills: Python, Data Science, Data Visualization, Neural Network, Data Analytics, Machine Learning, Deep Learning, Predictive Modeling.
• Soft Skills: Leadership, Time Management, Event Management.

Experience
• Bristlecone (Hybrid) — Associate Data Scientist (Full-time) — August 2025 - Present
• Tanex Solution (Remote) — Jr. Data Analyst (Internship) — Jan 2025 - Jun 2025
  Project: ELK stack data analysis and AI engine
• Dassault Systemes (Remote) — Industry Project (Part-time) — Aug 2024 - Nov 2024
  Project: Export Control Class Hierarchy using stsb-roberta-large
• GGP-PAAI Student Conference / Aston University (Remote) — Research — May 2023 - Jul 2023
  Research on ChatGPT merits/demerits (sponsored by British Council)
• Vodafone (VOIS) — Data Science Intern — Aug 2022 - Oct 2022
  Project: Player Market Value Prediction (Regression, 96% stated accuracy)

Projects
• Real Time System Information & Performance Monitor
  - Used psutil, integrated with SQL, visualized in Power BI.

• Export-Control-Class-Hierarchy
  - Used stsb-roberta-large for semantic similarity and a tooltip-based UI.

• Comparative Analysis of GANs for Multispectral Satellite Image Dehazing
  - CycleGANs, Pix2Pix, ViT GANs. Top PSNR 60 & SSIM 0.99.

• Sentiment Analysis using Speech Emotion Recognition
  - RAVDESS dataset with CNN+LSTM, 94% accuracy.

(End of resume)
"""

# ----------------------------
# Profile info (for display)
# ----------------------------
PROFILE = {
    "name": "Dhrubo Bhattacharjee",
    "headline": "ML & Data Analytics | AIML Grad | ELK (Beginner) | Building Predictive Systems",
    "about": (
        "AIML graduate skilled in Python, ML modeling and basic ELK configuration. "
        "I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening "
        "DevOps/MLOps competencies to transition from ML Analyst to ML Engineer and, later, MLOps Lead."
    ),
    "email": "dhrubob026@gmail.com",
    "github": "https://github.com/Dhrubo2003",
    "linkedin": "https://www.linkedin.com/in/dhrubo-bhattacharjee/",
    # direct-access Google Drive image (converted)
    "image_url": "https://drive.google.com/uc?id=1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ"
}

# ----------------------------
# Skills: base = current (0-100), max = max achievable (0-100), k/p = growth shape
# ELK marked as beginner (low base)
# ----------------------------
SKILLS = {
    "Python":       {"base": 70, "max": 95, "k": 0.6, "p": 1.0, "category": "Programming"},
    "Machine Learning": {"base": 60, "max": 95, "k": 0.5, "p": 1.0, "category": "ML"},
    "Deep Learning": {"base": 55, "max": 95, "k": 0.45, "p": 1.0, "category": "ML"},
    "Data Visualization": {"base": 65, "max": 92, "k": 0.5, "p": 1.0, "category": "Viz"},
    "SQL / MySQL":  {"base": 60, "max": 85, "k": 0.5, "p": 1.0, "category": "Data"},
    "PowerBI / Looker": {"base": 60, "max": 90, "k": 0.5, "p": 1.0, "category": "Viz"},
    "Ansible":      {"base": 30, "max": 80, "k": 0.6, "p": 1.0, "category": "DevOps"},
    "Elasticsearch": {"base": 20, "max": 80, "k": 0.6, "p": 1.0, "category": "ELK"},
    "Logstash":     {"base": 25, "max": 80, "k": 0.6, "p": 1.0, "category": "ELK"},
    "Kibana":       {"base": 25, "max": 80, "k": 0.6, "p": 1.0, "category": "ELK"},
    "PyTorch / TF / Keras": {"base": 55, "max": 92, "k": 0.5, "p": 1.0, "category": "ML"},
    "MLOps (concepts)": {"base": 20, "max": 90, "k": 0.5, "p": 1.1, "category": "DevOps"},
    "Docker / Containers": {"base": 20, "max": 85, "k": 0.6, "p": 1.0, "category": "DevOps"},
    "Data Engineering": {"base": 40, "max": 90, "k": 0.45, "p": 1.0, "category": "Data"}
}

# ----------------------------
# Projects & certs (short)
# ----------------------------
PROJECTS = [
    {
        "title": "Real Time System Information & Performance Monitor",
        "short_description": "psutil-based system monitoring, SQL integration, Power BI dashboards.",
    },
    {
        "title": "Export-Control-Class-Hierarchy",
        "short_description": "Semantic similarity using stsb-roberta-large to rank export control codes.",
    },
    {
        "title": "Comparative Analysis of GANs (Satellite Image Dehazing)",
        "short_description": "CycleGAN/Pix2Pix/ViT GAN comparisons on multispectral datasets; strong PSNR/SSIM results.",
    },
    {
        "title": "Speech Emotion Recognition (Sentiment from Audio)",
        "short_description": "CNN+LSTM on RAVDESS; extensive preprocessing; ~94% accuracy.",
    }
]

CERTIFICATIONS = [
    {"name": "MySQL Certification", "issuer": "MySQL / Coursera", "date": "2023"},
    {"name": "Data Visualization with PowerBI", "issuer": "Coursera", "date": "2023"},
    {"name": "Python for Data Science", "issuer": "Coursera", "date": "2022"},
    {"name": "Google Data Analytics Certificate", "issuer": "Google / Coursera", "date": "2022"},
]

# ----------------------------
# Prediction / growth model
# ----------------------------
def predict_skill_level(base: float, max_level: float, k: float, p: float, years: float):
    years = max(0.0, float(years))
    try:
        growth = (1 - math.exp(-k * years)) ** p
    except Exception:
        growth = 0.0
    value = base + (max_level - base) * growth
    return max(0.0, min(100.0, value))

def skills_df_for_year(skills_dict, years):
    rows = []
    for skill, meta in skills_dict.items():
        base = float(meta.get("base", 10))
        max_level = float(meta.get("max", 90))
        k = float(meta.get("k", 0.5))
        p = float(meta.get("p", 1.0))
        predicted = predict_skill_level(base, max_level, k, p, years)
        rows.append({
            "skill": skill,
            "current": base,
            "predicted": predicted,
            "category": meta.get("category", "Other")
        })
    df = pd.DataFrame(rows).sort_values("predicted", ascending=False).reset_index(drop=True)
    return df

# ----------------------------
# Sidebar (profile + controls)
# ----------------------------
with st.sidebar:
    # profile image
    try:
        st.image(PROFILE["image_url"], width=140)
    except Exception:
        st.write("")  # graceful fallback

    st.markdown(f"### {PROFILE['name']}")
    st.markdown(f"**{PROFILE['headline']}**")
    st.write(PROFILE["about"])
    st.markdown("---")

    # Experience slider (years) — default to 0.5 (6 months)
    years = st.slider(
        "Experience (years)",
        min_value=0.0, max_value=10.0, value=0.5, step=0.25,
        help="Slide to simulate future experience level (how your skills grow with years)"
    )

    st.markdown("**Contact**")
    st.write(f"Email: {PROFILE['email']}")
    st.write(f"Github: {PROFILE['github']}")
    st.write(f"LinkedIn: {PROFILE['linkedin']}")

    st.markdown("---")
    # Resume download (serve the RESUME_TEXT bytes)
    b = RESUME_TEXT.encode("utf-8")
    st.download_button(
        label="Download Resume (text)",
        data=b,
        file_name="Dhrubo_Bhattacharjee_Resume.txt",
        mime="text/plain"
    )
    st.markdown("---")
    st.caption("Theme: Futuristic (dark/light). Charts are static and reflect predicted skill levels.")

# ----------------------------
# Top header (main)
# ----------------------------
col1, col2 = st.columns([3, 2])
with col1:
    st.title(PROFILE["name"])
    st.subheader(PROFILE["headline"])
    st.write(PROFILE["about"])
with col2:
    # KPI boxes
    st.metric("Current Experience", "6 months")
    st.metric("Projects", len(PROJECTS))
    st.metric("Certifications", len(CERTIFICATIONS))

st.markdown("---")

# ----------------------------
# Skill Projection Charts
# ----------------------------
st.header("Skill Projection")

df_skills = skills_df_for_year(SKILLS, years)

# Radar chart
def radar_figure(df: pd.DataFrame):
    categories = df["skill"].tolist()
    if len(categories) < 3:
        # plotly radar needs >=3 points; pad if needed
        categories += categories * (3 - len(categories))
    vals_pred = df["predicted"].tolist()
    vals_cur = df["current"].tolist()
    # close loop
    vals_pred += [vals_pred[0]]
    vals_cur += [vals_cur[0]]
    cats = categories + [categories[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals_cur, theta=cats, fill='toself', name='Current (approx.)'))
    fig.add_trace(go.Scatterpolar(r=vals_pred, theta=cats, fill='toself', name=f'Predicted @ {years} yrs'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), margin=dict(t=20,b=10))
    return fig

col_a, col_b = st.columns([2, 3])
with col_a:
    st.subheader("Radar — Current vs Predicted")
    st.plotly_chart(radar_figure(df_skills), use_container_width=True)
with col_b:
    st.subheader("Top Predicted Skills")
    topn = st.number_input("Show top N skills", min_value=3, max_value=len(df_skills), value=6, step=1)
    top_df = df_skills.head(int(topn))
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["current"], name="Current"))
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["predicted"], name=f"Predicted @ {years} yrs"))
    bar_fig.update_layout(barmode='group', yaxis=dict(range=[0,100]), margin=dict(t=30,b=10))
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# ----------------------------
# Timeline & Roles
# ----------------------------
st.header("Projected Roles & Timeline")
st.write(f"Selected experience: **{years} years**")

if years >= 5:
    st.success("Projected role: **MLOps Lead**")
elif years >= 3:
    st.info("Projected role: **ML Engineer**")
elif years >= 1.5:
    st.info("Projected role: **Junior/Sr ML Engineer (growing)**")
else:
    st.info("Projected role: **ML Analyst / Junior ML Engineer**")

st.markdown("**Projected milestones**")
timeline = [
    {"year": 1, "text": "Solidify ML fundamentals, reproducible pipelines"},
    {"year": 3, "text": "Productionized models, containerized pipelines, CI/CD"},
    {"year": 5, "text": "Lead MLOps initiatives, architecture & mentoring"},
]
for t in timeline:
    if years >= t["year"]:
        st.markdown(f"- ✅ Year {t['year']}: {t['text']}")
    else:
        st.markdown(f"- ⌛ Year {t['year']}: {t['text']}")

st.markdown("---")

# ----------------------------
# Projects
# ----------------------------
st.header("Selected Projects (College & Other)")
for proj in PROJECTS:
    st.subheader(proj["title"])
    st.write(proj["short_description"])

st.markdown("---")

# ----------------------------
# Certifications
# ----------------------------
st.header("Certifications")
cols = st.columns(3)
for i, cert in enumerate(CERTIFICATIONS):
    with cols[i % 3]:
        st.markdown(f"**{cert['name']}**")
        st.write(cert.get("issuer", ""))
        st.caption(cert.get("date", ""))

st.markdown("---")

# ----------------------------
# Footer / Contact
# ----------------------------
st.write("### Contact")
st.write(f"- Email: {PROFILE['email']}")
st.write(f"- GitHub: {PROFILE['github']}")
st.write(f"- LinkedIn: {PROFILE['linkedin']}")

st.caption("Prototype: Replace text resume with an uploaded PDF if you prefer, and/or replace the Drive image URL with a hosted profile image URL.")
