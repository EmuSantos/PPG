import streamlit as st

# ----- Streamlit Page Configuration -----
st.set_page_config(page_title="PPG", page_icon="🌍", layout="centered")

# ----- Project Title -----
st.markdown("""
# 🌍 Environmental Zone Project - Pico y Placa Generator
#### A tool for creating vehicle restriction metadata
""")

# ----- Project Description -----
st.markdown("""
The **PPG** helps cities and mobility platforms define and export vehicle restriction rules.

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

col1, col2 = st.columns(3)

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

# ----- Footer -----
st.markdown("---")
st.markdown("""
Open-source project for smart mobility platforms.  
🔗 [GitHub Repository](https://github.com/EmuSantos/PPG)
""")
