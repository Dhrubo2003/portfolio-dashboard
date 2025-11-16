# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math

# ---------------------------
# Config / Profile (edit here)
# ---------------------------
PAGE_TITLE = "Dhrubo Bhattacharjee — Future Skills Portfolio"
PROFILE_IMG_ID = "1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ"   # profile pic Google Drive file id
RESUME_FILE_ID = "1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E"   # resume Google Drive file id

PROFILE_IMG_URL = f"https://drive.google.com/uc?id={PROFILE_IMG_ID}"
RESUME_DL_URL = f"https://drive.google.com/uc?export=download&id={RESUME_FILE_ID}"

HEADLINE = "ML & Data Analytics | AIML Grad | ELK (Beginner) | Building Predictive Systems"
ABOUT_TEXT = (
    "AIML graduate skilled in Python, ML modeling and basic ELK configuration. "
    "I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening "
    "DevOps/MLOps competencies to transition from ML Analyst to ML Engineer and, later, MLOps Lead."
)

CONTACT = {
    "Email": "dhrubob026@gmail.com",
    "GitHub": "https://github.com/Dhrubo2003",
    "Mobile": "+91-9881453253",
    "LinkedIn": "https://www.linkedin.com/in/dhrubo-bhattacharjee/"
}

# ---------------------------
# Skills (base and growth)
# base = current approx level (0-100)
# max = expected max reachable (0-100)
# k, p = growth curve parameters (higher k -> faster early growth)
# category = for grouping on charts
# ---------------------------
SKILLS = {
    "Python":        {"base": 70, "max": 95, "k": 0.6, "p": 1.0, "category": "ML"},
    "Machine Learning": {"base": 65, "max": 95, "k": 0.5, "p": 1.0, "category": "ML"},
    "Deep Learning": {"base": 60, "max": 95, "k": 0.45, "p": 1.0, "category": "ML"},
    "Data Visualization": {"base": 68, "max": 92, "k": 0.5, "p": 1.0, "category": "Analytics"},
    "SQL":           {"base": 60, "max": 90, "k": 0.5, "p": 1.0, "category": "Analytics"},
    "ELK (Elasticsearch/Logstash/Kibana)": {"base": 30, "max": 80, "k": 0.6, "p": 1.0, "category": "Tools"},
    "Ansible":       {"base": 30, "max": 85, "k": 0.5, "p": 1.0, "category": "DevOps"},
    "Docker":        {"base": 20, "max": 90, "k": 0.5, "p": 1.0, "category": "DevOps"},
    "Kubernetes":    {"base": 10, "max": 88, "k": 0.45, "p": 1.0, "category": "DevOps"},
    "MLOps":         {"base": 15, "max": 92, "k": 0.5, "p": 1.0, "category": "DevOps"},
    "Git":           {"base": 50, "max": 90, "k": 0.4, "p": 1.0, "category": "Tools"}
}

# ---------------------------
# Projects (from resume)
# ---------------------------
PROJECTS = [
    {
        "title": "Real Time System Information & Performance Monitor",
        "short_description": "Monitors system metrics using psutil, stores data in SQL and visualizes in Power BI.",
        "tech": ["Python", "psutil", "SQL", "Power BI"],
        "long_description": "Leveraged psutil to extract real-time system stats, integrated with SQL for storage and created dynamic Power BI dashboards for performance monitoring."
    },
    {
        "title": "Export-Control-Class-Hierarchy",
        "short_description": "Identifies and ranks export control codes using stsb-roberta-large Sentence Transformer.",
        "tech": ["Transformers", "NLP", "Python"],
        "long_description": "Developed semantic similarity pipelines using stsb-roberta-large to recommend and rank export control codes with a tooltip-based UI for descriptions."
    },
    {
        "title": "Comparative Analysis of GANs for Multispectral Satellite Image Dehazing",
        "short_description": "Compared CycleGAN, Pix2Pix and ViT-GAN for image dehazing on SIH dataset.",
        "tech": ["GANs", "PyTorch", "Image Processing"],
        "long_description": "Analyzed results on Government of India SIH dataset; CycleGAN achieved best PSNR (60) and SSIM (0.99) in experiments."
    },
    {
        "title": "Sentiment Analysis using Speech Emotion Recognition",
        "short_description": "Built CNN+LSTM pipeline to detect emotions from audio with high accuracy.",
        "tech": ["CNN", "LSTM", "Audio processing"],
        "long_description": "Used RAVDESS dataset and advanced preprocessing for feature extraction; achieved ~94% accuracy."
    }
]

# ---------------------------
# Certifications (from resume)
# ---------------------------
CERTIFICATIONS = [
    {"name": "MySQL", "issuer": "Unknown", "date": ""},
    {"name": "Data Visualization with PowerBI", "issuer": "Unknown", "date": ""},
    {"name": "Python for Data Science", "issuer": "Unknown", "date": ""},
    {"name": "Google Data Analytics Certificate", "issuer": "Google", "date": ""},
]

# ---------------------------
# Simple growth model functions
# ---------------------------
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
    df = pd.DataFrame(rows).sort_values("predicted", ascending=False)
    return df

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title=PAGE_TITLE, layout="wide")

