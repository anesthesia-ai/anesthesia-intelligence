import streamlit as st
import openai
from PIL import Image
import pytesseract
import io

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
st.title("Ask Me Anything: Anesthesia + Critical Care")

# ----------------------
# Privacy Notice
# ----------------------
st.info("💡 Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.")

# ----------------------
# Layout with upload and text input inside a container
# ----------------------
with st.container():
    st.markdown("### 📂 Upload Section")
    uploaded_file = st.file_uploader("Upload EKGs, TEGs, Medications List, etc.", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed")

    extracted_text = ""
    if uploaded_file is not None:
        st.success(f"📄 {uploaded_file.name} uploaded successfully!")
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file)
            image = Image.open(uploaded_file)
            extracted_text = pytesseract.image_to_string(image)
        elif uploaded_file.type == "application/pdf":
            st.write("PDF uploaded. (Preview not shown)")
            extracted_text = "PDF file uploaded. Please summarize its contents in your query."

    prompt = st.text_area(
        label="",
        placeholder="Type your question here (e.g., 'Interpret this TEG, EKG, or Labs', 'Home meds and Anesthesia Considerations', 'Anti-coagulant reversal', 'Make care plan an EGD for EF <20% on an LVAD and Milrinone drip')..."
    )

# ----------------------
# Submit Button
# ----------------------
if st.button("⏳ Submit Question"):
    if not prompt and not uploaded_file:
        st.warning("Please enter a question or upload a file.")
    else:
        full_prompt = prompt
        if extracted_text:
            full_prompt = f"User provided the following file contents: {extracted_text}\n\nAdditionally, user asked: {prompt}"

        with st.spinner("🔄 Thinking..."):
            try:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are an expert CRNA and Critical Care Consultant. Help interpret uploaded files and answer based on clinical best practices."},
                            {"role": "user", "content": full_prompt}
                        ]
                    )
                except openai.APIError as e:
                    if "model_not_found" in str(e) or "You do not have access" in str(e):
                        st.warning("🔄 GPT-4 not available. Falling back to GPT-3.5-turbo.")
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are an expert CRNA and Critical Care Consultant. Help interpret uploaded files and answer based on clinical best practices."},
                                {"role": "user", "content": full_prompt}
                            ]
                        )
                    else:
                        raise e
                st.success("✅ Response ready!")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
