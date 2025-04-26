import streamlit as st
import openai
from PIL import Image
import pytesseract
import io
import base64

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
      div[data-testid="stFileUploader"] { visibility: hidden; height: 0px; overflow: hidden; position: absolute; }
      .flex-container {
        display: flex;
        align-items: center;
        background-color: #2c2f36;
        border-radius: 24px;
        padding: 15px;
        margin: auto;
        width: 100%;
        max-width: 900px;
        box-shadow: inset 0 0 8px rgba(255, 255, 255, 0.1);
        position: relative;
      }
      .flex-container input[type="text"] {
        flex: 1;
        margin: 0 10px;
        padding: 20px;
        border: none;
        background-color: transparent;
        color: white;
        font-size: 20px;
      }
      .upload-label, .mic-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 24px;
        color: white;
        transition: 0.3s;
      }
      .upload-label:hover, .mic-button:hover {
        filter: brightness(1.2);
      }
      .mic-button:disabled {
        color: gray;
        cursor: not-allowed;
      }
      .thumbnail {
        height: 40px;
        width: 40px;
        object-fit: cover;
        border-radius: 6px;
        margin-right: 10px;
        animation: fadeIn 0.5s;
      }
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .ask-button:hover {
        background-color: #3d8bfd;
        transition: background-color 0.3s ease;
      }
      .footer {
        background-color: #333;
        color: white;
      }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Title and Subtitle
# ----------------------
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-weight: normal; margin-bottom: 10px; text-align: center;'>
        <span style='color: red;'>&gt;</span> Anesthesia <span style='font-size: 120px; color: blue; margin: 0 10px;'>.</span> Intelligence <span style='color: red;'>&lt;</span>
    </h1>
    <div style='font-family: "Pacifico", cursive; font-size: 20px; color: #555; text-align: center;'>A.I</div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Upload logic
# ----------------------
placeholder = st.empty()
uploaded_file = placeholder.file_uploader("", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed", key="hidden-upload")

upload_html = '<label class="upload-label">➕</label>'

if uploaded_file:
    if uploaded_file.type.startswith("image/"):
        image = Image.open(uploaded_file)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        encoded = base64.b64encode(byte_im).decode()
        upload_html = f'<img src="data:image/png;base64,{encoded}" class="thumbnail">'
    else:
        upload_html = '<span class="upload-label">📄</span>'

# ----------------------
# Unified Input Bar
# ----------------------
st.markdown(f"""
<div class="flex-container">
  {upload_html}
  <input id="text-input" name="prompt" type="text" placeholder="Type your question here (e.g., 'Interpret this TEG, EKG, or Labs', 'Home meds and Anesthesia Considerations', 'Anti-coagulant reversal', 'Make care plan an EGD for EF <20% on an LVAD and Milrinone drip')...">
  <button class="mic-button" disabled>🎤</button>
</div>
""", unsafe_allow_html=True)

submit = st.button("🚀 Ask The A.I.", key="ask_button", use_container_width=True)

# ----------------------
# Privacy Notice (footer)
# ----------------------
st.markdown("""
<div class="footer" style="padding: 12px; border-radius: 8px; font-size: 12px; text-align: center; margin-top: 40px;'>
⚡ Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.
</div>
""", unsafe_allow_html=True)
