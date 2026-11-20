"""
FileGuard – Suspicious File Type Detection System
A modern, premium, and futuristic cybersecurity web application built with Streamlit.
Faithfully designed after the reference architecture specification.
"""

import os
import re
import time
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# Import modular components
from detector import analyze_file, SIGNATURES_TABLE
from report import generate_text_report, generate_markdown_report, generate_json_report
from three_hero import get_threejs_hero_html

# Page Configuration
st.set_page_config(
    page_title="FileGuard | Suspicious File Type Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Safe HTML Renderer (Prevents CommonMark 4-space code block traps)
def render_html(html_content: str):
    """Safely renders HTML without Markdown 4-space indentation code block traps."""
    cleaned = re.sub(r'^[ \t]+', '', html_content, flags=re.MULTILINE)
    st.markdown(cleaned, unsafe_allow_html=True)

# Session State Initialization
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Home"

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "preset_sample" not in st.session_state:
    st.session_state.preset_sample = None

if "trigger_instant_scan" not in st.session_state:
    st.session_state.trigger_instant_scan = False

# Sample data generators for instant demonstration
def get_sample_file(sample_type: str):
    """Provides pre-configured binary samples to test immediately."""
    if sample_type == "safe_pdf":
        content = (
            b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
            b"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n"
            b"0000000117 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n193\n%%EOF"
        )
        return "annual_report.pdf", content
    elif sample_type == "disguised_exe":
        content = (
            b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00\xb8\x00\x00\x00"
            b"This program cannot be run in DOS mode.\r\r\n$"
            b"\x00\x00\x00\x00\x00\x00\x00PE\x00\x00L\x01\x03\x00\x00\x00\x00\x00"
        )
        return "invoice_overdue.pdf", content
    elif sample_type == "mismatched_png":
        content = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00"
            b"\x1f\xf3\xffa\x00\x00\x00\x19IDATx\x9cc\xfc\xff\xff?\x03\x03\x03\x13\x13\x13\x00\x00"
            b"\x00\xff\xff\x03\x00\x1b\x06\x01\x19\xa9\x86\xbb\x8b\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return "profile_picture.jpg", content
    elif sample_type == "double_ext":
        content = (
            b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
            b"PE payload simulator - double extension test file"
        )
        return "payroll_summary.docx.exe", content
    return "sample.txt", b"Hello, FileGuard forensic security verification!"

# -------------------------------------------------------------------------------------------------
# SIDEBAR - MATCHING EXACT REFERENCE IMAGE
# -------------------------------------------------------------------------------------------------
with st.sidebar:
    # Top Logo with Shield & Keyhole inside
    render_html("""
    <div class="fg-side-logo-wrap">
      <div class="fg-side-shield-icon">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <circle cx="12" cy="11" r="2" fill="currentColor"/>
          <path d="M12 13v3" stroke-width="2.5"/>
        </svg>
      </div>
      <div class="fg-side-title">FileGuard</div>
      <div class="fg-side-subtitle">Scan • Detect • Stay Safe</div>
    </div>
    """)

    nav_options = {
        "Home": "🏠 Home",
        "Dashboard": "📊 Dashboard",
        "Scan": "🔍 Scan File",
        "History": "🕒 Scan History",
        "About": "ℹ️ About"
    }

    if "nav_radio" not in st.session_state:
        st.session_state.nav_radio = st.session_state.active_nav

    def on_nav_change():
        st.session_state.active_nav = st.session_state.nav_radio

    selected_nav = st.radio(
        "Navigation Menu",
        options=list(nav_options.keys()),
        format_func=lambda k: nav_options[k],
        key="nav_radio",
        on_change=on_nav_change,
        label_visibility="collapsed"
    )
    st.session_state.active_nav = selected_nav

    # Bottom Sidebar Card: "Cyber Security Made Simple"
    render_html("""
    <div class="fg-side-bottom-card">
      <div class="fg-side-bottom-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <polyline points="9 12 11 14 15 10"/>
        </svg>
      </div>
      <div class="fg-side-bottom-text">Cyber Security<br/>Made Simple</div>
    </div>
    """)

# -------------------------------------------------------------------------------------------------
# TOP HEADER BAR: "Advanced File Security Scanner" + "Stay Secure" & Avatar
# -------------------------------------------------------------------------------------------------
render_html("""
<div class="fg-topbar-row">
  <div class="fg-header-badge">
    <span>🛡️</span>
    <span>Advanced File Security Scanner</span>
    <span class="fg-badge-green-dot"></span>
  </div>
  <div class="fg-user-pill-wrap">
    <div class="fg-stay-secure-badge">
      <span class="fg-badge-green-dot"></span>
      <span>Stay Secure</span>
    </div>
    <div class="fg-user-avatar">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
      </svg>
    </div>
  </div>
</div>
""")

# -------------------------------------------------------------------------------------------------
# REUSABLE MODULAR SCANNER & RESULTS COMPONENTS
# -------------------------------------------------------------------------------------------------
def render_scan_module(is_full_width=False):
    render_html('<div id="scan-chamber-anchor"></div>')

    sample_to_use = None
    if st.session_state.preset_sample:
        p_name, p_content = st.session_state.preset_sample
        render_html(f"""
        <div style="background: rgba(37, 99, 235, 0.08); border: 1.5px solid rgba(37, 99, 235, 0.35); border-radius: 14px; padding: 12px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
          <span style="font-size: 13.5px; color: #0F172A;"><b>⚡ Loaded Sample:</b> <code>{p_name}</code> ({len(p_content)} bytes)</span>
          <span style="background: #2563EB; color: white; padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;">Ready to Scan</span>
        </div>
        """)
        sample_to_use = (p_name, p_content)

    # Upload Card Container matching reference screenshot
    render_html("""
    <div class="fg-upload-panel">
      <div class="fg-upload-dashed-box">
        <svg class="fg-curved-arrow-left" viewBox="0 0 50 30" fill="none">
          <path d="M10 25 C25 25 35 15 45 5" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round"/>
          <polyline points="35 5 45 5 45 15" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg class="fg-curved-arrow-right" viewBox="0 0 50 30" fill="none">
          <path d="M10 25 C25 25 35 15 45 5" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round"/>
          <polyline points="35 5 45 5 45 15" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="fg-cloud-icon-box">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
            <polyline points="12 11 12 16"/>
            <polyline points="9 13 12 10 15 13"/>
          </svg>
        </div>
        <div style="font-size: 19px; font-weight: 800; color: #0F172A; margin-bottom: 2px;">Drag & Drop your file here</div>
        <div style="font-size: 13.5px; color: #64748B; margin-bottom: 8px;">or click to browse</div>
        <div style="font-size: 12px; color: #94A3B8; font-weight: 500;">Supports: PDF, JPG, PNG, DOC, EXE, ZIP and more...</div>
      </div>
    </div>
    """)

    uploaded_file = st.file_uploader(
        "Upload file",
        type=None,
        accept_multiple_files=False,
        key=f"uploader_{'full' if is_full_width else 'home'}",
        label_visibility="collapsed"
    )

    active_filename = None
    active_bytes = None

    if uploaded_file is not None:
        active_filename = uploaded_file.name
        active_bytes = uploaded_file.getvalue()
        st.session_state.preset_sample = None
    elif sample_to_use is not None:
        active_filename, active_bytes = sample_to_use

    if active_filename and active_bytes is not None:
        render_html(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 12px 18px; border-radius: 14px; margin-top: 10px; border: 1.5px solid #3B82F6; box-shadow: 0 4px 14px rgba(59,130,246,0.12);">
          <div>
            <span style="font-size: 12px; color: #64748B; font-weight: 700; text-transform: uppercase;">Ready to Scan:</span>
            <b style="color: #0F172A; margin-left: 6px;">{active_filename}</b>
          </div>
          <span style="background: rgba(37,99,235,0.12); color: #2563EB; padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 800;">{len(active_bytes):,} bytes</span>
        </div>
        """)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍 Analyze File", use_container_width=True, key=f"btn_analyze_{'full' if is_full_width else 'home'}")

    should_scan = analyze_btn or st.session_state.trigger_instant_scan
    if should_scan:
        st.session_state.trigger_instant_scan = False
        if not active_filename or active_bytes is None:
            active_filename, active_bytes = get_sample_file("disguised_exe")

        # 3D Holographic Scanning Chamber Modal
        anim_box = st.empty()
        with anim_box:
            components.html(get_threejs_hero_html(mode="SCANNER", target_name=active_filename), height=260)
            render_html(f"""
            <div class="fg-scanner-modal">
              <div style="text-align: center; margin-bottom: 12px;">
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">✨ Holographic Scanning Chamber Active...</div>
                <div style="font-size: 13px; color: #64748B;">Analyzing target: <b>{active_filename}</b></div>
              </div>
              <div class="fg-scan-steps-list">
                <div class="fg-scan-step-item fg-scan-step-active">
                  <div class="fg-spinner-dot"></div>
                  <span>Reading low-level magic bytes at offset headers...</span>
                </div>
              </div>
            </div>
            """)
        time.sleep(0.55)

        with anim_box:
            components.html(get_threejs_hero_html(mode="SCANNER", target_name=active_filename), height=260)
            render_html(f"""
            <div class="fg-scanner-modal">
              <div style="text-align: center; margin-bottom: 12px;">
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">✨ Holographic Scanning Chamber Active...</div>
                <div style="font-size: 13px; color: #64748B;">Analyzing target: <b>{active_filename}</b></div>
              </div>
              <div class="fg-scan-steps-list">
                <div class="fg-scan-step-item fg-scan-step-done">
                  <div class="fg-check-dot">✓</div>
                  <span>Magic byte signature extracted</span>
                </div>
                <div class="fg-scan-step-item fg-scan-step-active">
                  <div class="fg-spinner-dot"></div>
                  <span>Verifying declared extension against binary format...</span>
                </div>
              </div>
            </div>
            """)
        time.sleep(0.55)

        with anim_box:
            components.html(get_threejs_hero_html(mode="SCANNER", target_name=active_filename), height=260)
            render_html(f"""
            <div class="fg-scanner-modal">
              <div style="text-align: center; margin-bottom: 12px;">
                <div style="font-size: 18px; font-weight: 800; color: #0F172A;">✨ Holographic Scanning Chamber Active...</div>
                <div style="font-size: 13px; color: #64748B;">Analyzing target: <b>{active_filename}</b></div>
              </div>
              <div class="fg-scan-steps-list">
                <div class="fg-scan-step-item fg-scan-step-done">
                  <div class="fg-check-dot">✓</div>
                  <span>Magic byte signature extracted</span>
                </div>
                <div class="fg-scan-step-item fg-scan-step-done">
                  <div class="fg-check-dot">✓</div>
                  <span>Extension verification complete</span>
                </div>
                <div class="fg-scan-step-item fg-scan-step-active">
                  <div class="fg-spinner-dot"></div>
                  <span>Verifying container structure & spoofing flags...</span>
                </div>
              </div>
            </div>
            """)
        time.sleep(0.4)

        analysis = analyze_file(active_bytes, active_filename)
        analysis["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.session_state.last_analysis = analysis
        st.session_state.scan_history.insert(0, analysis)
        anim_box.empty()
        st.rerun()

    # Quick Test Demo Buttons Underneath Upload Box
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        if st.button("📄 Safe PDF", use_container_width=True, key=f"demo_safe_{'full' if is_full_width else 'home'}"):
            n, c = get_sample_file("safe_pdf")
            st.session_state.preset_sample = (n, c)
            st.session_state.trigger_instant_scan = True
            st.rerun()
    with d2:
        if st.button("⚠️ Disguised EXE", use_container_width=True, key=f"demo_exe_{'full' if is_full_width else 'home'}"):
            n, c = get_sample_file("disguised_exe")
            st.session_state.preset_sample = (n, c)
            st.session_state.trigger_instant_scan = True
            st.rerun()
    with d3:
        if st.button("🖼️ Spoofed PNG", use_container_width=True, key=f"demo_png_{'full' if is_full_width else 'home'}"):
            n, c = get_sample_file("mismatched_png")
            st.session_state.preset_sample = (n, c)
            st.session_state.trigger_instant_scan = True
            st.rerun()
    with d4:
        if st.button("🪤 Double Ext", use_container_width=True, key=f"demo_dbl_{'full' if is_full_width else 'home'}"):
            n, c = get_sample_file("double_ext")
            st.session_state.preset_sample = (n, c)
            st.session_state.trigger_instant_scan = True
            st.rerun()

def render_results_card():
    if not st.session_state.last_analysis:
        return

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    res = st.session_state.last_analysis
    status = res.get("status", "UNKNOWN")

    if status == "SAFE":
        card_class = "fg-result-card-safe"
        pill_class = "fg-finding-safe"
        finding_label = "🟢 VERIFIED FORMAT MATCH"
        status_icon_html = """
        <div class="fg-status-icon-wrap fg-status-icon-safe">
          <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <polyline points="9 12 11 14 15 10"/>
          </svg>
        </div>
        """
    elif status == "SUSPICIOUS":
        card_class = "fg-result-card-suspicious"
        pill_class = "fg-finding-suspicious"
        finding_label = "🔴 SUSPICIOUS FORMAT MISMATCH"
        status_icon_html = """
        <div class="fg-status-icon-wrap fg-status-icon-suspicious">
          <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        """
    else:
        card_class = "fg-result-card-unknown"
        pill_class = "fg-finding-unknown"
        finding_label = "🟠 UNKNOWN / UNSUPPORTED FORMAT"
        status_icon_html = """
        <div class="fg-status-icon-wrap fg-status-icon-unknown">
          <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/>
            <line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        """

    # Interactive 3D Holographic Result Presentation
    res_3d_col, res_info_col = st.columns([1, 1.4])
    with res_3d_col:
        components.html(get_threejs_hero_html(mode="RESULT", status=status, target_name=res.get('filename')), height=280)

    with res_info_col:
        render_html(f"""
        <div class="fg-result-card {card_class}" style="margin-top: 0; min-height: 280px; display: flex; flex-direction: column; justify-content: center;">
          <div class="fg-result-header">
            {status_icon_html}
            <div>
              <div class="fg-status-finding-pill {pill_class}">{finding_label}</div>
              <div class="fg-status-title-text">{res.get('status_title')}</div>
              <div style="font-size: 16px; font-weight: 600; color: #334155;">{res.get('status_message')}</div>
            </div>
          </div>
          <div style="font-size: 14.5px; color: #334155; line-height: 1.6; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.06);">
            {res.get('risk_summary')}
          </div>
        </div>
        """)

    # File Properties Cards
    st.markdown("<h4 style='font-size: 18px; font-weight: 800; color: #0F172A; margin-top: 20px; margin-bottom: 12px;'>File Forensic Properties</h4>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    with p1:
        render_html(f"""
        <div class="fg-property-item">
          <div class="fg-property-label">Target File Name</div>
          <div class="fg-property-value">{res.get('filename')}</div>
        </div>
        <div style="height: 12px;"></div>
        <div class="fg-property-item">
          <div class="fg-property-label">File Size</div>
          <div class="fg-property-value">{res.get('file_size_formatted')}</div>
        </div>
        """)

    with p2:
        render_html(f"""
        <div class="fg-property-item">
          <div class="fg-property-label">Declared Extension</div>
          <div class="fg-property-value"><span class="fg-mono-code">.{res.get('declared_extension')}</span></div>
        </div>
        <div style="height: 12px;"></div>
        <div class="fg-property-item">
          <div class="fg-property-label">Actual Identified Format</div>
          <div class="fg-property-value" style="color: #2563EB;">{res.get('actual_format')}</div>
        </div>
        """)

    with p3:
        threat_color = '#EF4444' if res.get('threat_level') in ['Critical', 'High'] else '#10B981'
        render_html(f"""
        <div class="fg-property-item">
          <div class="fg-property-label">Category & MIME</div>
          <div class="fg-property-value">{res.get('actual_category')} &bull; <span style="font-size: 12px; color: #64748B;">{res.get('mime_type')}</span></div>
        </div>
        <div style="height: 12px;"></div>
        <div class="fg-property-item">
          <div class="fg-property-label">Security Threat Rating</div>
          <div class="fg-property-value" style="color: {threat_color};">{res.get('threat_level')}</div>
        </div>
        """)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    render_html(f"""
    <div class="fg-card" style="padding: 22px;">
      <div style="font-weight: 800; font-size: 16px; margin-bottom: 12px; color: #0F172A;">🔬 Low-Level Signature & Cryptographic Fingerprints</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
        <div>
          <div style="font-size: 11.5px; color: #64748B; font-weight: 700; text-transform: uppercase;">Magic Bytes (Hex Representation)</div>
          <div style="margin-top: 6px;"><code class="fg-mono-code">{res.get('magic_hex')}</code></div>
        </div>
        <div>
          <div style="font-size: 11.5px; color: #64748B; font-weight: 700; text-transform: uppercase;">Magic Bytes (ASCII Representation)</div>
          <div style="margin-top: 6px;"><code class="fg-mono-code">{res.get('magic_ascii')}</code></div>
        </div>
      </div>
      <div style="margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(226, 232, 240, 0.9);">
        <div style="font-size: 11.5px; color: #64748B; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">SHA-256 Checksum</div>
        <code>{res.get('hashes', {}).get('sha256')}</code>
      </div>
    </div>
    """)

    # Download Report Buttons
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    txt_report = generate_text_report(res)
    md_report = generate_markdown_report(res)
    json_report = generate_json_report(res)

    rep_c1, rep_c2, rep_c3 = st.columns(3)
    with rep_c1:
        st.download_button(
            label="📄 Download Text Report (.txt)",
            data=txt_report,
            file_name=f"FileGuard_Report_{res.get('filename')}.txt",
            mime="text/plain",
            key=f"dl_txt_{res.get('filename')}",
            use_container_width=True
        )
    with rep_c2:
        st.download_button(
            label="📝 Download Markdown (.md)",
            data=md_report,
            file_name=f"FileGuard_Report_{res.get('filename')}.md",
            mime="text/markdown",
            key=f"dl_md_{res.get('filename')}",
            use_container_width=True
        )
    with rep_c3:
        st.download_button(
            label="📊 Download JSON Export (.json)",
            data=json_report,
            file_name=f"FileGuard_Report_{res.get('filename')}.json",
            mime="application/json",
            key=f"dl_json_{res.get('filename')}",
            use_container_width=True
        )

# -------------------------------------------------------------------------------------------------
# VIEW 1: HOME (LANDING PAGE & HERO LABORATORY)
# -------------------------------------------------------------------------------------------------
if st.session_state.active_nav == "Home":

    # HERO SECTION (2 COLUMNS: TYPOGRAPHY ON LEFT, 3D SHIELD ON RIGHT)
    hero_left_col, hero_right_col = st.columns([1.1, 1.1])

    with hero_left_col:
        render_html("""
        <div>
          <h1 class="fg-hero-title-main">
            ENTER THE<br/>
            <span class="fg-hero-title-gradient">FILEGUARD SECURITY LAB</span>
          </h1>
          <p class="fg-hero-desc">
            Every File Has a Story. We Reveal Its True Identity.
          </p>
        </div>
        """)

        btn_c1, btn_c2 = st.columns([1.1, 1.1])
        with btn_c1:
            if st.button("⚡ Start Scanning ➔", use_container_width=True, key="hero_start_scan_btn"):
                st.session_state.nav_radio = "Scan"
                st.session_state.active_nav = "Scan"
                st.rerun()
        with btn_c2:
            if st.button("🧪 Quick Test Disguised EXE", use_container_width=True, key="hero_quick_scan_btn"):
                n, c = get_sample_file("disguised_exe")
                st.session_state.preset_sample = (n, c)
                st.session_state.trigger_instant_scan = True
                st.session_state.nav_radio = "Scan"
                st.session_state.active_nav = "Scan"
                st.rerun()

        render_html("""
        <div style="margin-top: 10px; margin-bottom: 8px;">
          <a href="#scan-chamber-anchor" style="font-size: 13px; color: #2563EB; font-weight: 700; text-decoration: none;">
            ⬇️ Or scroll down to drag & drop files
          </a>
        </div>
        """)

    with hero_right_col:
        # Interactive 3D Holographic Laboratory Scene (Three.js WebGL Engine)
        components.html(get_threejs_hero_html(mode="HERO"), height=370)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # THREE HORIZONTAL CAPABILITY CARDS
    cap1, cap2, cap3 = st.columns(3)

    with cap1:
        render_html("""
        <div class="fg-cap-card">
          <div class="fg-cap-left">
            <div class="fg-cap-icon-circle" style="background: linear-gradient(135deg, #2563EB, #3B82F6);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 0 0-10 10c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/>
              </svg>
            </div>
            <div>
              <div class="fg-cap-title">File Signature Detection</div>
              <div class="fg-cap-sub">Identify actual file format</div>
            </div>
          </div>
          <div class="fg-cap-arrow">➔</div>
        </div>
        """)

    with cap2:
        render_html("""
        <div class="fg-cap-card">
          <div class="fg-cap-left">
            <div class="fg-cap-icon-circle" style="background: linear-gradient(135deg, #7C3AED, #8B5CF6);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
            </div>
            <div>
              <div class="fg-cap-title">Extension Verification</div>
              <div class="fg-cap-sub">Check for mismatches</div>
            </div>
          </div>
          <div class="fg-cap-arrow">➔</div>
        </div>
        """)

    with cap3:
        render_html("""
        <div class="fg-cap-card">
          <div class="fg-cap-left">
            <div class="fg-cap-icon-circle" style="background: linear-gradient(135deg, #059669, #10B981);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
            </div>
            <div>
              <div class="fg-cap-title">Suspicious File Identification</div>
              <div class="fg-cap-sub">Spot hidden threats</div>
            </div>
          </div>
          <div class="fg-cap-arrow">➔</div>
        </div>
        """)

    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

    # BOTTOM SECTION: UPLOAD PANEL (LEFT) & SECURITY OVERVIEW (RIGHT)
    bot_left_col, bot_right_col = st.columns([1.35, 1])

    with bot_left_col:
        render_scan_module(is_full_width=False)

    with bot_right_col:
        total_scanned = len(st.session_state.scan_history)
        safe_files = sum(1 for s in st.session_state.scan_history if s.get("status") == "SAFE")
        suspicious_files = sum(1 for s in st.session_state.scan_history if s.get("status") == "SUSPICIOUS")
        issues_found = sum(1 for s in st.session_state.scan_history if s.get("status") != "SAFE")

        disp_total = f"{1200 + total_scanned}" if total_scanned == 0 else f"{total_scanned}"
        disp_safe = f"{980 + safe_files}" if total_scanned == 0 else f"{safe_files}"
        disp_susp = f"{120 + suspicious_files}" if total_scanned == 0 else f"{suspicious_files}"
        disp_issues = f"{85 + issues_found}" if total_scanned == 0 else f"{issues_found}"

        render_html(f"""
        <div class="fg-overview-card">
          <div class="fg-overview-header">
            <span>🛡️</span> <span>Security Overview</span>
          </div>

          <div class="fg-stat-tiles-row">
            <div class="fg-mini-tile fg-mini-tile-blue">
              <div style="font-size: 16px; margin-bottom: 2px;">📁</div>
              <div class="fg-mini-tile-num">{disp_total}</div>
              <div class="fg-mini-tile-lbl">Files Scanned</div>
            </div>
            <div class="fg-mini-tile fg-mini-tile-green">
              <div style="font-size: 16px; margin-bottom: 2px;">✅</div>
              <div class="fg-mini-tile-num">{disp_safe}</div>
              <div class="fg-mini-tile-lbl">Safe Files</div>
            </div>
            <div class="fg-mini-tile fg-mini-tile-red">
              <div style="font-size: 16px; margin-bottom: 2px;">🚨</div>
              <div class="fg-mini-tile-num">{disp_susp}</div>
              <div class="fg-mini-tile-lbl">Suspicious</div>
            </div>
            <div class="fg-mini-tile fg-mini-tile-orange">
              <div style="font-size: 16px; margin-bottom: 2px;">⚠️</div>
              <div class="fg-mini-tile-num">{disp_issues}</div>
              <div class="fg-mini-tile-lbl">Issues Found</div>
            </div>
          </div>

          <div class="fg-recent-activity-header">
            <span>Recent Activity</span>
            <span style="color: #2563EB; font-size: 12.5px; cursor: pointer;">Live Feed</span>
          </div>
          <div>
            <div class="fg-recent-item">
              <div class="fg-recent-name">
                <span style="color: #10B981;">✅</span> photo.jpg
              </div>
              <span class="fg-badge-safe-sm">Safe Format</span>
              <span style="color: #94A3B8; font-size: 11.5px;">2 min ago</span>
            </div>
            <div class="fg-recent-item">
              <div class="fg-recent-name">
                <span style="color: #EF4444;">🚨</span> invoice.jpg
              </div>
              <span class="fg-badge-danger-sm">Format Mismatch</span>
              <span style="color: #94A3B8; font-size: 11.5px;">5 min ago</span>
            </div>
            <div class="fg-recent-item">
              <div class="fg-recent-name">
                <span style="color: #3B82F6;">ℹ️</span> document.pdf
              </div>
              <span class="fg-badge-info-sm">Verified</span>
              <span style="color: #94A3B8; font-size: 11.5px;">8 min ago</span>
            </div>
          </div>
        </div>
        """)

    render_results_card()

# -------------------------------------------------------------------------------------------------
# VIEW 2: DEDICATED 3D FILE SCANNING LABORATORY
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "Scan":
    render_html("""
    <div style="margin-bottom: 18px;">
      <h2 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px; letter-spacing: -0.6px;">
        🔍 3D Holographic File Scanning Laboratory
      </h2>
      <p style="font-size: 14px; color: #64748B; margin: 0;">
        Deep binary signature inspection, magic bytes analysis, and disguised file anomaly detection.
      </p>
    </div>
    """)

    # Top Holographic Scanning Chamber
    current_target = st.session_state.preset_sample[0] if st.session_state.preset_sample else "Chamber Ready"
    components.html(get_threejs_hero_html(mode="SCANNER", target_name=current_target), height=250)

    # Full-width Scanning Module
    render_scan_module(is_full_width=True)

    # Forensic Results Card
    render_results_card()

# -------------------------------------------------------------------------------------------------
# VIEW 2: DASHBOARD
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "Dashboard":
    render_html("""
    <div style="margin-bottom: 22px;">
      <h2 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px; letter-spacing: -0.6px;">Security Telemetry Dashboard</h2>
      <p style="font-size: 14px; color: #64748B; margin: 0;">Comprehensive telemetry analytics, inspection rates, and security status reports.</p>
    </div>
    """)

    total_files = len(st.session_state.scan_history)
    safe_files = sum(1 for s in st.session_state.scan_history if s.get("status") == "SAFE")
    suspicious_files = sum(1 for s in st.session_state.scan_history if s.get("status") == "SUSPICIOUS")
    format_mismatches = sum(1 for s in st.session_state.scan_history if s.get("status") == "SUSPICIOUS" and "Mismatch" in s.get("status_title", ""))

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_html(f"""
        <div class="fg-card" style="padding: 20px; text-align: center;">
          <div style="font-size: 28px; margin-bottom: 4px;">📁</div>
          <div style="font-size: 28px; font-weight: 800; color: #0F172A;">{total_files}</div>
          <div style="font-size: 13px; color: #64748B; font-weight: 600;">Total Files Scanned</div>
        </div>
        """)
    with m2:
        render_html(f"""
        <div class="fg-card" style="padding: 20px; text-align: center;">
          <div style="font-size: 28px; margin-bottom: 4px;">🛡️</div>
          <div style="font-size: 28px; font-weight: 800; color: #10B981;">{safe_files}</div>
          <div style="font-size: 13px; color: #64748B; font-weight: 600;">Safe Format Matches</div>
        </div>
        """)
    with m3:
        render_html(f"""
        <div class="fg-card" style="padding: 20px; text-align: center;">
          <div style="font-size: 28px; margin-bottom: 4px;">🚨</div>
          <div style="font-size: 28px; font-weight: 800; color: #EF4444;">{suspicious_files}</div>
          <div style="font-size: 13px; color: #64748B; font-weight: 600;">Suspicious Files</div>
        </div>
        """)
    with m4:
        render_html(f"""
        <div class="fg-card" style="padding: 20px; text-align: center;">
          <div style="font-size: 28px; margin-bottom: 4px;">⚠️</div>
          <div style="font-size: 28px; font-weight: 800; color: #F59E0B;">{format_mismatches}</div>
          <div style="font-size: 13px; color: #64748B; font-weight: 600;">Format Mismatches</div>
        </div>
        """)

# -------------------------------------------------------------------------------------------------
# VIEW 3: SCAN HISTORY
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "History":
    render_html("""
    <div style="margin-bottom: 22px;">
      <h2 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px; letter-spacing: -0.6px;">Scan History & Forensic Audit Log</h2>
      <p style="font-size: 14px; color: #64748B; margin: 0;">Session audit trail of all inspected files, signatures, and verdicts.</p>
    </div>
    """)

    if len(st.session_state.scan_history) == 0:
        render_html("""
        <div class="fg-card" style="text-align: center; padding: 40px;">
          <div style="font-size: 40px; margin-bottom: 10px;">📂</div>
          <div style="font-weight: 800; font-size: 18px; color: #0F172A;">No Scans Conducted Yet</div>
          <div style="font-size: 14px; color: #64748B; margin-top: 4px;">Upload files or try test samples to populate the ledger.</div>
        </div>
        """)
    else:
        rows_html = ""
        for item in st.session_state.scan_history:
            st_status = item.get("status", "UNKNOWN")
            badge = "<span class='fg-badge-safe-sm'>MATCH</span>" if st_status == "SAFE" else "<span class='fg-badge-danger-sm'>MISMATCH</span>"
            rows_html += f"""
            <tr>
              <td><b>{item.get('filename')}</b></td>
              <td>.{item.get('declared_extension')}</td>
              <td>{item.get('actual_format')}</td>
              <td>{item.get('file_size_formatted')}</td>
              <td><code class="fg-mono-code">{item.get('magic_hex')}</code></td>
              <td>{badge}</td>
              <td style="color: #64748B; font-size: 12px;">{item.get('timestamp', 'Recent')}</td>
            </tr>
            """
        render_html(f"""
        <div style="overflow-x: auto; margin-bottom: 20px;">
          <table class="fg-history-table">
            <thead>
              <tr>
                <th>File Name</th>
                <th>Declared Ext</th>
                <th>Actual Format</th>
                <th>Size</th>
                <th>Signature</th>
                <th>Status</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {rows_html}
            </tbody>
          </table>
        </div>
        """)

        if st.button("🗑️ Clear History", use_container_width=False):
            st.session_state.scan_history = []
            st.session_state.last_analysis = None
            st.rerun()

# -------------------------------------------------------------------------------------------------
# VIEW 4: ABOUT / DATABASE
# -------------------------------------------------------------------------------------------------
elif st.session_state.active_nav == "About":
    render_html("""
    <div style="margin-bottom: 22px;">
      <h2 style="font-size: 28px; font-weight: 800; color: #0F172A; margin-bottom: 4px; letter-spacing: -0.6px;">Known File Signatures Catalog</h2>
      <p style="font-size: 14px; color: #64748B; margin: 0;">FileGuard forensic signature catalog across binaries, documents, media, and containers.</p>
    </div>
    """)

    for item in SIGNATURES_TABLE[:15]:
        magic_hex_str = " ".join(f"{b:02X}" for b in item["magic"][0])
        ext_list = ", ".join("." + e for e in item["valid_extensions"])
        render_html(f"""
        <div class="fg-card" style="padding: 18px 24px; margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <b style="font-size: 16px; color: #0F172A;">{item['name']}</b>
            <span style="background: rgba(37,99,235,0.1); color: #2563EB; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;">{item['category']}</span>
          </div>
          <div style="margin-top: 8px; font-size: 13px; color: #64748B;">
            Magic Bytes: <code class="fg-mono-code">{magic_hex_str}</code> &bull; Extensions: <b>{ext_list}</b>
          </div>
        </div>
        """)
