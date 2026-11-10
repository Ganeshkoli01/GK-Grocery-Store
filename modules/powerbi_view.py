"""
GK GROCERY STORE – In-App Power BI Integration Guide Viewer
"""

import streamlit as st
from config import POWERBI_DIR


def render_powerbi_guide():
    """Renders the Power BI guide directly inside Streamlit."""
    st.markdown(
        """
        <div class="brand-header-box">
            <div>
                <div class="brand-title">📊 Microsoft Power BI Modeling & DAX Guide</div>
                <div class="brand-subtitle">Step-by-step instructions for building commercial Power BI dashboards from GK Grocery Store data</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    guide_path = POWERBI_DIR / "powerbi_guide.md"
    if guide_path.exists():
        with open(guide_path, "r", encoding="utf-8") as f:
            guide_md = f.read()
        st.markdown(guide_md)
    else:
        st.error("Power BI guide document not found.")

