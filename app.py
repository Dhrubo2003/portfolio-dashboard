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

# Import project data
from data import PROFILE, SKILLS, PROJECTS, CERTIFICATIONS, HEADLINE, ABOUT_TEXT

st.set_page_config(
    page_title="Dhrubo Bhattacharjee — Future Skills Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Utilities ----------
def load_lottie_file(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def make_download_link(url: str, filename: str = "resume.pdf"):
    return f"[📄 Download Resume]({url})"

# Skill Growth Model
def predict_skill_level(base, max_level, k, p, years):
    years = max(0.0, float(years))
    try:
        growth = (1 - math.exp(-k * years)) ** p
    except Exception:
        growth = 0.0
    return max(0.0, min(100.0, base + (max_level - base) * growth))

def skills_df_for_year(skills_dict, years):
    rows = []
    for skill, meta in skills_dict.items():
        predicted = predict_skill_level(
            float(meta.get("base", 10)),
            float(meta.get("max", 90)),
            float(meta.get("k", 0.5)),
            float(meta.get("p", 1.0)),
            years
        )
        rows.append({
            "skill": skill,
            "current": float(meta.get("base", 10)),
            "predicted": predicted,
            "category": meta.get("category", "Other")
        })
    return pd.DataFrame(rows).sort_values("predicted", ascending=False)

# ---------- Sidebar ----------
with st.sidebar:

    # YOUR GOOGLE DRIVE IMAGE
    st.image(
        "https://drive.google.com/uc?export=view&id=1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ",
        width=140
    )

    st.markdown(f"### {HEADLINE}")
    st.markdown(ABOUT_TEXT)
    st.markdown("---")

    years = st.slider(
        "Project experience (years)",
        min_value=0.0, max_value=10.0, value=1.0, step=0.5,
        help="Slide to simulate future experience."
    )

    st.markdown("**Target Roles:**")
    st.write("- 0–2 yrs: ML Analyst / Junior ML Engineer")
    st.write("- 3 yrs: ML Engineer")
    st.write("- 5+ yrs: MLOps Lead")
    st.markdown("---")

    # YOUR RESUME LINK
    resume_link = "https://drive.google.com/file/d/1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E/view?usp=sharing"
    st.markdown(make_download_link(resume_link))

    st.markdown("---")
    st.caption("Theme: AI / Futuristic dashboard")

# ---------- Top Hero Section ----------
col1, col2 = st.columns([2, 3])

with col1:
    st.title("Dhrubo Bhattacharjee")
    st.subheader(HEADLINE)
    st.write(ABOUT_TEXT)

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Current Experience", "6 months")
    col_kpi2.metric("Projects", len(PROJECTS))
    col_kpi3.metric("Certifications", len(CERTIFICATIONS))

with col2:
    lottie = load_lottie_file(Path("assets/lottie/ai_animation.json"))
    if lottie:
        st_lottie(lottie, height=250)
    else:
        st.image(
            "https://drive.google.com/uc?export=view&id=1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ",
            width=320
        )

st.markdown("---")
