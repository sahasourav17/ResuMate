import streamlit as st
import os
import openai
from dotenv import load_dotenv
from llama_index.core.llama_pack import download_llama_pack

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

pack_folder = "./resume_screener_pack"
ResumeScreenerPack = download_llama_pack("ResumeScreenerPack", pack_folder)
# if not os.path.exists(pack_folder):
#     ResumeScreenerPack = download_llama_pack("ResumeScreenerPack", pack_folder)
# else:
#     from resume_screener_pack.llama_index.packs.resume_screener import (
#         ResumeScreenerPack,
#     )


def fact_check_resume(resume_content, criteria_decisions):
    fact_check_prompt = f"""
    Givent the following resume content and criteria decisions, please fact-check the claims made in the resume:
    
    Resume Content:
    {resume_content}
    
    Criteria Decision:
    {criteria_decisions}
    
    Please list any potential discrepancies or areas that may need verification:
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for fact-checking resumes.",
            },
            {"role": "user", "content": fact_check_prompt},
        ],
    )

    return response.choices[0].message.content


def rate_resume(criteria_decisions, overall_decision):
    rate_prompt = f"""
    Given the criteria decisions and overall decision, please rate the resume from 1 (lowest) to 10 (highest):
    
    Criteria Decisions:
    {criteria_decisions}
    
    Overall Decision:
    {overall_decision}
    
    Please provide a numerical rating and a brief explanation for your rating:
    
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for rating resumes.",
            },
            {"role": "user", "content": rate_prompt},
        ],
    )

    return response.choices[0].message.content


st.title("ResuMate")

uploaded_file = st.file_uploader("Upload the Resume File", type=["pdf"])

col1, col2 = st.columns(2)
with col1:
    job_description = st.text_area("Job Description", "")
with col2:
    criteria = st.text_area("Selection Criteria (One per line)", "")

if (
    st.button("Screen Resume")
    and uploaded_file is not None
    and job_description
    and criteria
):
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    criteria_list = [c.strip() for c in criteria.split("\n") if c.strip()]

    resume_screener = ResumeScreenerPack(
        job_description=job_description,
        criteria=criteria_list,
    )

    response = resume_screener.run(resume_path="temp_resume.pdf")

    st.subheader("Screening Results")

    decisions = [
        {
            "title": f"Criteria Decision {i+1}",
            "reasoning": cd.reasoning,
            "decision": cd.decision,
        }
        for i, cd in enumerate(response.criteria_decisions)
    ]
    decisions.append(
        {
            "title": "Overall Decision",
            "reasoning": response.overall_reasoning,
            "decision": response.overall_decision,
        }
    )

    decision_summary = []
    for decision in decisions:
        st.markdown(f"#### {decision['title']}")
        st.write(decision["reasoning"])
        st.write(f"Decision: {decision['decision']}")

        decision_summary.extend(
            [
                decision["title"],
                decision["reasoning"],
                f"Decision: {decision['decision']}",
                "",
            ]
        )

    decision_summary = "\n".join(decision_summary).strip()

    st.subheader("Fact-Checking Results")
    fact_check_results = fact_check_resume(
        decision_summary, response.criteria_decisions
    )
    st.markdown(fact_check_results)

    st.subheader("Resume Rating")
    rating_results = rate_resume(response.criteria_decisions, response.overall_decision)
    st.markdown(rating_results)

    os.remove("temp_resume.pdf")
else:
    st.info(
        "Please upload a resume file, enter job description and criteria, then click 'Screen Resume'."
    )
