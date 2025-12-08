import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

st.title('🎓 Student Directory')
st.write('Browse student profiles and connect with potential mentees')

# Get current alumni ID from session state
current_alumni_id = int(st.session_state.get('user_id', 1))

# Search and filter section
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input('🔍 Search by name or major', placeholder='e.g., Computer Science, Engineering')

with col2:
    # Graduation year filter
    years = ['All Years', '2025', '2026', '2027', '2028', '2029']
    year_filter = st.selectbox('Graduation Year', years)

with col3:
    # Major filter (simplified list)
    majors = ['All Majors', 'Computer Science', 'Data Science', 'Software Engineering', 
              'Business Administration', 'Engineering']
    major_filter = st.selectbox('Major', majors)

st.write('')

# Fetch student data from API
try:
    # Build query parameters
    params = {}
    if year_filter != 'All Years':
        params['graduation_year'] = year_filter
    
    response = requests.get('http://web-api:4000/students', params=params)
    
    if response.status_code == 200:
        students_list = response.json()
        
        # Client-side search filter
        filtered_students = students_list
        
        if search_query:
            filtered_students = [s for s in filtered_students if 
                               search_query.lower() in s.get('name', '').lower() or
                               search_query.lower() in s.get('profile_summary', '').lower()]
        
        st.write(f'**{len(filtered_students)} students found**')
        st.write('')
        
        # Display student cards
        if filtered_students:
            for student in filtered_students:
                with st.container():
                    col_left, col_right = st.columns([4, 1])
                    
                    with col_left:
                        st.subheader(f"🎓 {student.get('name', 'N/A')}")
                        
                        # Get major name if available
                        major_info = student.get('major_name', 'N/A')
                        st.write(f"**Major:** {major_info}")
                        st.write(f"**Graduation Year:** {student.get('graduation_year', 'N/A')}")
                        
                        # Get location if available
                        if student.get('city') and student.get('state'):
                            st.write(f"📍 {student.get('city')}, {student.get('state')}")
                        
                        # Profile summary
                        if student.get('profile_summary'):
                            with st.expander('📝 About'):
                                st.write(student['profile_summary'])
                        else:
                            st.caption('No profile summary available')
                    
                    with col_right:
                        st.write('')
                        st.write('')
                        
                        # Check if already connected
                        is_connected = False
                        try:
                            conn_response = requests.get(f"http://web-api:4000/connections?alumni_id={current_alumni_id}&student_id={student['student_id']}")
                            if conn_response.status_code == 200:
                                connections = conn_response.json()
                                is_connected = len(connections) > 0
                        except:
                            pass
                        
                        if is_connected:
                            st.success('Connected ✓')
                            
                            # Offer to schedule meeting
                            if st.button('📅 Schedule Meeting', key=f"schedule_{student['student_id']}", 
                                       type='primary', use_container_width=True):
                                st.session_state['schedule_with_student'] = student['student_id']
                                st.session_state['student_name_selected'] = student.get('name', 'N/A')
                                st.rerun()
                        else:
                            if st.button('Connect', key=f"connect_{student['student_id']}", 
                                       type='primary', use_container_width=True):
                                # Create connection request (from alumni side)
                                connection_data = {
                                    'student_id': student['student_id'],
                                    'alumni_id': current_alumni_id,
                                    'status': 'accepted'  # Alumni can auto-accept
                                }
                                create_response = requests.post('http://web-api:4000/connections', 
                                                               json=connection_data)
                                if create_response.status_code == 201:
                                    st.success('Connected with student!')
                                    st.rerun()
                                else:
                                    st.error('Failed to connect')
                            
                            st.caption('Connect to schedule meetings')
                    
                    # Show scheduling form if this student is selected
                    if st.session_state.get('schedule_with_student') == student['student_id']:
                        st.write('---')
                        st.write(f"### 📅 Schedule Meeting with {st.session_state.get('student_name_selected')}")
                        
                        with st.form(f"schedule_form_{student['student_id']}"):
                            from datetime import date, time as dt_time
                            
                            meeting_date = st.date_input('Meeting Date', min_value=date.today())
                            meeting_time = st.time_input('Meeting Time')
                            meeting_topic = st.text_input('Topic', placeholder='e.g., Resume review, Career guidance')
                            meeting_notes = st.text_area('Notes', placeholder='What would you like to discuss?')
                            
                            col_submit, col_cancel = st.columns(2)
                            with col_submit:
                                submitted = st.form_submit_button('Schedule Meeting', type='primary', use_container_width=True)
                            with col_cancel:
                                canceled = st.form_submit_button('Cancel', use_container_width=True)
                            
                            if submitted:
                                session_data = {
                                    'student_id': student['student_id'],
                                    'alumni_id': current_alumni_id,
                                    'session_date': meeting_date.strftime('%Y-%m-%d'),
                                    'session_time': meeting_time.strftime('%H:%M:%S'),
                                    'topic': meeting_topic,
                                    'notes': meeting_notes,
                                    'status': 'scheduled'
                                }
                                
                                try:
                                    session_response = requests.post('http://web-api:4000/sessions', json=session_data)
                                    if session_response.status_code == 201:
                                        st.success('✅ Meeting scheduled successfully!')
                                        st.session_state['schedule_with_student'] = None
                                        st.rerun()
                                    else:
                                        st.error('Failed to schedule meeting')
                                except Exception as e:
                                    st.error(f'Error: {str(e)}')
                            
                            if canceled:
                                st.session_state['schedule_with_student'] = None
                                st.rerun()
                    
                    st.divider()
        else:
            st.info('No students found matching your filters')
    
    else:
        st.error('Failed to load student data')
        
except Exception as e:
    st.error(f'Error connecting to server: {str(e)}')
    logger.error(f'Error in Browse_Students: {str(e)}')

# Quick actions at bottom
st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2 = st.columns(2)
with col1:
    if st.button('👤 My Profile', use_container_width=True):
        st.switch_page('pages/01_Alumni_Profile.py')
with col2:
    if st.button('📅 My Availability', use_container_width=True):
        st.switch_page('pages/03_Alumni_Availability.py')