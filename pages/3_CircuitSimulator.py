import streamlit as st
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
st.title("⚡️ Circuit Simulator & Workspace")

st.write("""
**This page helps students work with circuit simulations, uploads, and external tools.**

🧩 **What you can do here:**
- Upload your **circuit diagrams** (images)
- Upload your **simulation reports** (PDF)
- Upload **circuit videos** (MP4)
- Embed and link to online simulators
- Write **notes** and submit
""")

# Example external simulator link
example_url = "https://circuitverse.org/simulator"
st.markdown(f"👉 [Try CircuitVerse Online ➜]({example_url})")

# Upload Diagram Image
st.subheader("📁 Upload Circuit Diagram")
uploaded_image = st.file_uploader(
    "Upload image (PNG, JPG, JPEG, SVG)",
    type=["png", "jpg", "jpeg", "svg"],
    key="upload_img"
)
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Circuit Diagram", use_column_width=True)

# Upload PDF
st.subheader("📄 Upload Circuit Report (PDF)")
uploaded_pdf = st.file_uploader(
    "Upload PDF Report",
    type=["pdf"],
    key="upload_pdf"
)
if uploaded_pdf:
    st.success(f"Uploaded: {uploaded_pdf.name}")

# Upload Video
st.subheader("🎥 Upload Circuit Demo Video")
uploaded_video = st.file_uploader(
    "Upload MP4 Video",
    type=["mp4"],
    key="upload_vid"
)
if uploaded_video:
    st.video(uploaded_video)

# Student Notes
st.subheader("📝 Notes")
notes = st.text_area("Write any notes or description here...")

if st.button("✅ Submit"):
    st.success("Your diagram/report/video and notes have been saved (placeholder action).")

st.subheader("📺 Example: Logic Gates Explained")
st.video("https://www.youtube.com/watch?v=HpwNEjcDVFI")

st.subheader("📺 Example: DeMorgan’s Theorem")
st.video("https://www.youtube.com/watch?v=JYecfwHOhb4")



