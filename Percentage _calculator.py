import streamlit as st
from PIL import Image, ImageDraw
import io

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="POS Slip Calc", layout="centered")

# --- STAGE 1: Setup ---
if st.session_state.step == "setup":
    st.subheader("Receipt Setup")
    name_input = st.text_input("Enter the name", placeholder="Aravindan Varadarajan")
    amount_input = st.number_input("Enter the amount", min_value=0.0, step=0.01, value=100.0)
    
    if st.button("Start Calculations"):
        if name_input:
            st.session_state.user_name = name_input
            st.session_state.current_amount = amount_input
            st.session_state.step = "percentage"
            st.rerun()

# --- STAGE 2: Calculations ---
elif st.session_state.step == "percentage":
    st.write(f"User: **{st.session_state.user_name}**")
    st.write(f"Current Balance: **{st.session_state.current_amount}**")
    percent = st.number_input("Next Percentage (%)", min_value=0.0, step=0.1)

    if st.button("Apply %"):
        reduction = st.session_state.current_amount * (percent / 100)
        new_amount = st.session_state.current_amount - reduction
        st.session_state.history.append({
            "label": f"Calculation {len(st.session_state.history)+1}",
            "detail": f"{st.session_state.current_amount} * {percent}% = {round(new_amount, 2)}"
        })
        st.session_state.current_amount = round(new_amount, 2)
        st.rerun()

    if st.button("Generate POS Slip"):
        st.session_state.step = "final"
        st.rerun()

# --- STAGE 3: Final Card ---
elif st.session_state.step == "final":
    # POS Slip Size: Narrow (380px) and Dynamic Height
    # Height accounts for Header, Calculations, Total, and Thank You
    width = 380
    height = 320 + (len(st.session_state.history) * 60)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    y = 40
    # Name: Size 24 (Simulated Bold & Large)
    draw.text((20, y), st.session_state.user_name.upper(), fill=(0, 0, 0))
    draw.text((21, y), st.session_state.user_name.upper(), fill=(0, 0, 0)) 
    
    y += 40
    draw.line((20, y, 360, y), fill=(0, 0, 0), width=1)
    y += 30

    # Calculations: Size 14
    for item in st.session_state.history:
        draw.text((20, y), f"{item['label']}:", fill=(0, 0, 0))
        draw.text((21, y), f"{item['label']}:", fill=(0, 0, 0))
        y += 20
        draw.text((20, y), item['detail'], fill=(60, 60, 60))
        y += 40

    # Total: Size 18
    y += 20
    draw.line((20, y, 360, y), fill=(0, 0, 0), width=2)
    y += 25
    total_txt = f"TOTAL: {st.session_state.current_amount}"
    draw.text((20, y), total_txt, fill=(0, 128, 0))
    draw.text((21, y), total_txt, fill=(0, 128, 0))

    # THANK YOU!: Size 16 (Centered)
    y += 60
    thank_you_text = "THANK YOU!"
    # Simple centering logic
    draw.text((120, y), thank_you_text, fill=(0, 0, 0))
    draw.text((121, y), thank_you_text, fill=(0, 0, 0))

    # Display result
    st.image(img, caption="Final POS Slip")

    # Image processing for sharing
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    st.download_button("Save Receipt to Phone", data=img_bytes, file_name="pos_receipt.png", mime="image/png")
    st.info("Download the image first, then share it to WhatsApp. This keeps your data private and log-free.")

    if st.button("New Calculation"):
        st.session_state.step = "setup"
        st.session_state.history = []
        st.rerun()
