# data.py
# Central data file for your Streamlit AI-themed portfolio dashboard.

# ---------------- PROFILE TEXT ----------------

HEADLINE = "ML & Data Analytics | AIML Grad | ELK (Beginner) | Building Predictive Systems"

ABOUT_TEXT = (
    "AIML graduate skilled in Python, ML modeling and basic ELK configuration. "
    "I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening "
    "DevOps/MLOps competencies to transition from ML Analyst to ML Engineer and, later, MLOps Lead."
)

PROFILE = {
    "name": "Dhrubo Bhattacharjee",
    "email": "paste your email here",
    "linkedin": "https://www.linkedin.com/in/dhrubo-bhattacharjee/",
}

# ---------------- SKILLS ----------------
# base = current level (0–100), max = future max, k & p = growth curve shape

SKILLS = {
    # --- Machine Learning ---
    "Python": {"base": 65, "max": 95, "k": 0.55, "p": 1.1, "category": "ML"},
    "Machine Learning": {"base": 55, "max": 92, "k": 0.48, "p": 1.2, "category": "ML"},
    "Deep Learning": {"base": 40, "max": 90, "k": 0.42, "p": 1.3, "category": "ML"},
    "Data Visualization": {"base": 60, "max": 90, "k": 0.50, "p": 1.1, "category": "ML"},
    "Pandas / Numpy": {"base": 70, "max": 95, "k": 0.55, "p": 1.1, "category": "ML"},
    "Scikit-Learn": {"base": 55, "max": 90, "k": 0.50, "p": 1.2, "category": "ML"},

    # --- ELK Stack (Beginner as you said) ---
    "Elasticsearch": {"base": 20, "max": 80, "k": 0.45, "p": 1.15, "category": "ELK"},
    "Logstash": {"base": 20, "max": 80, "k": 0.45, "p": 1.15, "category": "ELK"},
    "Kibana": {"base": 25, "max": 82, "k": 0.45, "p": 1.15, "category": "ELK"},

    # --- DevOps / MLOps Path ---
    "Docker": {"base": 20, "max": 85, "k": 0.50, "p": 1.25, "category": "MLOps"},
    "Git/GitHub": {"base": 60, "max": 90, "k": 0.55, "p": 1.1, "category": "MLOps"},
    "Linux/CLI": {"base": 40, "max": 88, "k": 0.48, "p": 1.2, "category": "MLOps"},
    "MLOps": {"base": 20, "max": 95, "k": 0.50, "p": 1.3, "category": "MLOps"},
}

# ---------------- PROJECTS (College + Others) ----------------

PROJECTS = [
    {
        "title": "Flight–Weather Prediction System (Dashboard + ML)",
        "short_description": "A predictive ML system analyzing European flight & weather data with real-time APIs, visualization dashboards, and automated ETL.",
        "long_description": (
            "Developed a Streamlit-based prediction system integrating real-time flight APIs, weather APIs, and "
            "data preprocessing. Designed ML models to analyze how atmospheric conditions affect flight delays. "
            "Built dashboards and automation pipelines for continuous updates."
        ),
        "tech": ["Python", "Streamlit", "APIs", "ML", "Weather/Flight Data"],
        "link": ""
    },
    {
        "title": "ELK Stack Setup with Ansible (Automation Project)",
        "short_description": "Automated Elasticsearch + Logstash + Kibana deployment on multiple CentOS VMs using Ansible.",
        "long_description": (
            "Configured Ansible playbooks to deploy and manage the ELK stack across several CentOS-based VMs. "
            "Automated setups included Elasticsearch clusters, Logstash ETL pipelines, and Kibana dashboards. "
            "This project improved observability and log analytics automation."
        ),
        "tech": ["Ansible", "Elasticsearch", "Logstash", "Kibana", "CentOS"],
        "link": ""
    },
    {
        "title": "ML College Projects (AIML Degree)",
        "short_description": "Multiple ML-focused academic projects involving supervised learning, data visualization, and model evaluation.",
        "long_description": (
            "Coursework included implementation of regression, classification, ensemble learning, and clustering "
            "algorithms. Built end-to-end ML pipelines, performed exploratory data analysis, and validated models "
            "using modern metrics."
        ),
        "tech": ["Python", "ML", "Pandas", "EDA"],
        "link": ""
    }
]

# ---------------- CERTIFICATIONS ----------------

CERTIFICATIONS = [
    {
        "name": "Artificial Intelligence & Machine Learning (AIML) Degree",
        "issuer": "Your University / Institute",
        "date": "Year of Completion"
    },
    {
        "name": "Python for Data Science (College Coursework / Specialization)",
        "issuer": "Institute / Online Platform",
        "date": "Completion Year"
    },
    {
        "name": "Machine Learning Foundations",
        "issuer": "Institute / Online Platform",
        "date": "Completion Year"
    }
]

