import streamlit as st
import json
import base64
import requests

# ---------- Page Setup ----------
st.set_page_config(
    page_title="28 Foot AI Dashboard",
    layout="wide",
    page_icon="🤖"
)

# ---------- Sidebar Branding ----------
with st.sidebar:
    st.image("https://28footmarketing.com/logo.png", width=140)
    st.markdown("**28 Foot Marketing**")
    st.caption("🚀 AI Recruiting Tools for Game-Changers")
    view = st.radio("Select Mode", ["🌐 Public Dashboard", "🔐 Admin Panel"])
    st.markdown("---")

# ---------- Custom Styles ----------
st.markdown("""
<style>
body {
    background-color: #f9f9f9;
}
.card {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 12px;
    padding: 20px;
    transition: transform 0.2s ease;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}
.card:hover {
    transform: scale(1.03);
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}
.card img {
    float: right;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("""
<div style="background: url('https://28footmarketing.com/hero.jpg') center/cover no-repeat; padding: 60px 30px; border-radius: 12px;">
    <h1 style="color: white; font-size: 38px;">🚀 Welcome to the 28 Foot AI Dashboard</h1>
    <p style="color: white; font-size: 18px;">Tap into tools built for recruiters, athletes, and agencies who want results—not guesses.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Token Validator ----------
def is_valid_token(token, tool_name):
    url = "https://script.google.com/macros/s/YOUR_DEPLOYED_SCRIPT_ID/exec"
    payload = {"token": token, "tool": tool_name}
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.json().get("valid", False) if response.status_code == 200 else False
    except Exception as e:
        print("Token validation error:", e)
        return False

# ---------- Load Data ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ config.json missing.")
    tool_data = {}

# ---------- Query Params ----------
query_params = st.query_params
unlocked_token = query_params.get("token", [None])[0]

# ---------- Category Icons ----------
category_icons = {
    "📣 Recruiting Agents": "🎯",
    "🎓 Training Modules": "📘",
    "💼 Business Automation": "⚙️",
    "🧠 GPT Assistant Tools": "🧩"
}

# ---------- View Routing ----------
if view == "🌐 Public Dashboard":
    if tool_data:
        selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
        icon = category_icons.get(selected_tool, "")
        st.markdown(f"### {icon} {selected_tool}")
        search_term = st.text_input("🔍 Search Tool Name")

        filtered_tools = [
            tool for tool in tool_data[selected_tool]
            if search_term.lower() in tool["name"].lower()
        ]

        total_launches = sum([t.get('launch_count', 0) for group in tool_data.values() for t in group])
        st.metric(label="Total Tool Launches", value=f"{total_launches} 🚀")

        for tool in filtered_tools:
            paywall = tool.get("paywall", {})
            is_locked = paywall.get("active") and not is_valid_token(unlocked_token, tool["name"])

            if is_locked:
                st.markdown(f"""<div class="card">
                    <img src="{tool['image']}" width="75">
                    <h4>{tool['name']} 🔒</h4>
                    <p>{tool['desc']}</p>
                    <p><strong>Premium Access Required</strong></p>
                    <a href="{paywall.get('stripe_url')}" target="_blank">💳 Unlock Now</a>
                </div>""", unsafe_allow_html=True)
                continue

            st.markdown(f"""<div class="card">
                <img src="{tool['image']}" width="75">
                <h4>{tool['name']} {tool.get('badge', '')}</h4>
                <p>{tool['desc']}</p>
                <p><small>🚀 Launches: {tool.get('launch_count', 0)}</small></p>
                <a href="{tool['link']}" target="_blank" style="
                    background-color: #0072ff;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 8px;
                    display: inline-block;
                    margin-top: 10px;
                ">🔗 Launch Tool</a>
            </div>""", unsafe_allow_html=True)
    else:
        st.warning("No agents found. Check config.json.")

elif view == "🔐 Admin Panel":
    from admin_panel import load_admin_panel
    load_admin_panel(tool_data)
