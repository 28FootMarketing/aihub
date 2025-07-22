import streamlit as st
import json

# -------- Settings -------- #
st.set_page_config(
    page_title="28 Foot Marketing AI Hub",
    layout="wide",
    page_icon="🤖"
)

# -------- Branding -------- #
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

st.markdown('<div class="header">🤖 28 Foot Marketing AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Access GPT tools, workflow agents, and automations</div>', unsafe_allow_html=True)

# -------- Sidebar Navigation -------- #
st.sidebar.title("Agent Menu")
selected_tool = st.sidebar.radio("Select Agent", [
    "📣 Recruiting Agents",
    "🎓 Training Modules",
    "💼 Business Automation",
    "🧠 GPT Assistant Tools",
])

# -------- Tool Info JSON (simulated) -------- #
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

# -------- Display Section -------- #
st.markdown(f"### {selected_tool}")

for tool in tool_data[selected_tool]:
    st.markdown(f"""
    <div class="box">
        <strong>{tool["name"]}</strong><br>
        {tool["desc"]}
        <br><br>
        <a href="https://ai.28footmarketing.com" target="_blank">
            🔗 Launch Tool
        </a>
    </div>
    """, unsafe_allow_html=True)

# -------- Optional JSON Viewer -------- #
st.markdown("### 🔍 Raw Agent JSON Preview")
st.json(tool_data)

# -------- Placeholder for GHL Integration -------- #
with st.expander("🔁 Lead Flow Integration (GHL Placeholder)"):
    st.write("This panel will sync with GoHighLevel to track tool usage, leads, and automation triggers.")
    st.write("Future feature: Live webhook trigger + tagging via GHL API or n8n.")

# -------- Footer -------- #
st.markdown("---")
st.markdown("🚀 Powered by 28 Foot Marketing | Visit: [https://28footmarketing.com](https://28footmarketing.com)")
