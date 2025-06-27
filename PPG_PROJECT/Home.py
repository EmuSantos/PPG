import streamlit as st

# ----- Streamlit Page Configuration -----
st.set_page_config(page_title="EZ Metadata Generator", page_icon="🌍", layout="centered")

# ----- Project Title -----
st.markdown("""
# 🌍 Environmental Zone Project - EZ Metadata Generator
#### A tool for creating vehicle restriction metadata
""")

# ----- Project Description -----
st.markdown("""
The **EZ Metadata Generator** helps cities and mobility platforms define and export vehicle restriction rules.

Main features include:

🚗 **License plate-based restrictions** (e.g., odd/even, digit endings)  
🚛 **Min/Max weight restrictions** for trucks  
📅 **Day-specific or date-range restrictions**  
🧾 **Environmental badges, vehicle age, overrides**

All restrictions are exported to structured **CSV and Excel formats**, ready for integration into smart city systems or GIS platforms.
""")
# ----- HERE Technologies Logo -----
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/EmuSantos/PPG/main/here-white-200px.png' width='200'/>
    </div>
    """,
    unsafe_allow_html=True
)

# ----- Navigation Options -----
st.markdown("---")
st.markdown("## 🌐 Select a zone to begin:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 AMER Zone")
    if st.button("Go to AMER Zone"):
        st.switch_page("pages/AMER Zone.py")

with col2:
    st.markdown("### 🔵 APAC Zone")
    if st.button("Go to APAC Zone"):
        st.switch_page("pages/APAC Zone.py")

with col3:
    st.markdown("### 🔴 EMEA Zone")
    if st.button("Go to EMEA Zone"):
        st.switch_page("pages/EMEA Zone.py")

# ----- Tutorials Section -----
st.markdown("---")
st.markdown("## 📘 Tutorials")

st.markdown("""
Learn how to use the EZ Metadata Generator for each regional zone.  
These tutorials will guide you step-by-step through the interface, inputs, and data export process.
""")

col_t1, col_t2, col_t3 = st.columns(3)

# AMER Tutorial
with col_t1:
    st.markdown("### 🟢 AMER Tutorial")
    st.markdown("Basic guide to metadata creation in American zones.")
    st.button("Open AMER Tutorial")

# APAC Tutorial
with col_t2:
    st.markdown("### 🔵 APAC Tutorial")
    st.markdown("Complete walkthrough with examples for APAC restrictions.")

    # Descargar el archivo DOCX desde GitHub
    with open("https://github.com/EmuSantos/PPG/raw/main/Work_Instruction_EZ_Metadata_APAC.docx", "rb") as f:
        btn = st.download_button(
            label="⬇️ Download APAC DOCX",
            data=f,
            file_name="Work_Instruction_EZ_Metadata_APAC.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# EMEA Tutorial
with col_t3:
    st.markdown("### 🔴 EMEA Tutorial")
    st.markdown("Special cases and configuration options for EMEA.")

    st.button("Open EMEA Tutorial")



# ----- Footer -----
st.markdown("---")
st.markdown("""
Open-source project for smart mobility platforms.  
🔗 [GitHub Repository](https://github.com/EmuSantos/PPG)
""")
