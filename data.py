# ============================================================
# data.py  
# Centralized data for your ML-driven portfolio dashboard  
# Author: Dhrubo Bhattacharjee
# ============================================================

# -----------------------------
# BASIC PROFILE INFORMATION
# -----------------------------
PROFILE = {
    "name": "Dhrubo Bhattacharjee",
    "headline": "ML & Data Analytics | AIML Grad | ELK (Beginner) | Building Predictive Systems",
    "about": (
        "AIML graduate skilled in Python, ML modeling and basic ELK configuration. "
        "I build reproducible ML pipelines, dashboards, and data-driven systems. "
        "Focused on expanding DevOps/MLOps competencies to transition from ML Analyst "
        "to ML Engineer and ultimately an MLOps Lead."
    ),
    "linkedin": "https://www.linkedin.com/in/dhrubo-bhattacharjee/",
    "resume_link": "paste-your-google-drive-resume-link-here"
}

# -----------------------------
# SKILLS (Current Levels)
# Scale: 1–10
# -----------------------------
SKILLS = {
    "Python": 8,
    "Machine Learning": 7,
    "Data Analysis": 8,
    "Deep Learning": 6,
    "Pandas / Numpy": 8,
    "ELK Stack (Beginner)": 3,
    "Logstash": 2,
    "Kibana": 3,
    "Elasticsearch": 3,
    "Docker": 4,
    "Git / GitHub": 7,
    "SQL": 7,
    "Streamlit": 8,
    "APIs & Automation": 7,
    "Model Deployment": 5
}

# -----------------------------
# FUTURE SKILL GROWTH MODEL INPUT  
# Used by your ML model in app.py  
# -----------------------------
FUTURE_SKILL_TARGETS = {
    # expected skill level after 3 years
    "year_3": {
        "Python": 9,
        "Machine Learning": 9,
        "MLOps": 7,
        "Docker": 7,
        "Kubernetes": 6,
        "Deep Learning": 8,
        "Data Engineering": 7,
        "ELK Stack": 6
    },
    # expected skill level after 5 years
    "year_5": {
        "Python": 9,
        "Machine Learning": 10,
        "MLOps": 9,
        "Docker": 9,
        "Kubernetes": 8,
        "Deep Learning": 9,
        "Data Engineering": 8,
        "ELK Stack": 8,
        "Architecting ML Systems": 7
    }
}

# -----------------------------
# CERTIFICATIONS
# -----------------------------
CERTIFICATIONS = [
    {
        "title": "Artificial Intelligence & Machine Learning",
        "issuer": "University / Program",
        "year": "2024"
    },
    # Add more manually here when needed
]

# -----------------------------
# PROJECTS
# -----------------------------
PROJECTS = [
    {
        "name": "Flight & Weather Prediction Dashboard",
        "description": (
            "Built a Streamlit-based predictive system that analyzes relationships "
            "between real-time flight metrics and European weather conditions."
        ),
        "tech": ["Python", "Streamlit", "APIs", "ML Models"],
        "role": "Built data pipeline + prediction logic + dashboard"
    },
    {
        "name": "ELK Stack Setup & Automation",
        "description": (
            "Automated ELK installation on multiple CentOS VMs using Ansible. "
            "Configured Elasticsearch, Logstash, and Kibana for data ingestion and visualization."
        ),
        "tech": ["ELK", "Ansible", "Linux", "VM Setup"],
        "role": "Full setup, automation & debugging"
    },
    {
        "name": "ML Model Pipeline",
        "description": (
            "Implemented ML models with feature engineering, evaluation, "
            "and reproducible pipeline structure."
        ),
        "tech": ["Scikit-Learn", "Python", "EDA"],
        "role": "Model development & optimization"
    }
]

# -----------------------------
# TIMELINE / CAREER PROGRESSION
# -----------------------------
CAREER_TIMELINE = [
    {"year": "2023", "event": "Completed AIML Graduation"},
    {"year": "2024", "event": "Developed ML/ELK beginner projects"},
    {"year": "2025", "event": "Working on predictive systems and ML dashboards"},
    {"year": "2027 (Projected)", "event": "ML Engineer"},
    {"year": "2029 (Projected)", "event": "MLOps Lead"},
]

# -----------------------------
# FUTURE ROLES (Based on Experience Slider)
# -----------------------------
FUTURE_ROLES = {
    "0-1": "ML Analyst / Data Analyst",
    "2-3": "Machine Learning Engineer",
    "4-5": "Senior ML Engineer / MLOps Engineer",
    "6-8": "MLOps Lead / Data Platform Engineer",
    "9-10": "AI Systems Architect"
}

# -----------------------------
# LOTTIE ANIMATIONS (placeholders)
# -----------------------------
LOTTIE_LINKS = {
    "hero_animation": "paste-lottie-link-here",
    "skills_animation": "paste-lottie-link-here",
    "projects_animation": "paste-lottie-link-here"
}
