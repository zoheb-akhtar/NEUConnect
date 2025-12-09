import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Alumni')}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# Get current alumni ID from session state
current_alumni_id = int(st.session_state.get('user_id', 1))

# Fetch real stats from API
try:
    # Get connections
    conn_response = requests.get(f'http://web-api:4000/connections?alumni_id={current_alumni_id}')
    if conn_response.status_code == 200:
        all_connections = conn_response.json()
        active_connections = len([c for c in all_connections if c.get('status') == 'accepted'])
        pending_requests = len([c for c in all_connections if c.get('status') == 'pending'])
    else:
        active_connections = 0
        pending_requests = 0
    
    # Get sessions
    sessions_response = requests.get(f'http://web-api:4000/sessions?alumni_id={current_alumni_id}')
    if sessions_response.status_code == 200:
        all_sessions = sessions_response.json()
        from datetime import datetime
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

# Quick stats section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Connections", active_connections)
with col2:
    st.metric("Upcoming Sessions", upcoming_sessions)
with col3:
    st.metric("Connection Requests", f"{pending_requests} Pending")

st.write('')

# Show pending connection requests if any exist
if pending_requests > 0:
    st.write('---')
    st.write('###  Pending Connection Requests')
    
    try:
        pending_conn = [c for c in all_connections if c.get('status') == 'pending']
        
        for conn in pending_conn[:3]:  # Show first 3
            student_id = conn.get('student_id')
            
            # Fetch student details
            try:
                student_response = requests.get(f'http://web-api:4000/students/{student_id}')
                if student_response.status_code == 200:
                    student = student_response.json()
                    
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**{student.get('name', 'N/A')}**")
                            st.write(f" {student.get('major_name', 'N/A')} • Class of {student.get('graduation_year', 'N/A')}")
                            if student.get('profile_summary'):
                                st.caption(student['profile_summary'][:100] + '...' if len(student['profile_summary']) > 100 else student['profile_summary'])
                        
                        with col2:
                            col_accept, col_decline = st.columns(2)
                            with col_accept:
                                if st.button('✅', key=f"accept_{conn['connection_id']}", 
                                           help='Accept', use_container_width=True):
                                    update_data = {'status': 'accepted'}
                                    update_response = requests.put(f"http://web-api:4000/connections/{conn['connection_id']}", 
                                                                  json=update_data)
                                    if update_response.status_code == 200:
                                        st.success('Connection accepted!')
                                        st.rerun()
                                    else:
                                        st.error('Failed to accept')
                            
                            with col_decline:
                                if st.button('❌', key=f"decline_{conn['connection_id']}", 
                                           help='Decline', use_container_width=True):
                                    update_data = {'status': 'rejected'}
                                    update_response = requests.put(f"http://web-api:4000/connections/{conn['connection_id']}", 
                                                                  json=update_data)
                                    if update_response.status_code == 200:
                                        st.success('Connection declined')
                                        st.rerun()
                                    else:
                                        st.error('Failed to decline')
                        
                        st.divider()
            except Exception as e:
                st.error(f'Error loading student: {str(e)}')
        
        if pending_requests > 3:
            st.caption(f'+ {pending_requests - 3} more requests')
    
    except Exception as e:
        st.error(f'Error loading connection requests: {str(e)}')

st.write('')
st.write('')

# Main action buttons
if st.button(' View Your Profile', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_Alumni_Profile.py')

if st.button(' View Student Profiles', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_Student_Profiles.py')

if st.button(' Configure Your Availability', 
             type='primary', 
             use_container_width=True):
    st.switch_page('pages/03_Alumni_Availability.py')

if st.button(' Job Postings', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/04_Alumni_Job_Postings.py')

# Recent activity section
st.write('')
st.write('')
st.write('###  Recent Activity')

try:
    # Show recently accepted connections (sorted by date)
    recent_accepted = sorted(
        [c for c in all_connections if c.get('status') == 'accepted'],
        key=lambda x: x.get('date_connected', ''),
        reverse=True
    )[:2]
    
    for conn in recent_accepted:
        try:
            student_response = requests.get(f'http://web-api:4000/students/{conn.get("student_id")}')
            if student_response.status_code == 200:
                student = student_response.json()
                st.info(f' Connected with {student.get("name")} ({student.get("major_name")})')
        except:
            pass
    
    # Show recently declined connections
    recent_declined = sorted(
        [c for c in all_connections if c.get('status') == 'rejected'],
        key=lambda x: x.get('date_connected', ''),
        reverse=True
    )[:2]
    
    for conn in recent_declined:
        try:
            student_response = requests.get(f'http://web-api:4000/students/{conn.get("student_id")}')
            if student_response.status_code == 200:
                student = student_response.json()
                st.warning(f' Declined connection with {student.get("name")}')
        except:
            pass
    
    # Show recent upcoming sessions
    if upcoming_sessions > 0:
        recent_sessions = sorted(
            [s for s in all_sessions if s.get('status') == 'scheduled'],
            key=lambda x: x.get('session_date', ''),
            reverse=True
        )[:2]
        
        for session in recent_sessions:
            try:
                student_response = requests.get(f'http://web-api:4000/students/{session.get("student_id")}')
                if student_response.status_code == 200:
                    student = student_response.json()
                    st.info(f' Upcoming session with {student.get("name")} - {session.get("topic", "No topic")}')
            except:
                pass
    
    # Show message if no activity
    if not recent_accepted and not recent_declined and upcoming_sessions == 0:
        st.caption('No recent activity')
        
except Exception as e:
    st.caption('Unable to load recent activity')