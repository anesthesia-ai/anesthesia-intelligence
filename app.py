import streamlit as st
import openai

# Load OpenAI key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Ask Me Anything", "Create Anesthesia Plan", "Upload Studies", "Group Licenses"])

# Student Mode Toggle
student_mode = st.sidebar.toggle("Student Mode (detailed explanations)")

# HIPAA Reminder Text
hipaa_notice = """
<small style='color:gray'>
<b>Privacy Notice:</b>  
At Anesthesia Intelligence, we take your privacy seriously and do not store or share any uploaded data beyond your active session.  
However, please be aware that your healthcare facility or institution may have policies that prohibit sharing Protected Health Information (PHI) with third-party platforms.  
Before uploading any patient images or data, please ensure compliance with your organization's HIPAA and internal guidelines.
</small>
"""

# Ask Me Anything Page
if menu == "Ask Me Anything":
    st.title("Ask Me Anything: Anesthesia + Critical Care")
    user_input = st.text_area("Type your question below (e.g., 'Interpret this TEG' or 'Help plan an EGD for EF <20%'):")

    if st.button("Submit Question"):
        if user_input.strip() != "":
            system_prompt = "You are an expert anesthesia and critical care assistant. Provide medically accurate, concise, evidence-based answers."
            if student_mode:
                system_prompt += " Include detailed educational explanations suitable for a student."

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response['choices'][0]['message']['content']
            st.markdown(answer)

# Create Anesthesia Plan Page
elif menu == "Create Anesthesia Plan":
    st.title("Student Mode: Create Anesthesia Plan")
    patient_info = st.text_area("Enter case info (e.g., '31yo F 98kg NKDA robotic thymectomy'):")

    if st.button("Generate Plan"):
        if patient_info.strip() != "":
            system_prompt = "You are an anesthesia care plan assistant. Generate Preoperative, Intraoperative, and Postoperative plans. Always begin by stating assumptions if patient history is limited. Explain critical steps, cite sources at bottom Wikipedia-style."
            if not student_mode:
                system_prompt += " Be concise, less detailed."

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": patient_info}
                ]
            )
            plan = response['choices'][0]['message']['content']
            st.markdown(plan)

# Upload Studies Page
elif menu == "Upload Studies":
    st.title("Upload and Interpret Medical Studies")
    uploaded_file = st.file_uploader("Upload EKG, BMP, PFT, TEG, airway photo, etc.", accept_multiple_files=False)
    st.markdown(hipaa_notice, unsafe_allow_html=True)

    hipaa_acknowledged = st.checkbox("I have reviewed my organization's HIPAA policies before uploading.")

    if uploaded_file is not None:
        if hipaa_acknowledged:
            file_bytes = uploaded_file.read()
            file_text = file_bytes.decode("utf-8", errors="ignore")

            prompt = f"Interpret the following uploaded medical text or lab report for anesthesia management:\n\n{file_text}"

            system_prompt = "You are an expert anesthesia assistant. Interpret labs, EKGs, PFTs, airway assessments, etc., and highlight anesthesia concerns."
            if student_mode:
                system_prompt += " Include educational explanation for students."

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            interpretation = response['choices'][0]['message']['content']
            st.markdown(interpretation)
        else:
            st.warning("Please acknowledge HIPAA compliance before proceeding.")

# Group Licenses Page
elif menu == "Group Licenses":
    st.title("Group License Discounts Available")
    st.markdown("""
    | Group Size | Price per User | Discount |
    |:--|:--|:--|
    | 5–10 users | $14.99/month | 25% off |
    | 11–25 users | $9.99/month | 50% off |
    | 26+ users | Custom quote | up to 65% off |

    Interested in group licensing for your program or facility?

    **[Request a Custom Quote by Contacting info@yourfuturecompany.com]**
    """)

# End
