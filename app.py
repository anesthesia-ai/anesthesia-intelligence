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
      .thumbnail {
        height: 30px;
        width: 30px;
        object-fit: cover;
        border-radius: 6px;
        margin-right: 10px;
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
extracted_text = ""
uploaded_thumbnail = ""
prompt = ""

st.markdown("""
<div class="flex-container">
  <input type="file" id="hidden-upload" accept="image/*,application/pdf" style="display:none" onchange="uploadFile(event)">
  <label for="hidden-upload" class="upload-label">➕</label>
  <input id="text-input" name="prompt" type="text" placeholder="Type your question here (e.g., 'Interpret this TEG, EKG, or Labs', 'Home meds and Anesthesia Considerations', 'Anti-coagulant reversal', 'Make care plan an EGD for EF <20% on an LVAD and Milrinone drip')...">
  <button class="mic-button">🎤</button>
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

submit = st.button("⏳ Submit Question", use_container_width=True)

if submit:
    if not prompt:
        st.warning("Please enter a question or upload a file.")
    else:
        full_prompt = prompt

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
st.markdown("""
<div class="footer" style="padding: 12px; border-radius: 8px; font-size: 12px; text-align: center; margin-top: 40px;">
⚡ Privacy Reminder: Please do not upload PHI (Protected Health Information). Files are processed temporarily and not stored permanently.
</div>
""", unsafe_allow_html=True)
