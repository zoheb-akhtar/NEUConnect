import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Student')}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

current_student_id = int(st.session_state.get('user_id', 1))

try:
    conn_response = requests.get(f'http://web-api:4000/connections?student_id={current_student_id}')
    if conn_response.status_code == 200:
        all_connections = conn_response.json()
        active_connections = len([c for c in all_connections if c.get('status') == 'accepted'])
        pending_requests = len([c for c in all_connections if c.get('status') == 'pending'])
    else:
        active_connections = 0
        pending_requests = 0
    
    sessions_response = requests.get(f'http://web-api:4000/sessions?student_id={current_student_id}')
    if sessions_response.status_code == 200:
        all_sessions = sessions_response.json()
        today = datetime.now().date()
        upcoming_sessions = 0
        for s in all_sessions:
            try:
                session_date_str = s.get('session_date', '')
                if 'GMT' in session_date_str:
                    session_date = datetime.strptime(session_date_str, '%a, %d %b %Y %H:%M:%S GMT').date()
                else:
                    session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()
                if session_date >= today and s.get('status') != 'cancelled':
                    upcoming_sessions += 1
            except:
                pass
    else:
        upcoming_sessions = 0
except:
    active_connections = 0
    pending_requests = 0
    upcoming_sessions = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Connections", active_connections)
with col2:
    st.metric("Upcoming Sessions", upcoming_sessions)
with col3:
    st.metric("Connection Requests", f"{pending_requests} Pending")

st.write('')
st.write('')

if st.button(' Browse Alumni Mentors', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/31_Students_Browse_Alumni.py')

if st.button(' My Sessions', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/32_Students_My_Sessions.py')

if st.button(' My Profile', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/33_Students_My_Profile.py')

if st.button(' Job Postings', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/34_Students_Job_Postings.py')

st.write('')
st.write('')
st.write('###  Recent Activity')

try:
    recent_accepted = sorted(
        [c for c in all_connections if c.get('status') == 'accepted'],
        key=lambda x: x.get('date_connected', ''),
        reverse=True
    )[:2]
    
    for conn in recent_accepted:
        try:
            alumni_response = requests.get(f'http://web-api:4000/alumni/{conn.get("alumni_id")}')
            if alumni_response.status_code == 200:
                alumni = alumni_response.json()
                st.info(f'✅ Connection accepted by {alumni.get("name")} ({alumni.get("current_role")})')
        except:
            pass
    
    recent_declined = sorted(
        [c for c in all_connections if c.get('status') == 'rejected'],
        key=lambda x: x.get('date_connected', ''),
        reverse=True
    )[:2]
    
    for conn in recent_declined:
        try:
            alumni_response = requests.get(f'http://web-api:4000/alumni/{conn.get("alumni_id")}')
            if alumni_response.status_code == 200:
                alumni = alumni_response.json()
                st.warning(f'❌ Connection declined by {alumni.get("name")}')
        except:
            pass
    
    recent_sessions = sorted(
        [s for s in all_sessions if s.get('status') == 'scheduled'],
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )[:2]
    
    for session in recent_sessions:
        try:
            alumni_response = requests.get(f'http://web-api:4000/alumni/{session.get("alumni_id")}')
            if alumni_response.status_code == 200:
                alumni = alumni_response.json()
                st.info(f' Session scheduled with {alumni.get("name")} - {session.get("topic", "No topic")}')
        except:
            pass
    
    if not recent_accepted and not recent_declined and not recent_sessions:
        st.caption('No recent activity')
        
except Exception as e:
    st.caption('Unable to load recent activity')