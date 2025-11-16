# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="Dhrubo Bhattacharjee — Future Skills Portfolio",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   page_icon=":bar_chart:")

# -------------------------
# Helpers
# -------------------------
def gdrive_direct_url(share_url: str):
    """
    Convert Google Drive share link to a direct 'uc?export=download&id=ID' url
    Example: https://drive.google.com/file/d/<ID>/view?usp=sharing
    """
    if not share_url:
        return None
    try:
        parts = share_url.split('/')
        if "drive.google.com" in share_url:
            if "file" in parts and "d" in parts:
                idx = parts.index("d")
                file_id = parts[idx + 1]
                return f"https://drive.google.com/uc?export=download&id={file_id}"
            qs = parse_qs(urlparse(share_url).query)
            if "id" in qs:
                return f"https://drive.google.com/uc?export=download&id={qs['id'][0]}"
    except Exception:
        pass
    return share_url

def make_download_button(link: str, label: str = "Download Resume (PDF)"):
    """Render a top-right styled download button (opens link in new tab)."""
    if not link:
        return
    st.markdown(
        f"""
        <div style="display:flex;justify-content:flex-end;margin-top:6px;">
          <a href="{link}" target="_blank" style="
              background: linear-gradient(90deg,#7b2ff7,#2b86f9);
              color: white;
              padding: 10px 18px;
              border-radius: 10px;
              text-decoration: none;
              font-weight: 700;
              box-shadow: 0 6px 20px rgba(43,134,249,0.22);
              ">
            {label}
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )

def predict_timeline_heuristic(skills: dict, n_projects: int, years: float):
    """
    Lightweight deterministic heuristic that generates short predicted milestones
    for 1 / 3 / 5 years based on provided skills and projects.
    """
    ml_levels = [v["level"] for k, v in skills.items() if v.get("area") == "ML"]
    dev_levels = [v["level"] for k, v in skills.items() if v.get("area") == "DevOps"]
    ml_score = np.mean(ml_levels) if ml_levels else 0
    dev_score = np.mean(dev_levels) if dev_levels else 0
    elk_beginner = skills.get("Elasticsearch", {}).get("level", 0) < 40

    milestones = {}
    # Year 1
    if years < 1:
        milestones[1] = "Focus on production-ready code, reproducible pipelines, and 1-2 production-oriented demos."
    else:
        milestones[1] = "Strengthen ML fundamentals, reproducible pipelines and CI basics; deliver production demos."
    # Year 3
    if ml_score >= 60 and dev_score >= 35:
        milestones[3] = "Move to ML Engineer: containerized models, CI/CD, monitoring & model deployment experience."
    else:
        milestones[3] = "Transition to ML Engineer by focusing on productionization, containerization and monitoring."
    # Year 5
    if dev_score >= 60 and n_projects >= 4:
        milestones[5] = "MLOps Lead: lead deployments, own infra & best practices, mentor teams and design ML platforms."
    else:
        milestones[5] = "Senior ML role with strong production ownership; aim for MLOps leadership with targeted DevOps upskilling."
    if elk_beginner:
        milestones[3] += " (Tip: strengthen ELK/observability skills to complement MLOps growth.)"
    return milestones

# -------------------------
# Embedded data (from your resume / LinkedIn inputs)
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
            "Sentence Transformer for semantic similarity. Implemented preprocessing, semantic matching, and a tooltip-based "
            "UI to present ranked code recommendations. Main contributions: designing semantic-matching pipeline, "
            "creating a lightweight API for recommendations, and building the front-end tooltip interface for easy navigation. "
            "See repo for architecture diagrams, sample inputs and evaluation notes."
        ),
        "tech": ["Python", "Sentence-Transformers", "Flask/FastAPI", "JS tooltip UI"],
        "link": "https://github.com/Dhrubo2003/Export-Control-Class-Hierarchy"
    },
    {
        "title": "Real Time System Information & Performance Monitor",
        "short_description": "Desktop monitoring system capturing system metrics and visualizing via PowerBI/SQL.",
        "long_description": (
            "Built a real-time system monitoring tool using psutil to collect CPU, memory, disk, and process metrics. "
            "Persisted metrics into a SQL database for historical analysis and created PowerBI dashboards for dynamic visualization. "
            "The repo contains collection scripts, schema designs, and example PowerBI reports used for operations dashboards."
        ),
        "tech": ["Python", "psutil", "MySQL/SQLite", "PowerBI"],
        "link": "https://github.com/Dhrubo2003/Desktop-Monitoring-System"
    },
    {
        "title": "Comparative Analysis of GANs for Multispectral Satellite Image Dehazing",
        "short_description": "Empirical comparison of CycleGAN / Pix2Pix / ViT-GAN for multispectral image dehazing.",
        "long_description": (
            "Performed a systematic comparison of GAN variants (CycleGAN, Pix2Pix, ViT-based GAN) on SIH multispectral datasets for image dehazing. "
            "Included extensive preprocessing, training pipelines, metric evaluation (PSNR/SSIM), and visual qualitative comparisons. "
            "CycleGAN experiments reached PSNR ~60 and SSIM ~0.99 in controlled settings — details, training logs and sample outputs in the repo."
        ),
        "tech": ["PyTorch", "GANs", "Image preprocessing", "PSNR/SSIM"],
        "link": "https://github.com/Dhrubo2003/GAN-RMFC-Div-A-Comparitive-Analysis-of-GANs-for-Multispectral-Satellite-Image-Dehazing"
    },
    {
        "title": "Sentiment Analysis using Speech Emotion Recognition",
        "short_description": "SER pipeline using CNN/LSTM on RAVDESS dataset; achieved ~94% accuracy.",
        "long_description": (
            "Built a speech emotion recognition pipeline using audio preprocessing (MFCCs, prosodic features), CNN+LSTM models, "
            "and augmentation. Trained and evaluated on the RAVDESS dataset, attaining ~94% accuracy for the target classes. "
            "Repo includes preprocessing notebooks, model training scripts and sample inference APIs."
        ),
        "tech": ["Python", "Keras/TensorFlow", "Audio feature extraction", "CNN/LSTM"],
        "link": "https://github.com/Dhrubo2003/Speech-Emotion-Recognition"
    }
]

CERTIFICATIONS = [
    {"name": "MySQL", "issuer": "", "date": "2023"},
    {"name": "Data Visualization with PowerBI", "issuer": "", "date": "2023"},
    {"name": "Python for Data Science", "issuer": "", "date": "2023"},
    {"name": "Google Data Analytics Certificate", "issuer": "Google / Coursera", "date": "2023"},
]

# Put your google drive links (share links). We convert to direct download for image display.
RESUME_SHARE = "https://drive.google.com/file/d/1HGv8HNeWkTYRu4DqXRjFXntwRt52HM3E/view?usp=sharing"
PROFILE_IMG_SHARE = "https://drive.google.com/file/d/1GcoDLu9Pm_pHfe6NOs3SGTltVT_F1qHJ/view?usp=sharing"

RESUME_LINK = RESUME_SHARE
PROFILE_IMG = gdrive_direct_url(PROFILE_IMG_SHARE)

# -------------------------
# Page UI (keeps layout you approved)
# -------------------------
# Header + profile
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(f"<h1 style='margin:0;color:#E6E6FA'>Dhrubo Bhattacharjee</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-top:6px;color:#9EA7FF'>{HEADLINE}</h3>", unsafe_allow_html=True)
    # Transparent about box
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.04);
            padding: 12px;
            border-radius: 10px;
            max-width: 900px;
            margin-top:8px;
        ">
            <p style="color:#d7dff9;margin:0;">{ABOUT_TEXT}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    if PROFILE_IMG:
        try:
            st.image(PROFILE_IMG, width=180)
        except Exception:
            st.info("Profile image could not be loaded from the provided link. Use PNG/JPG under ~2MB and ~400x400px resolution.")
    else:
        st.info("Add your profile image link in the code (PROFILE_IMG_SHARE).")

# Resume button (top)
make_download_button(RESUME_LINK, label="Download Resume (PDF)")

st.markdown("---")

# Experience slider (years)
years = st.slider("Total professional experience (years)", min_value=0.0, max_value=10.0, value=1.0, step=0.25)

# KPI + donut mini-chart (attractive small chart beside name)
k1, k2, k3, k4 = st.columns([1,1,1,2])
k1.metric("Experience", f"{years} yrs")
k2.metric("Projects", len(PROJECTS))
k3.metric("Certifications", len(CERTIFICATIONS))

skill_df = pd.DataFrame([{"skill": k, "level": SKILLS[k]["level"], "area": SKILLS[k].get("area","Other")} for k in SKILLS])
area_avg = skill_df.groupby("area")["level"].mean().reset_index()
fig_donut = go.Figure(go.Pie(labels=area_avg["area"], values=area_avg["level"], hole=0.6))
fig_donut.update_layout(showlegend=True, margin=dict(t=5,b=5,l=10,r=10), template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
with k4:
    st.plotly_chart(fig_donut, use_container_width=True, height=160)

st.markdown("---")

# Skill projection (bar + radar) — improved details
st.header("Skill Projection")
def predict_skill(base, target, k, years):
    return base + (target - base) * (1 - math.exp(-k * years))

proj_rows = []
for name, meta in SKILLS.items():
    base = meta["level"]
    if meta.get("area") == "ML":
        target = min(100, base + 30)
        k = 0.6
    elif meta.get("area") == "DevOps":
        target = min(100, base + 40)
        k = 0.45
    else:
        target = min(100, base + 20)
        k = 0.5
    predicted = predict_skill(base, target, k, years)
    proj_rows.append({"skill": name, "current": base, "predicted": round(predicted,2), "area": meta.get("area")})
proj_df = pd.DataFrame(proj_rows).sort_values("predicted", ascending=False)

col_a, col_b = st.columns([2,3])
with col_a:
    st.subheader("Top Skills (predicted)")
    top_n = st.slider("Top N skills to show", min_value=3, max_value=len(proj_df), value=6, key="topn")
    top_df = proj_df.head(top_n)
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
    if len(cats) >= 1:
        cats_loop = cats + [cats[0]]
        vals_cur_loop = vals_cur + [vals_cur[0]]
        vals_pred_loop = vals_pred + [vals_pred[0]]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=vals_cur_loop, theta=cats_loop, fill='toself', name='Current'))
        fig.add_trace(go.Scatterpolar(r=vals_pred_loop, theta=cats_loop, fill='toself', name=f'Predicted @ {years} yrs'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), template="plotly_dark", margin=dict(t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Experience Growth line chart (detailed)
st.header("Experience Growth (Cumulative timeline)")
milestones = [
    {"label": "Vodafone (end Oct 2022)", "exp": 0.25, "date": "2022-10"},
    {"label": "Aston (end Jul 2023)", "exp": 0.17, "date": "2023-07"},
    {"label": "Dassault (end Nov 2024)", "exp": 0.33, "date": "2024-11"},
    {"label": "Tanex (end Jun 2025)", "exp": 0.50, "date": "2025-06"},
    {"label": "Bristlecone (start Aug 2025)", "exp": 0.28, "date": "2025-11"}
]
cum = 0.0
xs = []
ys = []
for m in milestones:
    cum += m["exp"]
    xs.append(m["date"])
    ys.append(round(cum, 3))
xs.append("Selected")
ys.append(round(max(cum, years), 3))
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers+text", text=[str(y) for y in ys], textposition="top center", name="Cumulative experience"))
fig_line.update_layout(template="plotly_dark", yaxis=dict(title="Years (cumulative)"), margin=dict(t=10,b=10))
st.plotly_chart(fig_line, use_container_width=True)
st.markdown("**Explanation:** cumulative experience is estimated from listed internships and current role. Chart labels show the cumulative years at each milestone.")

st.markdown("---")

# Predicted Timeline (lightweight LLM-ish heuristic)
st.header("Predicted Timeline (heuristic)")
milestones_pred = predict_timeline_heuristic(SKILLS, len(PROJECTS), years)
st.markdown(f"**Based on:** {len(SKILLS)} skills, {len(PROJECTS)} projects, and {years} yrs experience.")
for yr in sorted(milestones_pred.keys()):
    st.markdown(f"**Year {yr}:** {milestones_pred[yr]}")

st.markdown("---")

# Projects (boxed cards with longer details + repo link)
st.header("Selected Projects")
for proj in PROJECTS:
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(43,134,249,0.06), rgba(123,47,247,0.04));
            border: 1px solid rgba(255,255,255,0.04);
            padding:12px;
            border-radius:10px;
            margin-bottom:10px;
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-weight:700;color:#e6e6ff;padding:8px 12px;border-radius:8px;background:rgba(0,0,0,0.15);">
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

# Certifications & Contact
st.header("Certifications & Contact")
cols = st.columns(3)
for i, cert in enumerate(CERTIFICATIONS):
    with cols[i % 3]:
        st.markdown(f"**{cert['name']}**")
        st.write(cert.get("issuer", ""))
        st.caption(cert.get("date", ""))

st.markdown("---")
st.write("**Contact**")
st.write(f"- Email: {CONTACT['email']}")
st.write(f"- GitHub: {CONTACT['github']}")
st.write(f"- LinkedIn: {CONTACT['linkedin']}")
st.write(f"- Mobile: {CONTACT['phone']}")
st.caption("Design: Dark Futuristic (neon/cyber look). Replace profile image and resume links with direct links if needed.")
