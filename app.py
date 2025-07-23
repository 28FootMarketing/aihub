import streamlit as st
import json
import base64
import requests

# ---------- Config ----------
st.set_page_config(
    page_title="28 Foot AI Dashboard",
    layout="wide",
    page_icon="🤖"
)

# ---------- Google Sheets Token Validator ----------
def is_valid_token(token, tool_name):
    url = "https://script.google.com/macros/s/YOUR_DEPLOYED_SCRIPT_ID/exec"  # Replace this
    payload = {"token": token, "tool": tool_name}

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result.get("valid", False)
        else:
            return False
    except Exception as e:
        print("Token validation error:", e)
        return False

# ---------- Load Agent Data ----------
try:
    with open("config.json", "r") as file:
        tool_data = json.load(file)
except FileNotFoundError:
    st.error("❌ config.json missing.")
    tool_data = {}

# ---------- Get Unlock Token from URL ----------
query_params = st.query_params
unlocked_token = query_params.get("token", [None])[0]

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

# ---------- View Selector ----------
view = st.sidebar.radio("Select Mode", ["🌐 Public Dashboard", "🔐 Admin Panel"])

# ---------- Public Dashboard ----------
if view == "🌐 Public Dashboard":
    if tool_data:
        selected_tool = st.selectbox("Choose a Tool Category", list(tool_data.keys()))
        st.markdown(f"### {selected_tool}")

        for tool in tool_data[selected_tool]:
            paywall = tool.get("paywall", {})

            # Premium Tool Check
            if paywall.get("active"):
                if not is_valid_token(unlocked_token, tool["name"]):
                    st.warning("🔒 This is a premium tool. Access requires payment.")
                    st.markdown(f"[🔓 Unlock Now]({paywall.get('stripe_url')})")
                    continue

            # Display Agent
            with st.container():
                cols = st.columns([1, 5])
                with cols[0]:
                    st.image(tool["image"], width=90)
                with cols[1]:
                    st.markdown(f"**{tool['name']}** {tool.get('badge', '')}")
                    st.markdown(tool["desc"])
                    st.markdown(f"[🔗 Launch Tool]({tool['link']})")

    else:
        st.warning("No agents found. Check config.json.")

# ---------- Admin Panel ----------
elif view == "🔐 Admin Panel":
    admin_code = st.text_input("Enter Admin Access Code:", type="password")
    if admin_code != "28FootAccess":
        st.warning("🔒 Admin access only")
        st.stop()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🛠 Manage Agents", "📸 Upload Avatar", "🔁 Trigger GHL", "📥 Export JSON"
    ])

# --- Tab 1: Manage Agents (Add + Edit) ---
with tab1:
    st.subheader("➕ Add New Agent")

    agent_name = st.text_input("Agent Name")
    agent_category = st.selectbox("Category", list(tool_data.keys()))
    agent_desc = st.text_area("Description")
    agent_link = st.text_input("Tool Launch Link")
    agent_img = st.text_input("Avatar Image URL")
    badge = st.text_input("Badge (emoji)", value="")
    paywall_active = st.checkbox("Is this a premium tool?")
    stripe_url = st.text_input("Stripe Checkout URL") if paywall_active else ""
    unlock_token_input = st.text_input("Temporary Unlock Token") if paywall_active else ""

    if st.button("✅ Save Agent"):
        new_agent = {
            "name": agent_name,
            "desc": agent_desc,
            "link": agent_link,
            "image": agent_img,
            "badge": badge,
            "category": agent_category,
            "updated": "2025-07-22",
            "launch_count": 0,
            "paywall": {
                "active": paywall_active,
                "stripe_url": stripe_url,
                "unlock_token": unlock_token_input
            }
        }
        tool_data[agent_category].append(new_agent)
        with open("config.json", "w") as f:
            json.dump(tool_data, f, indent=2)
        st.success(f"Agent '{agent_name}' added to '{agent_category}'.")

    # Divider for Edit Section
    st.divider()
    st.subheader("✏️ Edit Existing Agent")

    edit_category = st.selectbox("Select Category", list(tool_data.keys()), key="edit_category")
    edit_agent_names = [agent["name"] for agent in tool_data[edit_category]]

    if edit_agent_names:
        agent_to_edit = st.selectbox("Select Agent", edit_agent_names, key="agent_to_edit")
        selected_index = edit_agent_names.index(agent_to_edit)
        agent_data = tool_data[edit_category][selected_index]

        # Editable fields pre-filled
        edit_name = st.text_input("Agent Name", value=agent_data["name"], key="edit_name")
        edit_desc = st.text_area("Description", value=agent_data["desc"], key="edit_desc")
        edit_link = st.text_input("Tool Launch Link", value=agent_data["link"], key="edit_link")
        edit_img = st.text_input("Avatar Image URL", value=agent_data["image"], key="edit_img")
        edit_badge = st.text_input("Badge (emoji)", value=agent_data.get("badge", ""), key="edit_badge")
        edit_paywall_active = st.checkbox("Premium Tool?", value=agent_data.get("paywall", {}).get("active", False), key="edit_pw")
        edit_stripe_url = st.text_input("Stripe Checkout URL", value=agent_data.get("paywall", {}).get("stripe_url", ""), key="edit_stripe") if edit_paywall_active else ""
        edit_unlock_token = st.text_input("Temporary Unlock Token", value=agent_data.get("paywall", {}).get("unlock_token", ""), key="edit_token") if edit_paywall_active else ""

        if st.button("💾 Update Agent"):
            updated_agent = {
                "name": edit_name,
                "desc": edit_desc,
                "link": edit_link,
                "image": edit_img,
                "badge": edit_badge,
                "category": edit_category,
                "updated": "2025-07-22",
                "launch_count": agent_data.get("launch_count", 0),
                "paywall": {
                    "active": edit_paywall_active,
                    "stripe_url": edit_stripe_url,
                    "unlock_token": edit_unlock_token
                }
            }

            tool_data[edit_category][selected_index] = updated_agent
            with open("config.json", "w") as f:
                json.dump(tool_data, f, indent=2)
            st.success(f"Agent '{edit_name}' updated successfully.")
    else:
        st.info("No agents found in this category.")

    # --- Tab 2: Upload Avatar (Base64 helper) ---
    with tab2:
        st.subheader("Upload Avatar")
        file = st.file_uploader("Upload PNG/JPG", type=["png", "jpg", "jpeg"])
        if file:
            st.image(file, width=120)
            b64 = base64.b64encode(file.read()).decode()
            st.text_area("Base64 Preview (first 200 chars)", b64[:200] + "...")

    # --- Tab 3: Trigger GHL ---
    with tab3:
        st.subheader("Trigger GHL Tag (optional)")
        email = st.text_input("Lead Email")
        tag = st.text_input("Tag to Apply")
        if st.button("📨 Send Tag (Simulated)"):
            st.success(f"Tag '{tag}' sent to {email} (simulated)")

    # --- Tab 4: Export Config JSON ---
    with tab4:
        st.subheader("Download Agent Config")
        st.download_button("📄 Export JSON", data=json.dumps(tool_data, indent=2), file_name="tool_data.json")

# ---------- Footer ----------
st.markdown("---")
st.markdown("🚀 Powered by [28 Foot Marketing](https://28footmarketing.com)")
