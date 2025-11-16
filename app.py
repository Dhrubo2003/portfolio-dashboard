import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Dhrubo Portfolio Dashboard",
    layout="wide"
)

# -----------------------------
# HEADER SECTION
# -----------------------------
st.title("👨‍💻 Dhrubo Bhattacharjee – ML & Analytics Portfolio")

profile_pic_url = "https://drive.google.com/uc?export=view&id=YOUR_FILE_ID"

col1, col2 = st.columns([1, 3])

with col1:
    st.image(profile_pic_url, width=180)

with col2:
    st.subheader("ML & Data Analytics | AIML Grad | ELK (Beginner)")
    st.write(
        """
        AIML graduate skilled in Python, ML modeling and beginner-level ELK configuration.  
        I deliver reproducible ML pipelines and dashboards, and I’m focused on strengthening  
        DevOps/MLOps competencies to grow into an ML Engineer and later an MLOps Lead.
        """
    )
    st.download_button("📄 Download Resume", "resume.pdf", file_name="Dhrubo_Resume.pdf")

st.write("---")

# -----------------------------
# AGE-BASED FUTURE SKILL PREDICTOR
# -----------------------------

st.header("📈 Future Skill Projection (ML-based Mock Model)")

current_age = 22        # change this if needed
age = st.slider("Select Age", min_value=current_age, max_value=current_age + 10, value=current_age)

base_skills = {
    "Python": 80,
    "Machine Learning": 70,
    "Data Analytics": 75,
    "ELK Stack": 40,
    "MLOps": 30,
}

# Simple growth model (each year improves skills)
growth_per_year = {
    "Python": 2,
    "Machine Learning": 3,
    "Data Analytics": 2,
    "ELK Stack": 4,
    "MLOps": 5,
}

years_difference = age - current_age

predicted = {skill: base_skills[skill] + growth_per_year[skill] * years_difference
             for skill in base_skills}

df_skills = pd.DataFrame({
    "Skill": list(predicted.keys()),
    "Proficiency": list(predicted.values())
})

chart = (
    alt.Chart(df_skills)
    .mark_bar()
    .encode(
        x=alt.X("Proficiency:Q", title="Skill Level (%)"),
        y=alt.Y("Skill:N", sort="-x"),
        tooltip=["Skill", "Proficiency"]
    )
    .properties(height=300)
)

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# PROJECTS SECTION
# -----------------------------
st.header("🚀 Projects")

projects = {
    "Real-time Flight Weather Prediction System": "Built using APIs, Streamlit, and ML.",
    "Customer Churn ML Model": "Logistic Regression + Dashboards.",
    "ELK Stack Log Monitoring (Beginner)": "Setting up Elasticsearch/Kibana for logs.",
}

for name, desc in projects.items():
    st.markdown(f"### 🔹 {name}")
    st.write(desc)

# -----------------------------
# CERTIFICATIONS
# -----------------------------
st.header("🎓 Certifications")

certs = [
    "AIML Graduate Certificate",
    "Python for Data Science",
    "Machine Learning Specialization",
]

st.write("\n".join([f"- {c}" for c in certs]))

# -----------------------------
# CONTACT
# -----------------------------
st.write("---")
st.subheader("📬 Contact")
st.write("📧 bhattacharjeedhrubo544@gmail.com")
st.write("[LinkedIn Profile](https://www.linkedin.com/in/dhrubo-bhattacharjee/)")

