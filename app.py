# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from pathlib import Path
from streamlit_lottie import st_lottie
import json
from io import BytesIO
import base64

# Import project data (skills, projects, certs, profile text)
from data import PROFILE, SKILLS, PROJECTS, CERTIFICATIONS, HEADLINE, ABOUT_TEXT

st.set_page_config(page_title="Dhrubo Bhattacharjee — Future Skills Portfolio",
                   layout="wide",
                   initial_sidebar_state="expanded")

# ---------- Utilities ----------
def load_lottie_file(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def make_download_link(url: str, filename: str = "resume.pdf"):
    # If it's a Google share link or direct link, embed as link button.
    # Streamlit has st.download_button which needs bytes; but we don't have an actual file.
    # We'll create a clickable markdown link instead (placeholder).
    return f"[Download Resume]({url})"

# Simple growth model for skills:
# We'll model skill level (0-100) as a logistic-like curve:
# level(years) = base + (max_base - base) * (1 - exp(-k * years)) ^ p
def predict_skill_level(base: float, max_level: float, k: float, p: float, years: float):
    # clamp inputs
    years = max(0.0, float(years))
    try:
        growth = (1 - math.exp(-k * years)) ** p
    except Exception:
        growth = 0.0
    value = base + (max_level - base) * growth
    return max(0.0, min(100.0, value))

# Convert SKILLS dict -> DataFrame for plotting
def skills_df_for_year(skills_dict, years):
    rows = []
    for skill, meta in skills_dict.items():
        base = float(meta.get("base", 10))   # current level 0-100
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

# ---------- Sidebar ----------
with st.sidebar:
  
    PROFILE_PIC_URL = "https://drive.google.com/file/d/1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ/view?usp=sharing"
    st.image(PROFILE_PIC_URL, width=120)

    st.markdown(f"### {HEADLINE}")
    st.markdown(ABOUT_TEXT)
    st.markdown("---")
    years = st.slider("Project experience (years)", min_value=0.0, max_value=10.0, value=1.0, step=0.5,
                      help="Slide to simulate future experience. Recruiters can test how your skillset grows.")
    st.markdown("**Target roles (examples):**")
    st.write("- 0–2 yrs: ML Analyst / Junior ML Engineer")
    st.write("- 3 yrs: ML Engineer")
    st.write("- 5+ yrs: MLOps Lead / Senior ML Engineer")
    st.markdown("---")
    resume_link = "https://drive.google.com/file/d/1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E/view?usp=sharing"
    st.markdown(make_download_link(resume_link))
    st.markdown("---")
    st.caption("Theme: AI / Futuristic. Switch between light/dark via Streamlit settings if needed.")

# ---------- Top: Lottie / Hero ----------
col1, col2 = st.columns([2, 3])
with col1:
    st.title("Dhrubo Bhattacharjee")
    st.subheader(HEADLINE)
    st.write(ABOUT_TEXT)
    # Quick KPIs
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Current Experience", "6 months", delta=None)
    col_kpi2.metric("Projects", len(PROJECTS), delta=None)
    col_kpi3.metric("Certifications", len(CERTIFICATIONS), delta=None)
with col2:
    # attempt to load a lottie animation from assets
    lottie = load_lottie_file(Path("assets/lottie/ai_animation.json"))
    if lottie:
        st_lottie(lottie, height=250, key="hero")
    else:
        st.image("assets/images/.keep" if Path("assets/images/.keep").exists() else None, width=320)

st.markdown("---")

# ---------- Skills Charts ----------
st.header("Skill Projection")
df_skills = skills_df_for_year(SKILLS, years)

# Radar chart (Plotly)
def radar_figure(df: pd.DataFrame):
    categories = df["skill"].tolist()
    values = df["predicted"].tolist()
    values_current = df["current"].tolist()
    # close the loop
    cats = categories + [categories[0]]
    vals = values + [values[0]]
    vals_cur = values_current + [values_current[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals_cur, theta=cats, fill='toself',
                                  name='Current (approx.)'))
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself',
                                  name=f'Predicted @ {years} yrs'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                      showlegend=True, margin=dict(l=10,r=10,t=30,b=10))
    return fig

col_a, col_b = st.columns([2, 3])
with col_a:
    st.subheader("Radar: Current vs Predicted")
    st.plotly_chart(radar_figure(df_skills), use_container_width=True)
with col_b:
    st.subheader("Top Skills (Predicted)")
    topn = st.number_input("Show top N skills", min_value=3, max_value=len(df_skills), value=6, step=1)
    top_df = df_skills.head(int(topn))
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["current"], name="Current"))
    bar_fig.add_trace(go.Bar(x=top_df["skill"], y=top_df["predicted"], name=f"Predicted @ {years} yrs"))
    bar_fig.update_layout(barmode='group', yaxis=dict(range=[0,100]), margin=dict(t=30,b=10))
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# ---------- Timeline & Roles ----------
st.header("Projected Roles & Timeline")
st.markdown(f"**Selected experience:** {years} years")
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
    {"year": 3, "text": "Productionized ML models, containerized pipelines, CI/CD"},
    {"year": 5, "text": "Lead MLOps initiatives, architecture & mentoring"},
]
for t in timeline:
    if years >= t["year"]:
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
        if proj.get("link"):
            st.markdown(f"[Project Link]({proj['link']})")

st.markdown("---")

# ---------- Certifications ----------
st.header("Certifications")
cols = st.columns(3)
for i, cert in enumerate(CERTIFICATIONS):
    with cols[i % 3]:
        st.markdown(f"**{cert['name']}**")
        st.write(cert.get("issuer", ""))
        st.caption(cert.get("date", ""))

st.markdown("---")

# ---------- Footer & Contact ----------
st.markdown("### Contact & Notes")
st.write("LinkedIn: https://www.linkedin.com/in/dhrubo-bhattacharjee/")
st.write("Email: (put your email in data.py if you want it shown)")
st.markdown("----")
st.caption("This is a prototype. Replace 'assets' placeholders with real Lottie JSONs, icons, and profile image files for the full effect.")

# End of app

