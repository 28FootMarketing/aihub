# app_client.py
import streamlit as st
import json

# ---------- Config ----------
st.set_page_config(
    page_title="28 Foot AI Agent Hub",
    layout="wide",
    page_icon="🤖"
)

st.markdown("""
<style>
.header {
    font-size:36px;
    font-weight:800;
    color:#1F4E79;
}
.subheader {
    font-size:20px;
    color:#444;
}
.box {
    border:1px solid #ccc;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Branding ----------
st.markdown('<div class="header">🤖 AI Recruiting Agent Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Built by 28 Foot Marketing to help athletes win before they arrive</div>', unsafe_allow_html=True)

# ---------- Load Agent Data ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ config.json missing.")
    tool_data = {}

# ---------- Display Tools ----------
if tool_data:
    selected_tool = st.selectbox("Select a Tool Category", list(tool_data.keys()))
    st.markdown(f"### {selected_tool}")

    for tool in tool_data[selected_tool]:
        with st.container():
            cols = st.columns([1, 5])
            with cols[0]:
                st.image(tool["image"], width=90)
            with cols[1]:
                st.markdown(f"**{tool['name']}**")
                st.markdown(tool["desc"])
                st.markdown(f"[🔗 Launch Tool]({tool['link']})")
else:
    st.warning("No tools available at this time.")

# ---------- Footer ----------
st.markdown("---")
st.markdown("🚀 Powered by 28 Foot Marketing | [Visit Site](https://28footmarketing.com)")
