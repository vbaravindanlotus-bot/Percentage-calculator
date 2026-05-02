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

st.title("💰 Money Calculation Card")

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

# --- STAGE 2: Sequential Percentages ---
elif st.session_state.step == "percentage":
    st.subheader(f"Current Balance: {st.session_state.current_amount}")
    percent = st.number_input("Enter percentage (%)", min_value=0.0, step=0.1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Apply Percentage"):
            reduction = st.session_state.current_amount * (percent / 100)
            new_amount = st.session_state.current_amount - reduction
            
            # Record step
            step_num = len(st.session_state.history) + 1
            entry = f"Calculation {step_num}: {st.session_state.current_amount} - {percent}% = {new_amount}"
            st.session_state.history.append(entry)
            
            st.session_state.current_amount = new_amount
            st.rerun()

    with col2:
        if st.button("Finish & Generate Card"):
            st.session_state.step = "final"
            st.rerun()

    if st.session_state.history:
        st.write("---")
        for h in st.session_state.history:
            st.text(h)

# --- STAGE 3: Final Card Generation ---
elif st.session_state.step == "final":
    st.success("Summary Generated")
    
    # Create an Image (Card)
    img = Image.new('RGB', (500, 400), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # Text content for the card
    card_text = f"NAME: {st.session_state.user_name}\n\n"
    for h in st.session_state.history:
        card_text += f"{h}\n"
    card_text += f"\nTOTAL MONEY: {st.session_state.current_amount}"
    
    d.text((20, 20), card_text, fill=(255, 255, 0))
    
    # Display the Card
    st.image(img, caption="Your Calculation Card")
    
    # Convert image to bytes for download
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Card to Share on WhatsApp",
        data=byte_im,
        file_name="money_card.png",
        mime="image/png"
    )

    if st.button("Start New"):
        st.session_state.step = "setup"
        st.rerun()
