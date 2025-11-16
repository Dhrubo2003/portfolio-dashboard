# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from datetime import datetime
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="Dhrubo Bhattacharjee — Future Skills Portfolio",
                   layout="wide",
                   initial_sidebar_state="expanded")

# -------------------------
# Helpers
# -------------------------
def gdrive_direct_url(share_url: str):
    """Convert Google Drive share link to a direct download/viewable URL."""
    if not share_url:
        return None
    try:
        # typical pattern: https://drive.google.com/file/d/<id>/view?usp=sharing
        parts = share_url.split("/")
        if "drive.google.com" in share_url:
            if "file" in parts and "d" in parts:
                idx = parts.index("d")
                file_id = parts[idx + 1]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            # fallback: query param id=
            qs = parse_qs(urlparse(share_url).query)
            if "id" in qs:
                return f"https://drive.google.com/uc?export=download&id={qs['id'][0]}"
    except Exception:
        pass
    return share_url

def make_download_button(link: str, label: str = "Download Resume (PDF)"):
    """Render a stylized top-right resume download button (opens in new tab)."""
    if not link:
        return
    st.markdown(
        f"""
        <div style="display:flex;justify-content:flex-end;">
          <a href="{link}" target="_blank" style="
              background: linear-gradient(90deg,#7b2ff7,#2b86f9);
              color: white;
              padding: 10px 18px;
              border-radius: 10px;
              text-decoration: none;
              font-weight: 600;
              box-shadow: 0 6px 18px rgba(43,134,249,0.22);
              ">
            {label}
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )

def predict_timeline_heuristic(skills: dict, n_projects: int, years: float):
    """
    Lightweight deterministic 'LLM-ish' timeline generator - offline heuristic.
    Returns simple milestones for year 1, 3, 5.
    """
    ml_levels = [v["level"] for k,v in skills.items() if v.get("area") == "ML"]
    devops_levels = [v["level"] for k,v in skills.items() if v.get("area") == "DevOps"]
    ml_score = float(np.mean(ml_levels)) if ml_levels else 0.0
    devops_score = float(np.mean(devops_levels)) if devops_levels else 0.0
    elk_beginner = skills.get("Elasticsearch", {}).get("level", 0) < 40

    milestones = {}
    # Year 1
    if years < 1:
        milestones[1] = "Consolidate ML fundamentals, complete 1–2 production-oriented projects, document reproducible pipelines."
    else:
        milestones[1] = "Solidify ML fundamentals; show production-oriented notebook / dockerized demo."
    # Year 3
    if ml_score >= 60 and devops_score >= 40:
        milestones[3] = "Move to ML Engineer/Data Scientist: productionized models, containerized pipelines, basic CI/CD & monitoring."
    else:
        milestones[3] = "Aim for ML Engineer/Data Scientist: focus on productionization, containerization, and end-to-end pipelines."
    # Year 5
    if devops_score >= 60 and n_projects >= 4:
        milestones[5] = "MLOps Lead: architect ML systems, mentor teams, lead deployments and reliability."
    else:
        milestones[5] = "Senior ML role / path to MLOps Lead: strengthen DevOps & observability skills, lead cross-functional projects."
    if elk_beginner:
        milestones[3] += " (ELK is beginner — add observability and monitoring skills)."
    return milestones

# -------------------------
# Embedded data (from your provided resume & LinkedIn)
# -------------------------
HEADLINE = "ML & Data Analytics | AIML Grad | ELK (Beginner) | Building Predictive Systems"
ABOUT_TEXT = ("AIML graduate skilled in Python, ML modeling and basic ELK configuration. "
              "I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening "
              "DevOps/MLOps competencies to transition from ML Analyst to ML Engineer and, later, MLOps Lead.")

CONTACT = {
    "email": "dhrubob026@gmail.com",
    "github": "https://github.com/Dhrubo2003",
    "phone": "+91-9881453253",
    "linkedin": "https://www.linkedin.com/in/dhrubo-bhattacharjee/"
}

SKILLS = {
    "Python": {"level": 80, "area": "ML"},
    "Machine Learning": {"level": 70, "area": "ML"},
    "Deep Learning": {"level": 65, "area": "ML"},
    "Data Visualization": {"level": 75, "area": "ML"},
    "SQL": {"level": 70, "area": "ML"},
    "PyTorch": {"level": 60, "area": "ML"},
    "TensorFlow": {"level": 50, "area": "ML"},
    "Keras": {"level": 55, "area": "ML"},
    "PowerBI": {"level": 70, "area": "Tool"},
    "Excel": {"level": 75, "area": "Tool"},
    "Looker Studio": {"level": 60, "area": "Tool"},
    "Ansible": {"level": 40, "area": "DevOps"},
    "Elasticsearch": {"level": 30, "area": "DevOps"},  # beginner
    "Logstash": {"level": 30, "area": "DevOps"},
    "Kibana": {"level": 30, "area": "DevOps"},
    "MLOps": {"level": 35, "area": "DevOps"}
}

PROJECTS = [
    {
        "title": "Export-Control-Class-Hierarchy",
        "short_description": "Semantic-ranking application for export control codes using sentence transformers.",
        "long_description": (
            "Developed an application to identify and rank export control codes using the 'stsb-roberta-large' "
            "Sentence Transformer for semantic similarity. Implemented data cleaning, embedding-based retrieval, "
            "and ranking heuristics. Built a lightweight API for recommendations and a tooltip-driven UI for quick code exploration. "
            "Key contribution: a production-ready semantic matching pipeline and a clear UX for domain SMEs."
        ),
        "tech": ["Python", "Sentence-Transformers", "API", "Tooltip UI"],
        "link": "https://github.com/Dhrubo2003/Export-Control-Class-Hierarchy"
    },
    {
        "title": "Real Time System Information & Performance Monitor",
        "short_description": "Desktop monitoring system capturing system metrics and visualizing via PowerBI/SQL.",
        "long_description": (
            "Built a real-time system monitoring tool using psutil to collect CPU, memory, disk, and process metrics. "
            "Persisted metrics into SQL for historical analysis and created PowerBI dashboards for operational monitoring. "
            "Includes scheduling, aggregation, and visual alerting for anomalous system behavior."
        ),
        "tech": ["Python", "psutil", "SQL", "PowerBI"],
        "link": "https://github.com/Dhrubo2003/Desktop-Monitoring-System"
    },
    {
        "title": "Comparative Analysis of GANs for Multispectral Satellite Image Dehazing",
        "short_description": "Comparison of CycleGAN / Pix2Pix / ViT-GAN for multispectral image dehazing.",
        "long_description": (
            "Systematically compared CycleGAN, Pix2Pix, and ViT-based GAN variants on SIH multispectral datasets. "
            "Performed dataset preprocessing, model training, and quantitative evaluation (PSNR/SSIM). "
            "CycleGAN experiments yielded excellent PSNR and SSIM in controlled settings; full repo includes training scripts and visualizations."
        ),
        "tech": ["PyTorch", "GANs", "Image Processing"],
        "link": "https://github.com/Dhrubo2003/GAN-RMFC-Div-A-Comparitive-Analysis-of-GANs-for-Multispectral-Satellite-Image-Dehazing"
    },
    {
        "title": "Sentiment Analysis using Speech Emotion Recognition",
        "short_description": "Audio-based sentiment recognition using CNN/LSTM on RAVDESS (~94% accuracy).",
        "long_description": (
            "Created an end-to-end speech emotion recognition pipeline using audio feature extraction (MFCCs, prosodic features), "
            "augmentation, and CNN+LSTM architectures. Achieved high accuracy on RAVDESS and exported a demo prediction API."
        ),
        "tech": ["Keras/TensorFlow", "Audio Feature Extraction", "CNN/LSTM"],
        "link": "https://github.com/Dhrubo2003/Speech-Emotion-Recognition"
    }
]

CERTIFICATIONS = [
    {"name": "MySQL", "issuer": "", "date": "2023"},
    {"name": "Data Visualization with PowerBI", "issuer": "", "date": "2023"},
    {"name": "Python for Data Science", "issuer": "", "date": "2023"},
    {"name": "Google Data Analytics Certificate", "issuer": "Google / Coursera", "date": "2023"},
]

# Your provided Drive links (kept as requested)
RESUME_SHARE = "https://drive.google.com/file/d/1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E/view?usp=sharing"
PROFILE_IMG_SHARE = "https://drive.google.com/file/d/1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ/view?usp=sharing"

RESUME_LINK = gdrive_direct_url(RESUME_SHARE)
PROFILE_IMG = gdrive_direct_url(PROFILE_IMG_SHARE)

# -------------------------
# Page layout: left column for profile + controls; right for content
# -------------------------
left_col, main_col = st.columns([1, 3])

with left_col:
    # Profile photo, headline, contact, experience slider
    if PROFILE_IMG:
        try:
            st.image(PROFILE_IMG, width=180, caption=None)
        except Exception:
            st.info("Profile image couldn't be loaded from link. Use PNG/JPG under 2MB (~400x400 recommended).")
    else:
        st.info("Add profile image link in the code.")

    st.markdown(f"### <span style='color:#cfcfff'>{'Dhrubo Bhattacharjee'}</span>", unsafe_allow_html=True)
    st.markdown(f"**{HEADLINE}**")
    # Transparent box for about text
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.04);
            padding: 10px;
            border-radius: 8px;
        ">
            <p style="color:#d7dff9;margin:0;">{ABOUT_TEXT}</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("---")
    # Experience slider (1 - 10 years)
    years = st.slider("Total professional experience (years)", min_value=1.0, max_value=10.0, value=1.0, step=0.25)
    st.markdown(f"**Selected experience:** {years} yrs")

    st.markdown("---")
    # Contact quick list and resume button
    st.write(f"**Email:** {CONTACT['email']}")
    st.write(f"**GitHub:** {CONTACT['github']}")
    st.write(f"**LinkedIn:** {CONTACT['linkedin']}")
    st.write(f"**Mobile:** {CONTACT['phone']}")
    make_download_button(RESUME_LINK, label="Download Resume (PDF)")

with main_col:
    # Top KPIs and short chart area (left side removed pie chart)
    k1, k2, k3 = st.columns([1,1,1])
    k1.metric("Role", "Associate Data Scientist → Ready for ML Engineer")
    k2.metric("Projects", len(PROJECTS))
    k3.metric("Certifications", len(CERTIFICATIONS))

    st.markdown("---")

    # Skill Projection (bar + radar) using selected years
    st.header("Skill Projection")
    proj_rows = []
    for name, meta in SKILLS.items():
        base = meta["level"]
        # heuristic target & speed
        if meta.get("area") == "ML":
            target = min(100, base + 30)
            k = 0.6
        elif meta.get("area") == "DevOps":
            target = min(100, base + 40)
            k = 0.5
        else:
            target = min(100, base + 20)
            k = 0.45
        predicted = base + (target - base) * (1 - math.exp(-k * years))
        proj_rows.append({"skill": name, "current": base, "predicted": round(predicted, 1), "area": meta.get("area")})
    proj_df = pd.DataFrame(proj_rows).sort_values("predicted", ascending=False)

    col_a, col_b = st.columns([2,3])
    with col_a:
        st.subheader("Top Skills (predicted)")
        top_n = st.slider("Top N skills to show", min_value=3, max_value=len(proj_df), value=6, key="topn")
        top_df = proj_df.head(int(top_n))
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=top_df["skill"], y=top_df["current"], name="Current"))
        fig_bar.add_trace(go.Bar(x=top_df["skill"], y=top_df["predicted"], name=f"Predicted @ {years} yrs"))
        fig_bar.update_layout(barmode='group', yaxis=dict(range=[0,100]), template="plotly_dark", margin=dict(t=20,b=10))
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_b:
        st.subheader("Detailed Skill Radar")
        cats = top_df["skill"].tolist()
        vals_cur = top_df["current"].tolist()
        vals_pred = top_df["predicted"].tolist()
        if len(cats) >= 3:
            cats_loop = cats + [cats[0]]
            vals_cur_loop = vals_cur + [vals_cur[0]]
            vals_pred_loop = vals_pred + [vals_pred[0]]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals_cur_loop, theta=cats_loop, fill='toself', name='Current'))
            fig.add_trace(go.Scatterpolar(r=vals_pred_loop, theta=cats_loop, fill='toself', name=f'Predicted @ {years} yrs'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), template="plotly_dark", margin=dict(t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Select at least 3 top skills to render radar chart.")

    st.markdown("---")

    # Projects: boxed cards + expanded details
    st.header("Selected Projects")
    for proj in PROJECTS:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(43,134,249,0.04), rgba(123,47,247,0.03));
                border: 1px solid rgba(255,255,255,0.03);
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
            ">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-weight:700;color:#e6e6ff;padding:8px 12px;border-radius:8px;background:rgba(0,0,0,0.18);">
                        {proj['title']}
                    </div>
                    <div style="color:#aab6ff;font-size:13px;">Tech: {', '.join(proj.get('tech',[]))}</div>
                </div>
                <div style="margin-top:8px;color:#d7dff9;">{proj['short_description']}</div>
            </div>
            """, unsafe_allow_html=True)
        with st.expander("Read more / Details"):
            st.write(proj["long_description"])
            st.markdown(f"[Repository]({proj['link']})")

    st.markdown("---")

    # Experience Growth (Cumulative timeline) - updates with slider
    st.header("Experience Growth (Cumulative timeline)")
    # Resume-based approximate durations (as previously estimated)
    milestones = [
        {"label": "Vodafone (end Oct 2022)", "exp": 0.25, "date": "2022-10"},
        {"label": "Aston (end Jul 2023)", "exp": 0.17, "date": "2023-07"},
        {"label": "Dassault (end Nov 2024)", "exp": 0.33, "date": "2024-11"},
        {"label": "Tanex (end Jun 2025)", "exp": 0.50, "date": "2025-06"},
        {"label": "Bristlecone (start Aug 2025)", "exp": 0.28, "date": "2025-11"}
    ]
    # Build cumulative y-values and include the selected slider years as last point (to simulate future)
    cum = 0.0
    xs = []
    ys = []
    labels = []
    for m in milestones:
        cum += m["exp"]
        xs.append(m["date"])
        ys.append(round(cum, 3))
        labels.append(m["label"])
    # Add slider-selected projection point: set final point to max(cum, years)
    xs.append("Selected")
    ys.append(round(max(cum, years), 3))
    labels.append(f"Selected {years} yrs (slider)")

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name="Cumulative experience (years)"))
    fig_line.update_layout(template="plotly_dark", yaxis=dict(title="Years (cumulative)"), margin=dict(t=10,b=10))
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("**Notes:** Cumulative experience is estimated using listed internships and current role. Move the slider (1–10 yrs) to simulate projected cumulative experience.")

    st.markdown("---")

    # Predicted Timeline (heuristic LLM-like)
    st.header("Predicted Timeline (heuristic)")
    milestones_pred = predict_timeline_heuristic(SKILLS, len(PROJECTS), years)
    st.markdown(f"**Based on:** {len(SKILLS)} skills, {len(PROJECTS)} projects, and {years} yrs experience.")
    for yr in sorted(milestones_pred.keys()):
        st.markdown(f"**Year {yr}:** {milestones_pred[yr]}")

    st.markdown("---")

    # Certifications below experience
    st.header("Certifications")
    cols = st.columns(3)
    for i, cert in enumerate(CERTIFICATIONS):
        with cols[i % 3]:
            st.markdown(f"**{cert['name']}**")
            if cert.get("issuer"):
                st.write(cert.get("issuer"))
            st.caption(cert.get("date",""))

    st.markdown("---")
    st.caption("Design: Dark futuristic — replace profile image and resume links with direct links if you prefer. This is a lightweight prototype; we can expand with a small API or real LLM later if desired.")
