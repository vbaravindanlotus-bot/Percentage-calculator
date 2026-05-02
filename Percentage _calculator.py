import streamlit as st
from PIL import Image, ImageDraw
import io

# Initialize session state for tracking stages and data
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("💰 Money Calculation Card")

# --- STAGE 1: Enter Name and Amount ---
if st.session_state.step == "setup":
    # Specific input for the name
    name_input = st.text_input("Enter the name", placeholder="e.g. Aravindan Varadarajan")
    amount_input = st.number_input("Enter the amount", min_value=0.0, step=1.0, value=100.0)
    
    if st.button("Next"):
        if name_input.strip() == "":
            st.error("Please enter a name to continue.")
        else:
            st.session_state.user_name = name_input
            st.session_state.current_amount = amount_input
            st.session_state.history = []
            st.session_state.step = "percentage"
            st.rerun()

# --- STAGE 2: Percentage Entry ---
elif st.session_state.step == "percentage":
    st.subheader(f"User: {st.session_state.user_name}")
    st.write(f"Current Balance: **{st.session_state.current_amount}**")
    
    percent = st.number_input("Enter percentage (%)", min_value=0.0, step=0.1)

    if st.button("Calculate"):
        reduction = st.session_state.current_amount * (percent / 100)
        new_amount = st.session_state.current_amount - reduction
        
        step_num = len(st.session_state.history) + 1
        # Store as bold-ready labels
        st.session_state.history.append({
            "label": f"Calculation {step_num}",
            "detail": f"{st.session_state.current_amount} * {percent}% = {new_amount}"
        })
        
        st.session_state.current_amount = new_amount
        st.rerun()

    if st.button("Finish & View Card"):
        st.session_state.step = "final"
        st.rerun()

# --- STAGE 3: Final Card Generation ---
elif st.session_state.step == "final":
    # Create Phone-Optimized Canvas (Portrait)
    width, height = 450, 800 
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    y = 50
    # Draw Bold Name (using double-draw method for weight)
    name_text = st.session_state.user_name.upper()
    draw.text((40, y), name_text, fill=(0, 0, 0))
    draw.text((41, y), name_text, fill=(0, 0, 0))
    
    y += 50
    draw.line((40, y, 410, y), fill=(200, 200, 200), width=1)
    y += 40

    # Draw Calculations
    for item in st.session_state.history:
        # Bold Calculation Label
        draw.text((40, y), f"{item['label']}:", fill=(0, 0, 0))
        draw.text((41, y), f"{item['label']}:", fill=(0, 0, 0))
        y += 25
        # Calculation Detail
        draw.text((40, y), item['detail'], fill=(50, 50, 50))
        y += 60

    # Final Bold Total
    y += 30
    draw.line((40, y, 410, y), fill=(0, 0, 0), width=2)
    y += 30
    total_text = f"TOTAL MONEY = {st.session_state.current_amount}"
    draw.text((40, y), total_text, fill=(0, 100, 0))
    draw.text((41, y), total_text, fill=(0, 100, 0))

    st.image(img, caption="Final Result Card")
    
    # Download logic
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Card as Image",
        data=byte_im,
        file_name="calculation_card.png",
        mime="image/png"
    )

    if st.button("Start New Calculation"):
        st.session_state.step = "setup"
        st.rerun()
