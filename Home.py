import streamlit as st

# Set global page config for the entire app
st.set_page_config(
    page_title="DLD Course Helper",
    page_icon="🧮",
    layout="centered"
)
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

st.title("📘 Digital Logic Design Course Helper")

st.write("""
Welcome to your all-in-one **Digital Logic Design (DLD)** learning tool!  
Use the **sidebar** to navigate through interactive modules:

- ✅ **Boolean Expression Evaluator & Gate Diagram**
- ✅ **K-Map Simplifier**
- ✅ **Circuit Simulator** *(optional placeholder if not built yet)*
- ✅ **Flip-Flop & Latch Visualizer**
- ✅ **Number System Converter & Tools**
- ✅ **Logic Gates & DeMorgan's Laws**

---

**📚 Tip:** Each page includes examples and explanations — explore and learn!
""")

st.info("👈 *Use the sidebar to pick a module.*")
st.markdown("---")


