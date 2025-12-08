import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

st.title("System Statistics & Metrics")
st.write("Monitor platform health and activity")

try:
    dashboard_response = requests.get('http://web-api:4000/admin/dashboard')
    
    if dashboard_response.status_code == 200:
        metrics = dashboard_response.json()
        
        st.write('### Platform Overview')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", metrics.get('total_students', 0))
        with col2:
            st.metric("Total Alumni", metrics.get('total_alumni', 0))
        with col3:
            st.metric("Total Connections", metrics.get('total_connections', 0))
        with col4:
            st.metric("Active Sessions", metrics.get('active_sessions', 0))
        
        st.write('')
        st.write('### Pending Actions')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Pending Applications", metrics.get('pending_applications', 0))
        with col2:
            st.metric("Pending Reports", metrics.get('pending_reports', 0))
        
        st.write('')
        st.write('---')
        st.write('### Connection Status Breakdown')
        
        try:
            conn_response = requests.get('http://web-api:4000/connections')
            if conn_response.status_code == 200:
                all_connections = conn_response.json()
                
                pending = len([c for c in all_connections if c.get('status') == 'pending'])
                accepted = len([c for c in all_connections if c.get('status') == 'accepted'])
                rejected = len([c for c in all_connections if c.get('status') == 'rejected'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Pending Connections", pending)
                with col2:
                    st.metric("Accepted Connections", accepted)
                with col3:
                    st.metric("Rejected Connections", rejected)
        except:
            st.warning('Unable to load connection breakdown')
        
        st.write('')
        st.write('---')
        st.write('### Session Status Breakdown')
        
        try:
            sessions_response = requests.get('http://web-api:4000/sessions')
            if sessions_response.status_code == 200:
                all_sessions = sessions_response.json()
                
                scheduled = len([s for s in all_sessions if s.get('status') == 'scheduled'])
                completed = len([s for s in all_sessions if s.get('status') == 'completed'])
                cancelled = len([s for s in all_sessions if s.get('status') == 'cancelled'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Scheduled Sessions", scheduled)
                with col2:
                    st.metric("Completed Sessions", completed)
                with col3:
                    st.metric("Cancelled Sessions", cancelled)
        except:
            st.warning('Unable to load session breakdown')
    
    else:
        st.error('Failed to load dashboard metrics')

except Exception as e:
    st.error(f'Error: {str(e)}')

st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('← Back to Dashboard', use_container_width=True):
        st.switch_page('pages/20_Admin_Home.py')
with col2:
    if st.button('Review Applications', use_container_width=True):
        st.switch_page('pages/21_Admin_Applications.py')
with col3:
    if st.button('Review Reports', use_container_width=True):
        st.switch_page('pages/22_Admin_Reports.py')