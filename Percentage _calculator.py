import streamlit as st
from PIL import Image, ImageDraw
import io
import base64

# Initialize session state for tracking logic
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Calculator", layout="centered")

# --- STAGE 1: Setup ---
if st.session_state.step == "setup":
    st.title("👑 Money Calculation")
    # Field is empty as requested
    name_input = st.text_input("Enter the name", value="") 
    amount_input = st.number_input("Enter the amount", min_value=0.0, step=0.01)
    
    if st.button("Next"):
        if name_input.strip():
            st.session_state.user_name = name_input
            st.session_state.current_amount = amount_input
            st.session_state.step = "percentage"
            st.rerun()
        else:
            st.error("Please enter a name to continue.")

# --- STAGE 2: Calculation Sequence ---
elif st.session_state.step == "percentage":
    st.subheader(f"User: {st.session_state.user_name}")
    st.write(f"Balance: **{st.session_state.current_amount}**")
    percent = st.number_input("Enter percentage (%)", min_value=0.0, step=0.1)

    if st.button("Apply Percentage"):
        reduction = st.session_state.current_amount * (percent / 100)
        new_amount = st.session_state.current_amount - reduction
        st.session_state.history.append({
            "label": f"Calculation {len(st.session_state.history)+1}",
            "detail": f"{st.session_state.current_amount} * {percent}% = {round(new_amount, 2)}"
        })
        st.session_state.current_amount = round(new_amount, 2)
        st.rerun()

    if st.button("View Final Calculation"):
        st.session_state.step = "final"
        st.rerun()

# --- STAGE 3: Final Card (Handheld 57mm Standard) ---
elif st.session_state.step == "final":
    # Width 215px matches the 57mm narrow handheld POS standard
    width = 215 
    height = 250 + (len(st.session_state.history) * 55)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    y = 30
    # Name Header (Scale equivalent to 24px)
    name_txt = st.session_state.user_name.upper()
    draw.text((15, y), name_txt, fill=(0, 0, 0))
    draw.text((16, y), name_txt, fill=(0, 0, 0)) 
    
    y += 35
    draw.line((15, y, 200, y), fill=(0, 0, 0), width=1)
    y += 25

    # Calculation Steps (Scale equivalent to 14px)
    for item in st.session_state.history:
        draw.text((15, y), f"{item['label']}:", fill=(0, 0, 0))
        draw.text((16, y), f"{item['label']}:", fill=(0, 0, 0))
        y += 18
        draw.text((15, y), item['detail'], fill=(50, 50, 50))
        y += 35

    # Bold Total (Scale equivalent to 18px)
    y += 15
    draw.line((15, y, 200, y), fill=(0, 0, 0), width=2)
    y += 20
    total_txt = f"TOTAL: {st.session_state.current_amount}"
    draw.text((15, y), total_txt, fill=(0, 128, 0))
    draw.text((16, y), total_txt, fill=(0, 128, 0))

    # Thank You Message (Scale equivalent to 16px)
    y += 45
    draw.text((65, y), "THANK YOU!", fill=(0, 0, 0))
    draw.text((66, y), "THANK YOU!", fill=(0, 0, 0))

    st.image(img, caption="Final Calculation")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    b64_img = base64.b64encode(img_bytes).decode()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Download", data=img_bytes, file_name="calculation.png", mime="image/png")
    with col2:
        # Native Share Logic for Mobile Browsers
        share_js = f"""
            <script>
            async function shareImage() {{
                const res = await fetch("data:image/png;base64,{b64_img}");
                const blob = await res.blob();
                const file = new File([blob], 'calculation.png', {{ type: 'image/png' }});
                if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                    await navigator.share({{ files: [file], title: 'Final Calculation' }});
                }} else {{
                    alert("Native sharing not supported. Please use Download.");
                }}
            }}
            </script>
            <button onclick="shareImage()" style="background-color:#25D366;color:white;border:none;padding:10px;border-radius:5px;width:100%;font-weight:bold;cursor:pointer;">📲 Share</button>
        """
        st.components.v1.html(share_js, height=60)

    if st.button("New Calculation"):
        st.session_state.step = "setup"
        st.session_state.history = []
        st.rerun()
