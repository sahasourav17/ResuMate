import streamlit as st
import os
import openai
from dotenv import load_dotenv
from llama_index.core.llama_pack import download_llama_pack

# Load environment variables and set up OpenAI API key
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Download the ResumeScreenerPack
pack_folder = "./resume_screener_pack"
if not os.path.exists(pack_folder):
    print("hello")
    # Download the ResumeScreenerPack if the folder doesn't exist
    ResumeScreenerPack = download_llama_pack("ResumeScreenerPack", pack_folder)
else:
    # If the folder exists, import the pack
    from resume_screener_pack.llama_index.packs.resume_screener import (
        ResumeScreenerPack,
    )

st.title("ResuMate")

# File uploader for resume
uploaded_file = st.file_uploader("Upload the Resume File", type=["pdf"])

# Input fields for job description and criteria

col1, col2 = st.columns(2)
with col1:
    job_description = st.text_area(
        "Job Description", "Please enter the job description here"
    )
with col2:
    criteria = st.text_area(
        "Selection Criteria", "Please enter the selection criteria here (one per line)"
    )

if (
    st.button("Screen Resume")
    and uploaded_file is not None
    and job_description
    and criteria
):
    # Save the uploaded file temporarily
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process the criteria into a list
    criteria_list = [c.strip() for c in criteria.split("\n") if c.strip()]

    # Initialize the ResumeScreenerPack
    resume_screener = ResumeScreenerPack(
        job_description=job_description,
        criteria=criteria_list,
    )

    # Run the resume screening
    response = resume_screener.run(resume_path="temp_resume.pdf")

    # Display results
    st.subheader("Screening Results")

    for cd in response.criteria_decisions:
        st.markdown(f"#### Criteria Decision")
        st.write(cd.reasoning)
        st.write(f"Decision: {cd.decision}")

    st.markdown("#### Overall Decision")
    st.write(response.overall_reasoning)
    st.write(f"Final Decision: {response.overall_decision}")

    # Clean up the temporary file
    os.remove("temp_resume.pdf")
else:
    st.info(
        "Please upload a resume file, enter job description and criteria, then click 'Screen Resume'."
    )
