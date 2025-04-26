import streamlit as st
import openai

# ----------------------
# SETUP OpenAI Client Safely
# ----------------------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("🔒 OPENAI_API_KEY is missing. Please add it in Streamlit Secrets.")
    st.stop()

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ----------------------
# Title
# ----------------------
st.title("Ask Me Anything: Anesthesia")

# ----------------------
# Privacy Notice
# ----------------------
st.info("💡 Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.")

# ----------------------
# Upload Section
# ----------------------
uploaded_file = st.file_uploader("📂 Upload EKGs, TEGs, Medications List, etc.", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    st.success(f"📄 {uploaded_file.name} uploaded successfully!")
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        st.write("PDF uploaded. (Preview not shown)")

# ----------------------
# Text Input Section
# ----------------------
prompt = st.text_area("💬 Type your question below (e.g., 'Interpret this TEG' or 'Help plan an EGD for EF <20%'):")

if st.button("⏳ Submit Question"):
    if not prompt and not uploaded_file:
        st.warning("Please enter a question or upload a file.")
    else:
        with st.spinner("🔄 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert CRNA and Critical Care Consultant."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.success("✅ Response ready!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

