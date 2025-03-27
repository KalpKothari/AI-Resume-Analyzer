import streamlit as st
import os
import fitz  # PyMuPDF for PDF text extraction
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to interact with Gemini API for ATS analysis
def ask_gemini_query(job_desc, resume_text, analysis_type):
    prompt_templates = {
        "ATS Score": "Analyze the resume against the job description and provide an ATS score (0-100%).",
        "Strengths & Weaknesses": "Analyze the resume for strengths and weaknesses compared to the job description.",
        "Missing Keywords": "List important keywords missing from the resume that are present in the job description.",
        "Course Suggestions": "Suggest 3-5 online courses that can help the candidate improve their skills based on the missing qualifications in the resume."
    }
    
    prompt = f"{prompt_templates[analysis_type]}\n\nJob Description:\n{job_desc}\n\nResume:\n{resume_text}"
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text  # Extract AI-generated text

# Function to interact with Gemini API for "Ask Query" feature
def ask_gemini_general_query(query_text, resume_text, job_desc):
    prompt = f"""
    You are an AI assistant helping with resume and job applications.
    
    Here is the Job Description:
    {job_desc}
    
    Here is the Resume:
    {resume_text}
    
    Question: {query_text}
    
    Answer in a helpful and detailed manner based on the provided job description and resume.
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text

# Function to extract text from uploaded PDF resume
def extract_text_from_pdf(uploaded_file):
    document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return " ".join([page.get_text() for page in document])

# Streamlit UI Configuration
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("📄 AI Resume Analyzer")
st.subheader("Analyze your resume, get ATS score, and find course recommendations!")

# User Inputs
job_description = st.text_area("📌 Enter Job Description:", height=150)
uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF)", type=["pdf"])

# Extract resume text if uploaded
resume_text = ""
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume Uploaded Successfully")

# Analysis Options
st.subheader("📝 Choose What to Analyze:")
analysis_option = st.radio("Select an option:", [
    "ATS Score",
    "Strengths & Weaknesses",
    "Missing Keywords",
    "Course Suggestions"
])

# Ask Query Feature
st.subheader("❓ Ask Any Query:")
query_text = st.text_area("Enter your question related to resume/job search:")

# Analyze Resume Button
if st.button("🔍 Analyze Resume"):
    if uploaded_file and job_description:
        response = ask_gemini_query(job_description, resume_text, analysis_option)
        st.subheader("📊 AI Response:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")

# Ask Query Button
if st.button("💬 Ask Query"):
    if query_text and uploaded_file and job_description:
        response = ask_gemini_general_query(query_text, resume_text, job_description)
        st.subheader("🤖 AI Response:")
        st.write(response)
    else:
        st.warning("⚠️ Please enter a query, upload a resume, and provide a job description.")