# Minimal CSS to get a dark futuristic look (neat but simple)
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0f1a; color:#dbe9ff; }
    .sidebar .sidebar-content { background: linear-gradient(180deg, #071021, #0b0f1a); }
    h1, h2, h3, .css-1v0mbdj { color: #dbe9ff; }
    .stButton>button { background: linear-gradient(90deg,#5b6cff,#9b5cff); color: white; }
    .metric-label { color: #98b6ff; }
    .css-1d391kg p { color: #c7d9ff; }
    a { color: #9bd0ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.image(PROFILE_IMG_URL, width=140)
    st.markdown(f"### {HEADLINE}")
    st.markdown(ABOUT_TEXT)
    st.markdown("---")
    # Experience slider (years) — user asked for experience bar
    experience_years = st.slider("Experience (years)", min_value=0.0, max_value=10.0, value=0.5, step=0.25,
                                 help="Slide to simulate expected experience — see how skills grow.")
    st.markdown("**Target roles (examples):**")
    st.write("- 0–2 yrs: ML Analyst / Junior ML Engineer")
    st.write("- 3 yrs: ML Engineer")
    st.write("- 5+ yrs: MLOps Lead / Senior ML Engineer")
    st.markdown("---")
    st.markdown(f"[Download Resume]({RESUME_DL_URL})")
    st.markdown("---")
    st.markdown("**Contact**")
    for k, v in CONTACT.items():
        st.write(f"- **{k}:** {v}")

# ---------- Header / KPIs ----------
col1, col2 = st.columns([2, 3])
with col1:
    st.title("Dhrubo Bhattacharjee")
    st.subheader(HEADLINE)
    st.write(ABOUT_TEXT)
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Experience", "6 months")
    c2.metric("Projects", len(PROJECTS))
    c3.metric("Certifications", len(CERTIFICATIONS))
with col2:
    # small visual placeholder using Plotly (no animation)
    fig_placeholder = go.Figure()
    fig_placeholder.add_trace(go.Scatter(x=[0,1,2], y=[0.2,0.6,0.9], mode='lines+markers'))
    fig_placeholder.update_layout(template='plotly_dark', margin=dict(l=0,r=0,t=10,b=0), height=220)
    st.plotly_chart(fig_placeholder, use_container_width=True)

st.markdown("---")

# ---------- Skill Projection ----------
st.header("Skill Projection")
df_skills = skills_df_for_year(SKILLS, experience_years)

# Radar chart
def radar_figure(df: pd.DataFrame):
    categories = df["skill"].tolist()
    values = df["predicted"].tolist()
    values_current = df["current"].tolist()
    if len(categories) < 3:
        # plotly radar needs >=3 points; fallback to bar chart
        return None
    cats = categories + [categories[0]]
    vals = values + [values[0]]
    vals_cur = values_current + [values_current[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals_cur, theta=cats, fill='toself', name='Current'))
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself', name=f'Predicted @ {experience_years} yrs'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), template='plotly_dark', showlegend=True, margin=dict(t=20,b=10))
    return fig

col_a, col_b = st.columns([2, 3])
with col_a:
    st.subheader("Radar: Current vs Predicted")
    radar = radar_figure(df_skills)
    if radar:
        st.plotly_chart(radar, use_container_width=True)
    else:
        st.write("Not enough skills for radar — showing top skills bar chart.")
        st.bar_chart(df_skills.set_index("skill")[["current", "predicted"]].head(6))
with col_b:
    st.subheader("Top Skills (Predicted)")
    topn = st.number_input("Show top N skills", min_value=3, max_value=len(df_skills), value=6, step=1)
    top_df = df_skills.head(int(topn))
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["current"], name="Current"))
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["predicted"], name=f"Predicted @ {experience_years} yrs"))
    bar_fig.update_layout(barmode='group', yaxis=dict(range=[0,100]), template='plotly_dark', margin=dict(t=30,b=10), height=350)
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# ---------- Timeline & Roles ----------
st.header("Projected Roles & Timeline")
st.markdown(f"**Selected experience:** {experience_years} years")
if experience_years >= 5:
    st.success("Projected role: **MLOps Lead**")
elif experience_years >= 3:
    st.info("Projected role: **ML Engineer**")
elif experience_years >= 1.5:
    st.info("Projected role: **Junior/Sr ML Engineer (growing)**")
else:
    st.info("Projected role: **ML Analyst / Junior ML Engineer**")

st.markdown("**Projected milestones**")
timeline = [
    {"year": 1, "text": "Solidify ML fundamentals, reproducible pipelines"},
    {"year": 3, "text": "Productionized ML models, containerized pipelines, CI/CD"},
    {"year": 5, "text": "Lead MLOps initiatives, architecture & mentoring"},
]
for t in timeline:
    if experience_years >= t["year"]:
        st.markdown(f"- ✅ Year {t['year']}: {t['text']}")
    else:
        st.markdown(f"- ⌛ Year {t['year']}: {t['text']}")

st.markdown("---")

# ---------- Projects ----------
st.header("Selected Projects (College & Other)")
for proj in PROJECTS:
    st.subheader(proj["title"])
    st.write(proj["short_description"])
    if proj.get("tech"):
        st.caption("Tech: " + ", ".join(proj["tech"]))
    with st.expander("Read more / Details"):
        st.write(proj.get("long_description", "No further details provided."))

st.markdown("---")

# ---------- Certifications ----------
st.header("Certifications")
cols = st.columns(3)
for i, cert in enumerate(CERTIFICATIONS):
    with cols[i % 3]:
        st.markdown(f"**{cert['name']}**")
        if cert.get("issuer"):
            st.write(cert.get("issuer"))
        if cert.get("date"):
            st.caption(cert.get("date"))

st.markdown("---")

# ---------- Footer ----------
st.markdown("### Contact & Notes")
st.write(f"- LinkedIn: {CONTACT['LinkedIn']}")
st.write(f"- Email: {CONTACT['Email']}")
st.write(f"- GitHub: {CONTACT['GitHub']}")
st.write("This is a minimal prototype (dark futuristic theme). Replace skill values, projects, or contact info above as required.")
