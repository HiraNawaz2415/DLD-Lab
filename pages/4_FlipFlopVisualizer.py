import streamlit as st
import pandas as pd
st.markdown(
    """
    <style>
    /* Make sidebar background gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    /* Optional: make sidebar text white */
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: white;
    }

    /* Optional: style sidebar headings and text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("🔄 Flip-Flop & Latch Visualizer")

# Choose between Latch or Flip-Flop
mode = st.radio("Select Mode:", ["Latch", "Flip-Flop"])

if mode == "Latch":
    latch_type = st.selectbox(
        "Select Latch Type:",
        ["SR Latch", "D Latch"]
    )

    if latch_type == "SR Latch":
        st.subheader("SR Latch Truth Table")
        df = pd.DataFrame({
            "S": [0, 0, 1, 1],
            "R": [0, 1, 0, 1],
            "Q(next)": ["Q", "0", "1", "Invalid"]
        })
        st.table(df)
        st.info("SR Latch: Basic latch made with NOR or NAND gates. 'Invalid' when both S & R = 1 for NOR version.")

    elif latch_type == "D Latch":
        st.subheader("D Latch Truth Table")
        df = pd.DataFrame({
            "D": [0, 1],
            "Enable": [1, 1],
            "Q(next)": ["0", "1"]
        })
        st.table(df)
        st.info("D Latch: Data Latch — when Enable=1, output follows D. When Enable=0, output holds its state.")

elif mode == "Flip-Flop":
    ff_type = st.selectbox(
        "Select Flip-Flop Type:",
        ["SR Flip-Flop", "JK Flip-Flop", "D Flip-Flop", "T Flip-Flop"]
    )

    if ff_type == "SR Flip-Flop":
        st.subheader("SR Flip-Flop Truth Table")
        df = pd.DataFrame({
            "S": [0, 0, 1, 1],
            "R": [0, 1, 0, 1],
            "Q(next)": ["Q", "0", "1", "Invalid"]
        })
        st.table(df)
        st.info("SR Flip-Flop: Edge-triggered version of SR Latch. Invalid when both S & R = 1.")

    elif ff_type == "JK Flip-Flop":
        st.subheader("JK Flip-Flop Truth Table")
        df = pd.DataFrame({
            "J": [0, 0, 1, 1],
            "K": [0, 1, 0, 1],
            "Q(next)": ["Q", "0", "1", "~Q"]
        })
        st.table(df)
        st.info("JK Flip-Flop: Solves SR invalid state by toggling output when both J & K = 1.")

    elif ff_type == "D Flip-Flop":
        st.subheader("D Flip-Flop Truth Table")
        df = pd.DataFrame({
            "D": [0, 1],
            "Q(next)": ["0", "1"]
        })
        st.table(df)
        st.info("D Flip-Flop: Data Flip-Flop — output follows D at clock edge.")

    elif ff_type == "T Flip-Flop":
        st.subheader("T Flip-Flop Truth Table")
        df = pd.DataFrame({
            "T": [0, 1],
            "Q(next)": ["Q", "~Q"]
        })
        st.table(df)
        st.info("T Flip-Flop: Toggles output on each clock edge if T=1.")

# Upload timing diagram
st.subheader("Timing Diagram Example (Optional)")
uploaded_timing = st.file_uploader("Upload Timing Diagram Image", type=["png", "jpg", "jpeg"])
if uploaded_timing:
    st.image(uploaded_timing, caption="Timing Diagram", use_column_width=True)
