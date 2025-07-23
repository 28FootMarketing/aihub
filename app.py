# app.py
import streamlit as st
import json
import base64
from urllib.parse import parse_qs
query_params = st.experimental_get_query_params()
unlocked_token = query_params.get("unlock", [None])[0]

paywall = tool.get("paywall", {})
if paywall.get("active"):
    if unlocked_token != paywall.get("unlock_token"):
        st.warning("🔒 Premium tool. Please unlock to continue.")
        st.markdown(f"[🔓 Unlock Now]({paywall.get('stripe_url')})")
        st.stop()
# ---------- Config ----------
st.set_page_config(page_title="28 Foot AI Dashboard", layout="wide", page_icon="🤖")

# ---------- Load Tool Data ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ config.json missing.")
    tool_data = {}

# ---------- Header ----------
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

st.markdown('<div class="header">🤖 28 Foot AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Recruiting Agents • Tools • Automation</div>', unsafe_allow_html=True)

# ---------- Section Switch ----------
view = st.sidebar.radio("Select Mode", ["🌐 Public Dashboard", "🔐 Admin Panel"])

# ---------- 🌐 PUBLIC DASHBOARD ----------
if view == "🌐 Public Dashboard":
    if tool_data:
        selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
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
        st.warning("No tools available. Check config.json.")

# ---------- 🔐 ADMIN PANEL ----------
elif view == "🔐 Admin Panel":
    admin_code = st.text_input("Enter Admin Access Code:", type="password")
    if admin_code != "28FootAccess":
        st.warning("🔒 Admin access only")
        st.stop()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🛠 Manage Agents", "📸 Upload Avatar", "🔁 Trigger GHL", "📥 Export JSON"
    ])

    # --- Tab 1: Manage Agents ---
    with tab1:
        st.subheader("Add a New Agent")
        agent_name = st.text_input("Agent Name")
        agent_category = st.selectbox("Category", list(tool_data.keys()))
        agent_desc = st.text_area("Agent Description")
        agent_link = st.text_input("Launch Link (URL)")
        agent_img = st.text_input("Image URL")

        if st.button("✅ Save Agent"):
            new_agent = {
                "name": agent_name,
                "desc": agent_desc,
                "link": agent_link,
                "image": agent_img
            }
            tool_data[agent_category].append(new_agent)
            with open("config.json", "w") as f:
                json.dump(tool_data, f, indent=2)
            st.success(f"Agent '{agent_name}' added to '{agent_category}'.")

    # --- Tab 2: Upload Avatar Image (Base64 for local use) ---
    with tab2:
        st.subheader("Upload Avatar")
        file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if file:
            st.image(file, width=120)
            b64 = base64.b64encode(file.read()).decode()
            st.text_area("Base64 Preview", b64[:200] + "...")

    # --- Tab 3: Trigger GoHighLevel (placeholder) ---
    with tab3:
        st.subheader("Trigger GHL Webhook")
        email = st.text_input("Lead Email")
        tag = st.text_input("Tag to Apply")
        if st.button("📨 Send Tag (Simulated)"):
            st.success(f"Tag '{tag}' sent to {email} (simulated)")

    # --- Tab 4: Export JSON ---
    with tab4:
        st.subheader("Download Tool Data")
        st.download_button("📄 Export JSON", data=json.dumps(tool_data, indent=2), file_name="tool_data.json")

# ---------- Footer ----------
st.markdown("---")
st.markdown("🚀 Built by [28 Foot Marketing](https://28footmarketing.com)")
