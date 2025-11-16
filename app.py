import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# ----------------------------- #
#   PAGE CONFIG
# ----------------------------- #
st.set_page_config(
    page_title="Dhrubo Portfolio",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------- #
#   SIDEBAR (PHOTO + INFO)
# ----------------------------- #
with st.sidebar:
    st.image("assets/images/profile.png", width=180)

    st.markdown("""
        ### **Dhrubo Bhattacharjee**
        AIML Graduate  
        Associate Data Scientist  
        Pune, India  
        **Email:** dhrubob026@gmail.com  
        **GitHub:** github.com/Dhrubo2003  
        **Mobile:** +91-9881453253  
    """)

    # Transparent summary box
    st.markdown("""
    <div style="padding:10px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);">
        AIML graduate skilled in Python, ML modeling and basic ELK configuration.  
        I deliver reproducible ML pipelines and dashboards, and I’m focused on 
        strengthening DevOps/MLOps competencies to transition from  
        **ML Analyst → ML Engineer → MLOps Lead**.
    </div>
    """, unsafe_allow_html=True)

    # Download resume button
    resume_url = "https://drive.google.com/uc?export=download&id=1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E"
    st.markdown(
        f"""
        <a href="{resume_url}" target="_blank">
            <div style="
                margin-top:15px;
                padding:10px 15px;
                background:#6C63FF;
                color:white;
                text-align:center;
                border-radius:10px;
                font-weight:600;
                ">
                ⬇ Download Resume
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

# ----------------------------- #
#   MAIN SECTION
# ----------------------------- #
st.title("🚀 Portfolio Dashboard (Dark Futuristic)")

# ------------------------------------------ #
# EXPERIENCE GROWTH LINE CHART - TOP RIGHT
# ------------------------------------------ #

st.subheader("📈 Experience Growth Over Time")

# Experience Timeline (months)
experience = {
    "Role": [
        "Vodafone (VOIS)", 
        "GGP-PAAI Research",
        "Dassault Systemes",
        "Tanex Solutions",
        "Bristlecone"
    ],
    "Start": [
        "2022-08", 
        "2023-05", 
        "2024-08", 
        "2025-01", 
        "2025-08"
    ],
    "End": [
        "2022-10",
        "2023-07",
        "2024-11",
        "2025-06",
        datetime.now().strftime("%Y-%m")
    ]
}

df_exp = pd.DataFrame(experience)
df_exp["Start"] = pd.to_datetime(df_exp["Start"])
df_exp["End"] = pd.to_datetime(df_exp["End"])
df_exp["Months"] = (df_exp["End"] - df_exp["Start"]).dt.days // 30

df_exp["Cumulative Experience (Months)"] = df_exp["Months"].cumsum()

fig_exp = px.line(
    df_exp,
    x="Role",
    y="Cumulative Experience (Months)",
    markers=True,
    title="Experience Timeline Growth",
)

fig_exp.update_traces(line=dict(width=3))

st.plotly_chart(fig_exp, use_container_width=True)

# ---------------------------------------------- #
#   LLM PREDICTED CAREER TIMELINE
# ---------------------------------------------- #

st.subheader("🤖 AI Predicted Career Growth Timeline")

timeline_predictions = [
    "2026 → ML Engineer",
    "2028 → Senior ML Engineer",
    "2030 → MLOps Lead",
    "2032 → Principal AI/MLOps Architect"
]

for item in timeline_predictions:
    st.markdown(f"🔮 **{item}**")

# ---------------------------------------------- #
# PROJECTS WITH EXPANDED DETAILS + GITHUB
# ---------------------------------------------- #

st.subheader("📂 Featured Projects")

projects = [
    {
        "name": "Export-Control-Class-Hierarchy",
        "url": "https://github.com/Dhrubo2003/Export-Control-Class-Hierarchy",
        "details": """
        Designed an intelligent system using **STSB-RoBERTa-Large** to compute semantic similarity  
        between export control codes.  
        Built a tooltip-based UI to improve classification clarity.  
        Increased classification accuracy using contextual embeddings.
        """
    },
    {
        "name": "Real Time System Information & Performance Monitor",
        "url": "https://github.com/Dhrubo2003/Desktop-Monitoring-System",
        "details": """
        Built a real-time PC monitoring dashboard using **Psutil**, Python + SQL  
        and visualized system metrics in PowerBI.  
        Automated dataset generation for long-running analysis.
        """
    },
    {
        "name": "Comparative Analysis of GANs for Satellite Image Dehazing",
        "url": "https://github.com/Dhrubo2003/GAN-RMFC-Div-A-Comparitive-Analysis-of-GANs-for-Multispectral-Satellite-Image-Dehazing",
        "details": """
        Evaluated **CycleGAN, Pix2Pix, ViT-GAN** for multispectral image dehazing.  
        Achieved **PSNR=60** and **SSIM=0.99** with CycleGAN.  
        Processed high-res satellite data from Government of India SIH Dataset.
        """
    },
    {
        "name": "Speech Emotion Recognition",
        "url": "https://github.com/Dhrubo2003/Speech-Emotion-Recognition",
        "details": """
        Used **RAVDESS Dataset**, CNN + LSTM models to classify emotions from speech.  
        Reached **94% accuracy** using mel-spectrogram preprocessing.  
        Built dataset augmentation & noise-handling pipeline.
        """
    }
]

for p in projects:
    st.markdown(
        f"""
        <div style="padding:12px; margin-bottom:15px; border-radius:12px; 
        background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);">
            <h4 style="margin:0; color:#8AB4F8;">📘 {p['name']}</h4>
            <p>{p['details']}</p>
            <a href="{p['url']}" target="_blank">🔗 View on GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )
