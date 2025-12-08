import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

logger.info("Loading System Administrator Dashboard")
st.title('System Administrator Dashboard')
st.write(f"Welcome, {st.session_state.get('first_name', 'Admin')}!")
st.write("Use the tools below to manage users, review reports, and monitor platform health.")

st.divider()

st.subheader("Admin Overview Metrics")

try:
    dashboard_response = requests.get('http://web-api:4000/admin/dashboard')
    
    if dashboard_response.status_code == 200:
        metrics = dashboard_response.json()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            applications_response = requests.get('http://web-api:4000/applications?status=pending')
            pending_apps = 0
            if applications_response.status_code == 200:
                pending_apps = len(applications_response.json())
            st.metric("Pending Applications", pending_apps)
            st.caption("Students/Alumni awaiting admin approval")
        
        with col2:
            reports_response = requests.get('http://web-api:4000/reports?status=pending')
            pending_reports = 0
            if reports_response.status_code == 200:
                pending_reports = len(reports_response.json())
            st.metric("Open Reports", pending_reports)
            st.caption("Flagged issues requiring review")
        
        with col3:
            st.metric("Active Connections", metrics.get('total_connections', 0))
            st.caption("Current mentorship relationships")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pending Applications", "Error")
        with col2:
            st.metric("Open Reports", "Error")
        with col3:
            st.metric("Active Connections", "Error")
except Exception as e:
    st.error(f"Error loading metrics: {str(e)}")

st.divider()

st.subheader("Admin Tools")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.write("**Review Applications**")
    st.caption("Approve or reject new user applications")
    if st.button('Go to Applications', type='primary', use_container_width=True):
        st.switch_page('pages/21_Admin_Applications.py')

with c2:
    st.write("**Review Reports**")
    st.caption("Reply to or resolve user-reported issues")
    if st.button('Go to Reports', type='primary', use_container_width=True):
        st.switch_page('pages/22_Admin_Reports.py')

with c3:
    st.write("**System Stats**")
    st.caption("High-level platform activity and health metrics")
    if st.button('View System Stats', type='primary', use_container_width=True):
        st.switch_page('pages/23_Admin_System_Stats.py')

with c4:
    st.write("**Community Guidelines**")
    st.caption("Manage platform rules and guidelines")
    if st.button('Manage Guidelines', type='primary', use_container_width=True):
        st.switch_page('pages/24_Admin_Guidelines.py')