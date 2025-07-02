import streamlit as st
import pandas as pd
from graphviz import Digraph

st.set_page_config(page_title="Advanced Registers & Counters")
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
st.title("🧮 Advanced Registers & Counters")

st.markdown("""
This module expands on registers and counters with:
- 4-bit counter truth tables
- Example timing diagram
- Flip-flop chain visual
- Step-by-step simulation
- Clock signal demo
""")

st.header("📊 4-bit Up Counter: Truth Table")

# 4-bit up counter truth table
rows = []
for i in range(16):
    binary = format(i, "04b")
    rows.append([i] + list(binary))

df_up = pd.DataFrame(rows, columns=["Decimal", "Q3", "Q2", "Q1", "Q0"])
st.table(df_up)

st.header("📊 4-bit Down Counter: Truth Table")

rows_down = []
for i in reversed(range(16)):
    binary = format(i, "04b")
    rows_down.append([i] + list(binary))

df_down = pd.DataFrame(rows_down, columns=["Decimal", "Q3", "Q2", "Q1", "Q0"])
st.table(df_down)

st.markdown("---")

st.header("⏱️ Example Timing Diagram")

st.info("Below is a simple static example — upload your own for real circuits!")

timing_diagram_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/RippleCounterTimingDiagram.png/500px-RippleCounterTimingDiagram.png"

# ✅ FIXED: use_container_width
st.image(timing_diagram_url, caption="Sample Ripple Counter Timing Diagram", use_container_width=True)

uploaded_timing = st.file_uploader("Or upload your own timing diagram:", type=["png", "jpg"])
if uploaded_timing:
    st.image(uploaded_timing, caption="Uploaded Timing Diagram", use_container_width=True)

st.markdown("---")

st.header("🔗 Flip-Flop Chain (4-bit Ripple Counter)")

# Draw chain using Graphviz
dot = Digraph(comment="4-bit Ripple Counter")
for i in range(4):
    dot.node(f"T{i}", f"T Flip-Flop {i+1}")
for i in range(3):
    dot.edge(f"T{i}", f"T{i+1}", label="Clock")

dot.attr(rankdir="LR")
st.graphviz_chart(dot)

st.markdown("---")

st.header("🚦 Step-by-Step Counter Simulator")

st.write("Simulate a simple 4-bit counter by pressing Next.")

if 'counter' not in st.session_state:
    st.session_state.counter = 0

col1, col2 = st.columns(2)

with col1:
    if st.button("Next Clock Pulse ➡️"):
        st.session_state.counter = (st.session_state.counter + 1) % 16

with col2:
    if st.button("Reset 🔄"):
        st.session_state.counter = 0

current = st.session_state.counter
binary = format(current, "04b")
st.info(f"**Decimal:** {current} | **Binary:** {binary}")

# Show outputs visually
st.write(f"Q3: `{binary[0]}`, Q2: `{binary[1]}`, Q1: `{binary[2]}`, Q0: `{binary[3]}`")

st.markdown("---")

st.header("⏰ Clock Signal Demo")

st.write("""
A counter needs a clock signal to advance. Below is an example video showing how clock pulses drive flip-flops and counters.
""")

# ✅ Example working clock signal video
st.video("https://www.youtube.com/watch?v=7ukDKVHnac4")

st.info("Try it live: [Falstad Circuit Simulator ➜](https://falstad.com/circuit/)")

st.markdown("---")

st.success("✅ Tip: Use Logisim, Proteus, or CircuitVerse to simulate these counters practically!")
