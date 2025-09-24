from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import fitz  # PyMuPDF - replace pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Use PyMuPDF instead of pdf2image
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document[0]
        
        # Convert to image
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes("jpeg")
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")
#Streamlit App
st.set_page_config(page_title="ATS Resume EXpert")
st.header("Resumind - ATS Resume Tracker")
input_text = st.text_area("Enter Job Description",key="input") 
uploaded_file = st.file_uploader("Upload Resume (PDF)...",type=["pdf"])
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Get ATS Score")
submit3 = st.button("Percentage Match")
submit4 = st.button("Get Interview Questions")
submit5 = st.button("Get Resume Suggestions")

input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of any one job role from Data Science,Full Stack Web Development,Big Data Engineering,DEVOPS,Data Analyst,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced ATS Resume Reviewer with expertise in Data Science, Full Stack Web Development, Big Data Engineering, DEVOPS, and Data Analyst roles. 
Analyze the provided resume against the job description and provide detailed improvement suggestions:
1. Skills that need to be added or strengthened
2. Experience gaps that should be addressed
3. Technical keywords missing from the resume
4. Format and structure improvements
5. Specific recommendations to increase ATS compatibility
6. Certifications or projects that would enhance the profile
Please provide actionable and specific suggestions for improvement.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from  Data Science,Full Stack Web Development,Big Data Engineering,DEVOPS,Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt4 = """
You are a Senior Technical Interviewer with 10+ years of experience in Data Science, Full Stack Web Development, Big Data Engineering, DEVOPS, and Data Analyst domains.
Based on the resume and job description provided, generate relevant interview questions:
1. 5 Technical questions based on skills mentioned in resume
2. 3 Behavioral questions related to the job role
3. 2 Scenario-based questions for problem-solving
4. 1-2 Questions about projects mentioned in resume
Format the questions clearly and provide the difficulty level (Beginner/Intermediate/Advanced) for each technical question.
"""

input_prompt5 = """
You are an ATS (Applicant Tracking System) Scoring Expert. Analyze the resume against the job description and provide:
1. Overall ATS Score (0-100)
2. Breakdown by categories:
   - Skills Match (%)
   - Experience Relevance (%)
   - Keyword Density (%)
   - Format Compatibility (%)
3. Critical missing keywords
4. Top 5 recommendations to improve ATS score
5. Probability of passing initial ATS screening
Present the score prominently at the beginning.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt5,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt4,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the Resume")