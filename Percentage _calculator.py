import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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

st.title("💰 Professional Money Card")

# --- STAGE 1: Setup ---
if st.session_state.step == "setup":
    name = st.text_input("Enter your full name", value="Aravindan Varadarajan")
    amount = st.number_input("Enter initial amount", min_value=0.0, step=1.0, value=100.0)
    
    if st.button("Next"):
        st.session_state.user_name = name
        st.session_state.current_amount = amount
        st.session_state.history = []
        st.session_state.step = "percentage"
        st.rerun()

# --- STAGE 2: Calculations ---
elif st.session_state.step == "percentage":
    st.subheader(f"Current Balance: {st.session_state.current_amount}")
    percent = st.number_input("Enter percentage (%)", min_value=0.0, step=0.1)

    if st.button("Apply Percentage"):
        reduction = st.session_state.current_amount * (percent / 100)
        new_amount = st.session_state.current_amount - reduction
        
        step_num = len(st.session_state.history) + 1
        entry = (f"Calculation {step_num}", f"{st.session_state.current_amount} * {percent}% = {new_amount}")
        st.session_state.history.append(entry)
        
        st.session_state.current_amount = new_amount
        st.rerun()

    if st.button("Finish & Generate Card"):
        st.session_state.step = "final"
        st.rerun()

# --- STAGE 3: Final Optimized Card ---
elif st.session_state.step == "final":
    # 1. Create a Phone-Sized Canvas (Portrait 1080x1920 scaled down for web)
    width, height = 400, 700 
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 2. Draw Text (Using default font; size is simulated with spacing)
    y_offset = 60
    
    # Header: Name (Bold simulation)
    draw.text((40, y_offset), f"NAME: {st.session_state.user_name.upper()}", fill=(0, 0, 0))
    draw.text((41, y_offset), f"NAME: {st.session_state.user_name.upper()}", fill=(0, 0, 0)) # Double draw for bold
    
    y_offset += 60
    draw.line((40, y_offset, 360, y_offset), fill=(200, 200, 200))
    y_offset += 40

    # Calculations
    for label, calc in st.session_state.history:
        # Bold Label
        draw.text((40, y_offset), f"{label}:", fill=(0, 0, 0))
        draw.text((41, y_offset), f"{label}:", fill=(0, 0, 0))
        y_offset += 25
        # Calculation detail
        draw.text((40, y_offset), calc, fill=(60, 60, 60))
        y_offset += 50

    # Final Total
    y_offset += 40
    draw.line((40, y_offset, 360, y_offset), fill=(0, 0, 0), width=2)
    y_offset += 30
    final_text = f"TOTAL MONEY: {st.session_state.current_amount}"
    draw.text((40, y_offset), final_text, fill=(0, 128, 0))
    draw.text((41, y_offset), final_text, fill=(0, 128, 0)) # Bold Total

    # 3. Display and Download
    st.image(img, caption="WhatsApp Optimized Card")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Image to Share",
        data=byte_im,
        file_name="result_card.png",
        mime="image/png"
    )

    if st.button("Start New"):
        st.session_state.step = "setup"
        st.rerun()
