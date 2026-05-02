import streamlit as st

# Initialize session state to store our data across "refreshes"
if 'step' not in st.session_state:
    st.session_state.step = "amount"
if 'initial_amount' not in st.session_state:
    st.session_state.initial_amount = 0.0
if 'current_amount' not in st.session_state:
    st.session_state.current_amount = 0.0
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("💰 Money Calculator")

# --- STAGE 1: Enter Amount ---
if st.session_state.step == "amount":
    amount = st.number_input("Enter the amount", min_value=0.0, step=1.0, value=100.0)
    if st.button("Next"):
        st.session_state.initial_amount = amount
        st.session_state.current_amount = amount
        st.session_state.history = []  
        st.session_state.step = "percentage"
        st.rerun()

# --- STAGE 2: Percentage Calculation ---
elif st.session_state.step == "percentage":
    st.subheader(f"Current Amount: {st.session_state.current_amount}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        percent = st.number_input("Enter percentage (%)", min_value=0.0, step=0.1)
    with col2:
        st.write(" ") 
        st.write("%")

    col3, col4, col5 = st.columns(3)
    
    with col3:
        if st.button("Calculate"):
            reduction = st.session_state.current_amount * (percent / 100)
            new_amount = st.session_state.current_amount - reduction
            entry = f"{st.session_state.current_amount} * {percent}% = {new_amount}"
            st.session_state.history.append(entry)
            st.session_state.current_amount = new_amount
            st.rerun()

    with col4:
        if st.button("Back to Start"):
            st.session_state.step = "amount"
            st.rerun()
            
    with col5:
        if st.button("Finish"):
            st.session_state.step = "final"
            st.rerun()

    if st.session_state.history:
        st.write("---")
        for h in st.session_state.history:
            st.text(h)

# --- STAGE 3: Final Summary ---
elif st.session_state.step == "final":
    st.success("Calculation Finished")
    for h in st.session_state.history:
        st.write(h)
    st.divider()
    st.header(f"Your Money is = {st.session_state.current_amount}")
    if st.button("Start New Calculation"):
        st.session_state.step = "amount"
        st.rerun()
