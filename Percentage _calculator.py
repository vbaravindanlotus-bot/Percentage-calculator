import streamlit as st
from PIL import Image, ImageDraw
import io
import base64

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = "setup"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Settlement App", layout="centered")

# --- STAGE 1: Setup ---
if st.session_state.step == "setup":
    st.title("👑 Settlement Setup")
    # Field is empty by default
    name_input = st.text_input("Enter the name", value="") 
    amount_input = st.number_input("Enter initial balance", min_value=0.0, step=0.01)
    
    if st.button("Next"):
        if name_input.strip():
            st.session_state.user_name = name_input
            st.session_state.current_amount = amount_input
            st.session_state.step = "adjustment"
            st.rerun()
        else:
            st.error("Please enter a name to proceed.")

# --- STAGE 2: Settlement Adjustments ---
elif st.session_state.step == "adjustment":
    st.subheader(f"Account: {st.session_state.user_name}")
    st.write(f"Current Balance: **{st.session_state.current_amount}**")
    
    percent = st.number_input("Adjustment Percentage (%)", min_value=0.0, step=0.1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Apply Adjustment"):
            # Sequential Math Logic
            reduction = st.session_state.current_amount * (percent / 100)
            new_amount = st.session_state.current_amount - reduction
            
            st.session_state.history.append({
                "label": f"Adjustment {len(st.session_state.history)+1}",
                "detail": f"{st.session_state.current_amount} - {percent}% = {round(new_amount, 2)}"
            })
            st.session_state.current_amount = round(new_amount, 2)
            st.rerun()
    
    with col2:
        if st.button("Generate Final Slip"):
            st.session_state.step = "final"
            st.rerun()

    if st.button("⬅️ Back to Setup"):
        st.session_state.step = "setup"
        st.rerun()

# --- STAGE 3: Final Card (57mm x 40mm standard) ---
elif st.session_state.step == "final":
    # Width 215px matches handheld POS standard
    width = 215 
    height = 300 + (len(st.session_state.history) * 55)
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    y = 30
    # Name Header (Size 24 equiv)
    name_txt = st.session_state.user_name.upper()
    draw.text((15, y), name_txt, fill=(0, 0, 0))
    draw.text((16, y), name_txt, fill=(0, 0, 0)) # Bold
    
    y += 35
    draw.line((15, y, 200, y), fill=(0, 0, 0), width=1)
    y += 25

    # Adjustments (Size 14 equiv)
    for item in st.session_state.history:
        draw.text((15, y), f"{item['label']}:", fill=(0, 0, 0))
        draw.text((16, y), f"{item['label']}:", fill=(0, 0, 0))
        y += 18
        draw.text((15, y), item['detail'], fill=(50, 50, 50))
        y += 35

    # Final Total (Size 18 equiv)
    y += 15
    draw.line((15, y, 200, y), fill=(0, 0, 0), width=2)
    y += 20
    total_txt = f"FINAL BALANCE: {st.session_state.current_amount}"
    draw.text((15, y), total_txt, fill=(0, 128, 0))
    draw.text((16, y), total_txt, fill=(0, 128, 0))

    # Footer (Size 16 equiv)
    y += 50
    draw.text((65, y), "THANK YOU!", fill=(0, 0, 0))
    draw.text((66, y), "THANK YOU!", fill=(0, 0, 0))

    st.image(img, caption="Final Settlement Slip")

    # Processing for Download and Share
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    b64_img = base64.b64encode(img_bytes).decode()

    col_down, col_share = st.columns(2)
    with col_down:
        st.download_button("📥 Download", data=img_bytes, file_name="settlement.png", mime="image/png")
    
    with col_share:
        # Native Web Share for Mobile
        share_js = f"""
            <script>
            async function shareImage() {{
                const res = await fetch("data:image/png;base64,{b64_img}");
                const blob = await res.blob();
                const file = new File([blob], 'settlement.png', {{ type: 'image/png' }});
                if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                    await navigator.share({{ files: [file], title: 'Settlement' }});
                }}
            }}
            </script>
            <button onclick="shareImage()" style="background-color:#25D366;color:white;border:none;padding:10px;border-radius:5px;width:100%;font-weight:bold;cursor:pointer;">📲 Share</button>
        """
        st.components.v1.html(share_js, height=60)

    if st.button("⬅️ Back to Adjustments"):
        st.session_state.step = "adjustment"
        st.rerun()

    if st.button("🆕 New Settlement"):
        st.session_state.step = "setup"
        st.session_state.history = []
        st.rerun()
