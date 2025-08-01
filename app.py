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
    st.markdown("---")

# ---------- Role Filter ----------
user_role = st.sidebar.selectbox("Select Your Role", ['athlete', 'parent', 'coach', 'admin'])

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

# ---------- Header ----------
st.markdown('<div class="header">🤖 28 Foot AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Recruiting Agents • Tools • Automation</div>', unsafe_allow_html=True)

# ---------- View Selector ----------
view = st.sidebar.radio("Select Mode", ["🌐 Public Dashboard", "🔐 Admin Panel"])

# ---------- Public Dashboard ----------
if view == "🌐 Public Dashboard":
    if tool_data:
        selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
        st.markdown(f"### 🧠 Category: `{selected_tool}`")
        search_term = st.text_input("🔍 Search Tool Name")

        filtered_tools = [
            tool for tool in tool_data[selected_tool]
            if search_term.lower() in tool["name"].lower()
        ]

        for tool in filtered_tools:
            roles_allowed = tool.get("roles_allowed", [])
            if roles_allowed and user_role not in roles_allowed:
                st.markdown(f"""
                <div class="card">
                    <img src="{tool['image']}" width="75">
                    <h4>{tool['name']} 🔒</h4>
                    <p>{tool['desc']}</p>
                    <p><strong>Restricted to specific roles.</strong></p>
                </div>
                """, unsafe_allow_html=True)
                continue

            paywall = tool.get("paywall", {})
            is_locked = paywall.get("active") and not is_valid_token(unlocked_token, tool["name"])

            if is_locked:
                st.markdown(f"""
                <div class="card">
                    <img src="{tool['image']}" width="75">
                    <h4>{tool['name']} 🔒</h4>
                    <p>{tool['desc']}</p>
                    <p><strong>Premium Access Required</strong></p>
                    <a href="{paywall.get('stripe_url')}" target="_blank">💳 Unlock Now</a>
                </div>
                """, unsafe_allow_html=True)
                continue

            st.markdown(f"""
            <div class="card">
                <img src="{tool['image']}" width="75">
                <h4>{tool['name']} {tool.get('badge', '')}</h4>
                <p>{tool['desc']}</p>
                <p><small>🚀 Launches: {tool.get('launch_count', 0)}</small></p>
                <a href="{tool['link']}" target="_blank">🔗 Launch Tool</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No agents found. Check config.json.")
