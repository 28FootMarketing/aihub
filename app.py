# app.py
import streamlit as st
import json
from admin_panel import load_admin_panel  # make sure admin_panel.py is in the same folder

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
</style>
""", unsafe_allow_html=True)

# ---------- Branding ----------
st.markdown('<div class="header">🤖 28 Foot Marketing AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Custom GPT Tools, Recruiting Agents, and Automation Launchpad</div>', unsafe_allow_html=True)

# ---------- Tool Data (Mock / Replace with DB or Google Sheet) ----------
tool_data = {
    "📣 Recruiting Agents": [
        {"name": "Khloe – Lead Closer", "desc": "NEPQ-style follow-up bot to convert athlete leads."},
        {"name": "Magic – Opportunity Connector", "desc": "Matches athletes to best-fit colleges based on stats."}
    ],
    "🎓 Training Modules": [
        {"name": "Kobe – Recruiting Educator", "desc": "Delivers weekly training and challenge content."},
        {"name": "Dawn – Mental Reset Agent", "desc": "Supports emotional discipline and check-ins."}
    ],
    "💼 Business Automation": [
        {"name": "Bill – System Manager", "desc": "Monitors agent flows, alerts, and fallback automations."},
        {"name": "Steph – Skill Sharpening", "desc": "Improves technical workflows and marketing systems."}
    ],
    "🧠 GPT Assistant Tools": [
        {"name": "Recruit Tip Bot", "desc": "Delivers a daily recruiting tip via SMS or email."},
        {"name": "Parent Support GPT", "desc": "Explains the recruiting process in plain language."}
    ]
}

# ---------- Sidebar Navigation ----------
st.sidebar.title("Tool Menu")
menu_option = st.sidebar.radio("Select Section", [
    "📂 Agent Tools",
    "🔐 Admin Control Panel"
])

# ---------- Agent Tools Viewer ----------
if menu_option == "📂 Agent Tools":
    selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
    st.markdown(f"### {selected_tool}")

    for tool in tool_data[selected_tool]:
        st.markdown(f"""
        <div class="box">
            <strong>{tool['name']}</strong><br>
            {tool['desc']}
            <br><br>
            <a href="https://ai.28footmarketing.com" target="_blank">
                🔗 Launch Tool
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔍 Raw Agent JSON Preview")
    st.json(tool_data)

# ---------- Admin Panel Loader ----------
elif menu_option == "🔐 Admin Control Panel":
    load_admin_panel(tool_data)

# ---------- Footer ----------
st.markdown("---")
st.markdown("🚀 Powered by 28 Foot Marketing | Visit: [https://28footmarketing.com](https://28footmarketing.com)")
