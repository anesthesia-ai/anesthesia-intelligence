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
# Inject custom Google Font
# ----------------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# ----------------------
# Title and Subtitle
# ----------------------
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-weight: normal; margin-bottom: 10px;'>Anesthesia <span style='font-size: 80px; color: black; margin: 0 10px;'>.</span> Intelligence</h1>
    <div style='font-family: "Pacifico", cursive; font-size: 20px; color: #555;'>A.I</div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Centered styled container for upload and text input
# ----------------------
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <div style="background-color: #f9f9f9; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); width: 100%; max-width: 700px;">
""", unsafe_allow_html=True)

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
    placeholder="Type your question here (e.g., 'Interpret this TEG, EKG, or Labs', 'Home meds and Anesthesia Considerations', 'Anti-coagulant reversal', 'Make care plan an EGD for EF <20% on an LVAD and Milrinone drip')...",
    height=150
)

# ----------------------
# Submit Button
# ----------------------
st.markdown("""
<div style='display: flex; justify-content: center; margin-top: 20px;'>
    <button style="background-color: #4CAF50; color: white; padding: 10px 24px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background-color 0.3s;">
        ⏳ Submit Question
    </button>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("Submit"):
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

# ----------------------
# Privacy Notice (footer)
# ----------------------
st.markdown(
    """
    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-size: 12px; text-align: center; margin-top: 30px;">
    ⚡ Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.
    </div>
    """,
    unsafe_allow_html=True
)
