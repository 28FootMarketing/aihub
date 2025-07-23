updated_admin_panel = """
# admin_panel.py

import streamlit as st
import base64
import json
import datetime
import requests

# Constants
GOOGLE_SHEET_WEBHOOK = "https://your-webhook-url.com/save-agent"  # Replace with real webhook or n8n endpoint
TOKEN_ROTATOR_URL = "https://your-webhook-url.com/rotate-token"   # Optional for dynamic token rotation

def load_admin_panel(tool_data):
    st.sidebar.markdown("### Admin Access")
    admin_code = st.sidebar.text_input("Enter Admin Code:", type="password")

    if admin_code == "28FootAccess":
        st.markdown("## 🔐 Admin Control Panel")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🛠 Manage Agents",
            "📸 Upload Avatars",
            "💳 Paywall Setup",
            "🔁 GHL Triggers",
            "📥 Export Logs"
        ])

        with tab1:
            st.markdown("### 🔧 Edit or Add Agent")
            agent_name = st.text_input("Agent Name")
            agent_category = st.selectbox("Category", list(tool_data.keys()))
            agent_desc = st.text_area("Agent Description")
            agent_link = st.text_input("Agent Launch URL")
            agent_image = st.text_input("Avatar Image URL")
            agent_badge = st.text_input("Badge Emoji", value="🎯")
            agent_updated = datetime.date.today().isoformat()

            if st.button("✅ Save Agent"):
                new_agent = {
                    "name": agent_name,
                    "desc": agent_desc,
                    "link": agent_link,
                    "image": agent_image,
                    "badge": agent_badge,
                    "category": agent_category,
                    "updated": agent_updated,
                    "launch_count": 0,
                    "paywall": {"active": False}
                }

                try:
                    response = requests.post(GOOGLE_SHEET_WEBHOOK, json=new_agent)
                    if response.status_code == 200:
                        st.success(f"Agent '{agent_name}' saved successfully.")
                    else:
                        st.error("Save failed. Please check webhook URL.")
                except Exception as e:
                    st.error(f"Error: {e}")

        with tab2:
            st.markdown("### 🖼 Upload Avatar Image")
            uploaded_file = st.file_uploader("Upload avatar", type=["png", "jpg", "jpeg"])
            if uploaded_file:
                st.image(uploaded_file, caption="Preview")
                b64 = base64.b64encode(uploaded_file.getvalue()).decode()
                st.text_area("Base64 String", b64[:200] + "...")

        with tab3:
            st.markdown("### 💳 Paywall Token + Stripe Setup")
            token_agent_name = st.text_input("Agent Name (Token Protected)")
            stripe_url = st.text_input("Stripe Checkout URL")
            if st.button("🔐 Generate & Assign Token"):
                try:
                    payload = {"tool": token_agent_name}
                    res = requests.post(TOKEN_ROTATOR_URL, json=payload)
                    if res.status_code == 200:
                        generated_token = res.json().get("token", "unknown")
                        st.success(f"Token generated: {generated_token}")
                    else:
                        st.warning("Failed to generate token.")
                except Exception as e:
                    st.error(f"Token error: {e}")

        with tab4:
            st.markdown("### 🔁 Trigger GHL Tag")
            email = st.text_input("Lead Email")
            tag = st.text_input("Tag to Apply in GHL")
            if st.button("📨 Apply Tag"):
                st.success(f"Webhook triggered for {email} with tag '{tag}' (simulated).")

        with tab5:
            st.markdown("### 📥 Download Agent Data")
            st.download_button("⬇ Download config.json", data=json.dumps(tool_data), file_name="config.json")
    else:
        st.warning("🔒 Admin panel locked. Enter admin code in sidebar.")
"""

# Save the updated admin panel file
admin_panel_path = "/mnt/data/admin_panel.py"
with open(admin_panel_path, "w") as f:
    f.write(updated_admin_panel)

admin_panel_path
