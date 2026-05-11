"""
Streamlit Web Interface for Email Verification Tool
Provides real-time feedback as each verification phase completes.
"""

import streamlit as st
import time
from email_verifier import EmailVerifier
import json

# Page configuration
st.set_page_config(
    page_title="Email Verification Tool",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px 0;
    }
    .status-valid {
        background-color: #90EE90;
        color: #003300;
    }
    .status-invalid {
        background-color: #FFB6C6;
        color: #660000;
    }
    .status-undetermined {
        background-color: #FFE680;
        color: #665500;
    }
    .status-pending {
        background-color: #ADD8E6;
        color: #003366;
    }
    .phase-container {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #ccc;
    }
    .phase-passed {
        background-color: #f0f9ff;
        border-left-color: #22c55e;
    }
    .phase-failed {
        background-color: #fef2f2;
        border-left-color: #ef4444;
    }
    .phase-pending {
        background-color: #fffbf0;
        border-left-color: #f59e0b;
    }
    .phase-greylisted {
        background-color: #fef9f3;
        border-left-color: #d97706;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("✉️ Email Verification Tool")
st.markdown("**Lightweight • Open-Source • Zero Paid APIs**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    check_web_presence = st.checkbox("Check Web Presence (Phase 4)", value=True, 
                                     help="Checks Gravatar and public records")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool verifies email addresses through 4 phases:
    
    1. **Syntax Validation** - RFC 5322 compliance
    2. **Domain/MX Records** - DNS MX lookup
    3. **SMTP Handshake** - Port 25 connection test
    4. **Web Presence** - Gravatar/public profile check
    """)

# Main content area
st.markdown("### Enter Email Address")

# Input and verify button in columns
col1, col2 = st.columns([4, 1])

with col1:
    email_input = st.text_input(
        "Email Address",
        placeholder="example@domain.com",
        label_visibility="collapsed"
    )

with col2:
    verify_button = st.button("🔍 Verify", use_container_width=True)

st.markdown("---")

# Verification results
if verify_button and email_input:
    with st.spinner("Starting verification..."):
        verifier = EmailVerifier()
        result = verifier.verify(email_input, check_web_presence)
        
    # Display overall status at the top
    status_color_map = {
        "valid": "status-valid",
        "invalid": "status-invalid",
        "undetermined": "status-undetermined",
        "pending": "status-pending"
    }
    
    status_emoji_map = {
        "valid": "✅",
        "invalid": "❌",
        "undetermined": "⚠️",
        "unknown": "❓",
        "error": "⚠️"
    }
    
    status = result["overall_status"]
    status_html = f"""
    <div style="text-align: center; padding: 20px; background-color: #f9fafb; border-radius: 10px; margin: 20px 0;">
        <h2>{status_emoji_map.get(status, '❓')} Overall Status: <span class="status-badge {status_color_map.get(status, '')}">{status.upper()}</span></h2>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)
    
    # Display verification phases
    st.markdown("### 📋 Verification Phases")
    
    # Phase 1: Syntax Validation
    phase_1 = result["phase_1"]
    status_class = "phase-passed" if phase_1["status"] == "passed" else "phase-failed" if phase_1["status"] == "failed" else "phase-pending"
    
    st.markdown(f"""
    <div class="phase-container {status_class}">
        <h4>Phase 1: Syntax Validation</h4>
        <p><strong>Status:</strong> {phase_1['status'].upper()}</p>
        <p>{phase_1['message']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 2: Domain/MX Record Check
    phase_2 = result["phase_2"]
    status_class = "phase-passed" if phase_2["status"] == "passed" else "phase-failed" if phase_2["status"] == "failed" else "phase-pending"
    
    mx_display = ""
    if phase_2["mx_records"]:
        mx_display = "<p><strong>MX Records:</strong></p><ul>"
        for mx in phase_2["mx_records"]:
            mx_display += f"<li>{mx['host']} (Priority: {mx['priority']})</li>"
        mx_display += "</ul>"
    
    st.markdown(f"""
    <div class="phase-container {status_class}">
        <h4>Phase 2: Domain/MX Record Check</h4>
        <p><strong>Status:</strong> {phase_2['status'].upper()}</p>
        <p>{phase_2['message']}</p>
        {mx_display}
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 3: SMTP Handshake
    phase_3 = result["phase_3"]
    if phase_3["status"] == "passed":
        status_class = "phase-passed"
    elif phase_3["status"] in ("greylisted", "failed", "error"):
        status_class = "phase-failed"
    else:
        status_class = "phase-pending"
    
    server_info = f"<p><strong>Server:</strong> {phase_3['server']}</p>" if phase_3["server"] else ""
    
    st.markdown(f"""
    <div class="phase-container {status_class}">
        <h4>Phase 3: SMTP Handshake</h4>
        <p><strong>Status:</strong> {phase_3['status'].upper()}</p>
        <p>{phase_3['message']}</p>
        {server_info}
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 4: Web Presence (if enabled)
    if check_web_presence:
        phase_4 = result["phase_4"]
        status_class = "phase-passed" if phase_4["status"] in ("found", "passed") else "phase-pending"
        
        st.markdown(f"""
        <div class="phase-container {status_class}">
            <h4>Phase 4: Web Presence Search</h4>
            <p><strong>Status:</strong> {phase_4['status'].upper()}</p>
            <p>{phase_4['message']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced details expander
    with st.expander("📊 Raw JSON Results"):
        st.json(result)
    
    st.markdown("---")
    st.markdown("**💡 Tips:**")
    st.markdown("""
    - **Valid**: Email syntax is correct, domain exists, and inbox was accepted by mail server
    - **Invalid**: Email format is wrong, domain doesn't exist, or mail server rejected it
    - **Undetermined**: Domain exists but SMTP check was inconclusive (greylisting or connection issues)
    - **Greylisted**: Server temporarily rejected the recipient (anti-spam measure)
    """)

elif verify_button:
    st.error("Please enter an email address to verify.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
    🔒 <strong>Privacy Notice:</strong> This tool runs locally. No data is stored or sent to external servers (except DNS queries and MX server connections required for verification).<br>
    📖 <strong>Open Source:</strong> Built with dnspython, smtplib, and Streamlit. Zero paid APIs required.
</div>
""", unsafe_allow_html=True)
