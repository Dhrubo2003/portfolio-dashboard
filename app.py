import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
import base64

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Dhrubo Portfolio Dashboard",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- DARK FUTURISTIC THEME ----------------------
st.markdown("""
    <style>
    body {background-color: #0d0d0d !important;}
    .main {background-color: #0d0d0d !important;}

    /* Transparent Intro Box */
    .glass-box {
        background: rgba(255,255,255,0.06);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(6px);
    }

    /* Project Card */
    .project-card {
        background: rgba(255,255,255,0.05);
        margin: 10px 0px;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
    }

    /* Resume Button */
    .resume-btn {
        background: linear-gradient(90deg,#5b24ff,#9924ff);
        padding: 10px 25px;
        border-radius: 8px;
        color: white !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 16px;
    }

    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
col1, col2 = st.columns([1,3])

with col1:
    if Path("assets/images/profile.png").exists():
        st.image("assets/images/profile.png", width=180)
    else:
        st.warning("Profile image not found at assets/images/profile.png")

with col2:
    st.markdown("<h1 style='color:#bb86fc;'>Dhrubo Bhattacharjee</h1>", unsafe_allow_html=True)
    st.write("📧 **Email:** dhrubob026@gmail.com")
    st.write("📞 **Mobile:** +91-9881453253")
    st.write("💻 **GitHub:** github.com/Dhrubo2003")

    st.markdown("<br>", unsafe_allow_html=True)

    # Resume Download
    resume_link = "https://drive.google.com/file/d/1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E/view?usp=sharing"
    st.markdown(f"<a class='resume-btn' href='{resume_link}' target='_blank'>📄 Download Resume</a>",
                unsafe_allow_html=True)

# ---------------------- ABOUT (Transparent Box) ----------------------
st.markdown("### About Me")
st.markdown("""
<div class="glass-box">
AIML graduate skilled in Python, ML modeling and basic ELK configuration.  
I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening DevOps/MLOps 
competencies to transition from ML Analyst to ML Engineer and, later, MLOps Lead.
</div>
""", unsafe_allow_html=True)

# ---------------------- EXPERIENCE GROWTH CHART ----------------------
st.markdown("## 📈 Experience Growth Over Time")

exp_data = pd.DataFrame({
    "Year": ["2022", "2023", "2024", "2025"],
    "Experience (Months)": [3, 6, 10, 18]
})

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=exp_data["Year"],
    y=exp_data["Experience (Months)"],
    mode="lines+markers",
    line=dict(width=3),
    marker=dict(size=10),
))

fig.update_layout(
    template="plotly_dark",
    title="Total Experience Timeline",
    xaxis_title="Year",
    yaxis_title="Experience (Months)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------- AI-GENERATED FUTURE TIMELINE ----------------------
st.markdown("## 🤖 AI Predicted Career Timeline (Lightweight LLM)")

prompt = """
You are a lightweight model. Predict a realistic, motivational career timeline for an AIML graduate 
with Data Analytics, ML, ELK beginner skills, and DevOps/MLOps learning.

Return in 4-6 bullet points.
"""

try:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {st.secrets['groq_key']}"},
        json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
    )

    timeline_text = response.json()["choices"][0]["message"]["content"]
    st.markdown(f"### 📌 Predicted Path:\n{timeline_text}")

except:
    st.info("LLM key missing in secrets — showing sample output.")
    st.markdown("""
    - Grow into ML Engineer within 1–2 years  
    - Lead ML pipeline automation using MLOps  
    - Develop enterprise-scale AI systems  
    - Become MLOps Lead managing infra + models  
    """)

# ---------------------- PROJECTS SECTION ----------------------
st.markdown("## 🚀 Projects")

projects = [
    {
        "name": "Export-Control-Class-Hierarchy",
        "url": "https://github.com/Dhrubo2003/Export-Control-Class-Hierarchy",
        "details": """
        • Built an AI system using the `stsb-roberta-large` Sentence Transformer  
        • Identifies, ranks, and groups export control codes  
        • Implemented semantic similarity scoring + tooltip UI  
        • Enables fast classification for compliance workflows  
        """
    },
    {
        "name": "Real Time System Information & Performance Monitor",
        "url": "https://github.com/Dhrubo2003/Desktop-Monitoring-System",
        "details": """
        • Uses Psutil to track real-time CPU, RAM, Disk, Network  
        • Stored data into SQL tables for historical analysis  
        • Power BI dashboard created for live performance visualization  
        """
    },
    {
        "name": "Comparative Analysis of GANs for Satellite Image Dehazing",
        "url": "https://github.com/Dhrubo2003/GAN-RMFC-Div-A-Comparitive-Analysis-of-GANs-for-Multispectral-Satellite-Image-Dehazing",
        "details": """
        • Compared CycleGAN, Pix2Pix, and ViT GAN architectures  
        • Worked on SIH Multispectral hazed dataset  
        • Achieved top quality: PSNR 60, SSIM 0.99  
        """
    },
    {
        "name": "Sentiment Analysis using Speech Emotion Recognition",
        "url": "https://github.com/Dhrubo2003/Speech-Emotion-Recognition",
        "details": """
        • Deep learning models (CNN + LSTM) on RAVDESS dataset  
        • Achieved 94% accuracy in speech emotion detection  
        • Advanced MFCC preprocessing pipeline  
        """
    }
]

for p in projects:
    st.markdown(f"""
    <div class="project-card">
        <h4 style='color:#b57bff;'>{p['name']}</h4>
        <p>{p['details']}</p>
        <a href="{p['url']}" target="_blank">🔗 View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)
