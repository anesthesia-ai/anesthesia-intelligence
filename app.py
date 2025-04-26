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
# Inject custom Google Font, Dynamic Theme, and Animations
# ----------------------
st.markdown("""
    <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/5/55/Red_circle.png">
    <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
    <style>
      body { animation: fadeIn 1s ease-in; }
      @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
      div.card:hover { transform: scale(1.01); transition: all 0.3s ease-in-out; }
      .divider { border-top: 1px solid #ddd; margin: 30px 0; animation: fadeIn 2s; }
      button:hover { background-color: #45a049 !important; }
      @media (prefers-color-scheme: dark) {
        body { background-color: #0e1117; color: white; }
        div.card { background-color: #222; color: white; }
        .footer { background-color: #333; color: white; }
      }
      @media (prefers-color-scheme: light) {
        body { background-color: white; color: black; }
        div.card { background-color: #f9f9f9; color: black; }
        .footer { background-color: #f0f0f0; color: black; }
      }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Title and Subtitle
# ----------------------
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-weight: normal; margin-bottom: 10px;'>
        <span style='color: red;'>&gt;</span> Anesthesia <span style='font-size: 120px; color: blue; margin: 0 10px;'>.</span> Intelligence <span style='color: red;'>&lt;</span>
    </h1>
    <div style='font-family: "Pacifico", cursive; font-size: 20px; color: #555;'>A.I</div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Unified Upload + Text Input
# ----------------------
with st.container():
    st.markdown("""
    <div class="card" style="padding: 20px; border-radius: 12px; box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15); width: 100%; max-width: 700px; margin: auto;">
    """, unsafe_allow_html=True)

    uploaded_file = None
    extracted_text = ""

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed")

    with col2:
        prompt = st.text_input(
            "", placeholder="Type your question here..."
        )

    with col3:
        st.button("🎤", help="Voice input coming soon!", use_container_width=True)

    if uploaded_file is not None:
        with st.spinner("🔄 Processing file..."):
            if uploaded_file.type.startswith("image/"):
                image = Image.open(uploaded_file)
                extracted_text = pytesseract.image_to_string(image)
            elif uploaded_file.type == "application/pdf":
                extracted_text = "PDF file uploaded. Please summarize its contents in your query."

        st.image(uploaded_file, width=100)
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    submit = st.button("⏳ Submit Question", use_container_width=True)

    if submit:
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

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------
# Privacy Notice (footer)
# ----------------------
st.markdown("""
<div class="footer" style="padding: 12px; border-radius: 8px; font-size: 12px; text-align: center; margin-top: 40px;">
⚡ Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.
</div>
""", unsafe_allow_html=True)
