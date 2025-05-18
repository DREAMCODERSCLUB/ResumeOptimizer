import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

import streamlit as st
import pdfplumber

# ---- PAGE SETUP ----
st.set_page_config(page_title="GenAI Resume Optimizer", layout="centered")

st.title("📄 GenAI Resume Optimizer")
st.markdown("Tailor your resume for any job — powered by Gemini 1.5 Flash.")

# ---- INPUT: RESUME UPLOAD ----
st.subheader("1️⃣ Upload Your Resume")
resume_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])

resume_text = ""
if resume_file:
    if resume_file.type == "application/pdf":
        with pdfplumber.open(resume_file) as pdf:
            for page in pdf.pages:
                resume_text += page.extract_text() + "\n"
    elif resume_file.type == "text/plain":
        resume_text = resume_file.read().decode("utf-8")
    else:
        st.error("Unsupported file format")

if resume_text:
    st.success("✅ Resume uploaded and parsed successfully!")
    with st.expander("🔍 View Parsed Resume Text"):
        st.text_area("Parsed Resume", resume_text, height=250)

# ---- INPUT: JOB DESCRIPTION ----
st.subheader("2️⃣ Paste Job Description")
job_description = st.text_area("Paste the job description here", height=200)

# ---- PROCESS BUTTON ----
optimized_resume = None

if st.button("⚡ Optimize Resume"):
    if resume_text and job_description:
        prompt = f"""You are a resume consultant. Given a resume and job description, optimize the resume to fit the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Now, return the optimized resume text.
"""
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            optimized_resume = response.text.strip()

            st.subheader("🔍 Optimized Resume Output")
            st.text_area("Optimized Resume", optimized_resume, height=300)

            # ---- DOWNLOAD BUTTON ----
            st.download_button(
                label="⬇️ Download Optimized Resume",
                data=optimized_resume,
                file_name="optimized_resume.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
    else:
        st.warning("Please upload a resume and paste a job description.")

# ---- FOOTER ----
st.markdown("---")
st.caption("Built by Chirag Sharma | Powered by Gemini 1.5 Flash")
