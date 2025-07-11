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
    st.markdown("Download the step-by-step guide or watch a tutorial with examples for AMER zone.")
    st.button("Coming Soon...")

import requests
with col_t2:
    st.markdown("### 🔵 APAC Tutorial")
    st.markdown("Download the step-by-step guide or watch a tutorial with examples for APAC zone.")
    
    docx_url = "https://github.com/EmuSantos/PPG/blob/main/Work%20Instruction%20-%20APAC.docx"
    
    try:
        response = requests.get(docx_url)
        response.raise_for_status()
    
        st.download_button(
            label="⬇️ APAC Work Instruction",
            data=response.content,
            file_name="Work Instruction - APAC.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except requests.exceptions.RequestException:
        st.error("⚠️ Could not load the tutorial document. Please try again later.")

    st.link_button("▶️ Go to APAC Demo", 'https://here.webex.com/recordingservice/sites/here/recording/playback/e0bc8d64c8d849b8ad5e180c80ef294e')

# EMEA Tutorial
with col_t3:
    st.markdown("### 🔴 EMEA Tutorial")
    st.markdown("Download the step-by-step guide or watch a tutorial with examples for EMEA zone")
    
    docx_url = "https://github.com/EmuSantos/PPG/blob/main/Work%20Instruction%20-%20EMEA.docx"
    
    try:
        response = requests.get(docx_url)
        response.raise_for_status()
    
        st.download_button(
            label="⬇️ EMEA Work Instruction",
            data=response.content,
            file_name="Work Instruction - EMEA.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except requests.exceptions.RequestException:
        st.error("⚠️ Could not load the tutorial document. Please try again later.")

    st.link_button("▶️ Go to EMEA Demo", "https://here.webex.com/recordingservice/sites/here/recording/6a46e6cd47464456936776f7049889e9/playback")

st.markdown("### 🗂️ MMT Files Processor")
st.markdown("Quick tutorial for using the MMT Files Processor.")
st.link_button("▶️ Go to MMT Tutorial", 'https://here.webex.com/recordingservice/sites/here/recording/26a5a17a62db40b8822c2bd2d6a0687f/playback')



# ----- Footer -----
st.markdown("---")
st.markdown("""
Open-source project for smart mobility platforms.  
🔗 [GitHub Repository](https://github.com/EmuSantos/PPG)
""")
