# app_admin.py
import streamlit as st
import json
import base64

# ---------- Config ----------
st.set_page_config(
    page_title="Admin Control Panel",
    layout="wide",
    page_icon="🛠"
)

# ---------- Branding ----------
st.title("🛠 28 Foot Admin Control Panel")

# ---------- Load Tool Data ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ config.json missing.")
    tool_data = {}

# ---------- Auth Gate ----------
admin_code = st.text_input("Enter Admin Code:", type="password")
if admin_code != "28FootAccess":
    st.warning("🔒 Access Denied. Enter correct admin code.")
    st.stop()

# ---------- Admin Panel Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛠 Manage Agents", "📸 Upload Avatars", "🔁 Trigger GHL", "📥 Export Data"
])

# --- Tab 1: Manage Agents ---
with tab1:
    st.subheader("Edit or Add Agent")
    agent_name = st.text_input("Agent Name")
    agent_category = st.selectbox("Category", list(tool_data.keys()))
    agent_desc = st.text_area("Agent Description")
    agent_link = st.text_input("Agent Launch URL")
    agent_img = st.text_input("Avatar Image URL")

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

# --- Tab 2: Upload Avatars ---
with tab2:
    st.subheader("Upload Avatar (Base64)")
    file = st.file_uploader("Choose Image", type=["png", "jpg", "jpeg"])
    if file:
        st.image(file, width=120)
        b64 = base64.b64encode(file.read()).decode()
        st.text_area("Base64 Output (preview)", b64[:200] + "...")

# --- Tab 3: GHL Trigger (Optional Webhook) ---
with tab3:
    st.subheader("Send GHL Tag (Placeholder)")
    lead_email = st.text_input("Lead Email")
    tag = st.text_input("GHL Tag to Apply")
    if st.button("📨 Trigger GHL Webhook"):
        st.success(f"Triggered tag '{tag}' for {lead_email} (simulated)")

# --- Tab 4: Export Tool JSON ---
with tab4:
    st.subheader("Download Full Tool Data")
    st.download_button("📄 Download JSON", data=json.dumps(tool_data, indent=2), file_name="tool_data.json")
