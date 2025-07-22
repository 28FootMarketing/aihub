# app.py
import streamlit as st
import json
from admin_panel import load_admin_panel

# ---------- Page Config ----------
st.set_page_config(
    page_title="28 Foot Marketing AI Dashboard",
    layout="wide",
    page_icon="🤖"
)

# ---------- Styling ----------
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
.avatar {
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

# ---------- Branding ----------
st.markdown('<div class="header">🤖 28 Foot Marketing AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Custom GPT Tools, Recruiting Agents, and Automation Launchpad</div>', unsafe_allow_html=True)

# ---------- Load Tool Data from config.json ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ Could not find config.json. Please add the file to the project directory.")
    tool_data = {}

# ---------- Sidebar Navigation ----------
st.sidebar.title("Tool Menu")
menu_option = st.sidebar.radio("Select Section", [
    "📂 Agent Tools",
    "🔐 Admin Control Panel"
])

# ---------- Agent Tools Viewer ----------
if menu_option == "📂 Agent Tools":
    if tool_data:
        selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
        st.markdown(f"### {selected_tool}")

        for tool in tool_data[selected_tool]:
            with st.container():
                cols = st.columns([1, 5])
                with cols[0]:
                    if "image" in tool:
                        st.image(tool["image"], width=90)
                with cols[1]:
                    st.markdown(f"**{tool['name']}**")
                    st.markdown(tool["desc"])
                    st.markdown(f"[🔗 Launch Tool]({tool['link']})")

        st.markdown("### 🔍 Raw Agent JSON Preview")
        st.json(tool_data)
    else:
        st.warning("No agent data available. Check your config.json file.")

# ---------- Admin Panel Loader ----------
elif menu_option == "🔐 Admin Control Panel":
    load_admin_panel(tool_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("🚀 Powered by 28 Foot Marketing | Visit: [https://28footmarketing.com](https://28footmarketing.com)")
