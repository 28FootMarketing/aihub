
import streamlit as st
import base64
import json

def load_admin_panel(tool_data):
    st.sidebar.markdown("### Admin Access")
    admin_code = st.sidebar.text_input("Enter Admin Code:", type="password")

    if admin_code == "28FootAccess":
        st.markdown("## 🔐 Admin Control Panel")

        tab1, tab2, tab3, tab4 = st.tabs([
            "🛠 Manage Agents",
            "📸 Upload Assets",
            "🔁 GHL Triggers",
            "📥 Export / Logs"
        ])

        with tab1:
            st.markdown("### 🔧 Edit or Add Agent")
            agent_name = st.text_input("Agent Name")
            agent_category = st.selectbox("Category", list(tool_data.keys()))
            agent_desc = st.text_area("Agent Description")
            agent_link = st.text_input("Launch Link")
            agent_image = st.text_input("Avatar Image URL")
            agent_badge = st.text_input("Badge Icon (e.g., 🔥)")
            agent_paywall = st.checkbox("Enable Paywall?")
            stripe_url = st.text_input("Stripe Checkout URL") if agent_paywall else ""
            unlock_token = st.text_input("Unlock Token") if agent_paywall else ""

            if st.button("✅ Save Agent"):
                new_agent = {
                    "name": agent_name,
                    "desc": agent_desc,
                    "link": agent_link,
                    "image": agent_image,
                    "badge": agent_badge,
                    "category": agent_category,
                    "updated": "2025-07-23",
                    "launch_count": 0,
                    "paywall": {
                        "active": agent_paywall,
                        "stripe_url": stripe_url,
                        "unlock_token": unlock_token
                    } if agent_paywall else { "active": False }
                }
                tool_data[agent_category].append(new_agent)
                with open("config.json", "w") as f:
                    json.dump(tool_data, f, indent=2)
                st.success(f"Agent '{agent_name}' saved.")
        with tab2:
            st.markdown("### 🖼 Upload Avatar")
            uploaded_file = st.file_uploader("Upload avatar image", type=["png", "jpg", "jpeg"])
            if uploaded_file:
                st.image(uploaded_file, caption="Preview")
                b64 = base64.b64encode(uploaded_file.getvalue()).decode()
                st.text_area("Base64 Embed (first 200 chars)", b64[:200] + "...")
        with tab3:
            st.markdown("### 🔁 Trigger GHL Webhook")
            email = st.text_input("Lead Email")
            tag = st.text_input("GHL Tag to Apply")
            if st.button("📨 Send Tag to GHL"):
                st.success(f"Webhook triggered (placeholder) for {email} with tag '{tag}'")
        with tab4:
            st.markdown("### 📥 Export Logs")
            st.download_button("Download JSON", data=json.dumps(tool_data), file_name="export_config.json")
    else:
        st.warning("🔒 Admin panel locked. Enter access code in sidebar.")
