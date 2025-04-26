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
      .flex-container {
        display: flex;
        align-items: center;
        background-color: #2c2f36;
        border-radius: 24px;
        padding: 10px;
        margin: auto;
        width: 100%;
        max-width: 700px;
      }
      .flex-container input[type="text"] {
        flex: 1;
        margin: 0 10px;
        padding: 10px;
        border: none;
        background-color: transparent;
        color: white;
        font-size: 16px;
      }
      .upload-label, .mic-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 20px;
        color: white;
      }
      .mic-button:disabled {
        color: gray;
        cursor: not-allowed;
      }
      .thumbnail {
        height: 30px;
        width: 30px;
        object-fit: cover;
        border-radius: 6px;
        margin-right: 10px;
        animation: bounceIn 0.5s;
      }
      @keyframes bounceIn {
        0% { transform: scale(0.5); opacity: 0; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1); }
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
    <h1 style='font-weight: normal; margin-bottom: 10px;'>
        <span style='color: red;'>&gt;</span> Anesthesia <span style='font-size: 120px; color: blue; margin: 0 10px;'>.</span> Intelligence <span style='color: red;'>&lt;</span>
    </h1>
    <div style='font-family: "Pacifico", cursive; font-size: 20px; color: #555;'>A.I</div>
</div>
""", unsafe_allow_html=True)

# ----------------------
# Unified Upload + Text Input
# ----------------------
st.markdown("""
<div class="flex-container">
  <input type="file" id="hidden-upload" accept="image/*,application/pdf" style="display:none" onchange="uploadFile(event)">
  <label for="hidden-upload" class="upload-label">➕</label>
  <input id="text-input" name="prompt" type="text" placeholder="Interpret this TEG, EKG, or Labs','Make care plan an EGD for EF <20% on an LVAD and Milrinone drip">
  <button class="mic-button" disabled>🎤</button>
</div>
<script>
function uploadFile(event) {
  const file = event.target.files[0];
  if(file){
    const reader = new FileReader();
    reader.onload = function(e){
      const imgTag = document.createElement('img');
      imgTag.src = e.target.result;
      imgTag.className = 'thumbnail';
      document.querySelector('.upload-label').replaceWith(imgTag);
    }
    reader.readAsDataURL(file);
  }
}
</script>
""", unsafe_allow_html=True)

submit = st.button("Ask The A.I.", use_container_width=True)

# ----------------------
# Privacy Notice (footer)
# ----------------------
st.markdown("""
<div class="footer" style="padding: 12px; border-radius: 8px; font-size: 12px; text-align: center; margin-top: 40px;'>
⚡ Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.
</div>
""", unsafe_allow_html=True)
