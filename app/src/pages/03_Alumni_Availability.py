import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import time

st.set_page_config(layout='wide')
SideBarLinks()

st.title('📅 My Availability')
st.write('Manage your weekly availability for student meetings')

current_alumni_id = int(st.session_state.get('user_id', 1))

try:
    response = requests.get(f'http://web-api:4000/alumni/{current_alumni_id}/availability')
    
    if response.status_code == 200:
        availability_slots = response.json()
        
        st.write('### Current Availability Schedule')
        
        if availability_slots:
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            slots_by_day = {day: [] for day in days_order}
            
            for slot in availability_slots:
                day = slot.get('day_of_week')
                if day in slots_by_day:
                    slots_by_day[day].append(slot)
            
            for day in days_order:
                day_slots = slots_by_day[day]
                if day_slots:
                    with st.expander(f"📅 {day} ({len(day_slots)} slots)", expanded=True):
                        for slot in day_slots:
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.write(f"⏰ {slot.get('start_time', 'N/A')} - {slot.get('end_time', 'N/A')}")
                            
                            with col2:
                                if st.button('🗑️ Delete', key=f"delete_{slot['schedule_id']}", 
                                           use_container_width=True):
                                    delete_response = requests.delete(
                                        f"http://web-api:4000/alumni/{current_alumni_id}/availability/{slot['schedule_id']}"
                                    )
                                    if delete_response.status_code == 200:
                                        st.success('Slot deleted!')
                                        st.rerun()
                                    else:
                                        st.error('Failed to delete slot')
                            
                            st.divider()
        else:
            st.info('No availability slots set. Add your first availability slot below!')
        
        st.write('')
        st.write('---')
        st.write('### 📅 Upcoming Meetings')
        
        try:
            sessions_response = requests.get(f'http://web-api:4000/sessions?alumni_id={current_alumni_id}&status=scheduled')
            if sessions_response.status_code == 200:
                upcoming_sessions = sessions_response.json()
                
                if upcoming_sessions:
                    from datetime import datetime
                    today = datetime.now().date()
                    future_sessions = []
                    
                    for s in upcoming_sessions:
                        try:
                            session_date_str = s.get('session_date', '')
                            if 'GMT' in session_date_str:
                                session_date = datetime.strptime(session_date_str, '%a, %d %b %Y %H:%M:%S GMT').date()
                            else:
                                session_date = datetime.strptime(session_date_str, '%Y-%m-%d').date()
                            if session_date >= today:
                                future_sessions.append(s)
                        except:
                            future_sessions.append(s)
                    
                    future_sessions.sort(key=lambda x: x.get('session_date', ''))
                    
                    if future_sessions:
                        for session in future_sessions[:5]:
                            student_id = session.get('student_id')
                            
                            try:
                                student_response = requests.get(f'http://web-api:4000/students/{student_id}')
                                if student_response.status_code == 200:
                                    student = student_response.json()
                                    
                                    with st.container():
                                        st.write(f"**{session.get('session_date')}** at **{session.get('session_time', 'TBD')}**")
                                        st.write(f"👤 {student.get('name')} - {student.get('major_name', 'N/A')}")
                                        st.write(f"📌 Topic: {session.get('topic', 'No topic')}")
                                        st.divider()
                            except:
                                pass
                        
                        if len(future_sessions) > 5:
                            st.caption(f'+ {len(future_sessions) - 5} more upcoming sessions')
                    else:
                        st.info('No upcoming meetings scheduled')
                else:
                    st.info('No upcoming meetings scheduled')
            else:
                st.warning('Unable to load sessions')
        except Exception as e:
            st.warning(f'Unable to load upcoming meetings: {str(e)}')
        
        st.write('')
        st.write('---')
        st.write('### ➕ Add New Availability Slot')
        
        with st.form('add_availability_form'):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                day_of_week = st.selectbox(
                    'Day of Week',
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                )
            
            with col2:
                start_time = st.time_input('Start Time', value=time(9, 0))
            
            with col3:
                end_time = st.time_input('End Time', value=time(17, 0))
            
            st.write('')
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                submitted = st.form_submit_button('Add Availability', type='primary', use_container_width=True)
            
            if submitted:
                if start_time >= end_time:
                    st.error('End time must be after start time')
                else:
                    availability_data = {
                        'day_of_week': day_of_week,
                        'start_time': start_time.strftime('%H:%M:%S'),
                        'end_time': end_time.strftime('%H:%M:%S')
                    }
                    
                    try:
                        create_response = requests.post(
                            f'http://web-api:4000/alumni/{current_alumni_id}/availability',
                            json=availability_data
                        )
                        if create_response.status_code == 201:
                            st.success('✅ Availability slot added!')
                            st.rerun()
                        else:
                            st.error('Failed to add availability slot')
                    except Exception as e:
                        st.error(f'Error: {str(e)}')
        
        st.write('')
        st.write('---')
        st.write('### Availability Status')
        
        try:
            alumni_response = requests.get(f'http://web-api:4000/alumni/{current_alumni_id}')
            if alumni_response.status_code == 200:
                alumni_data = alumni_response.json()
                current_status = alumni_data.get('availability_status', 'unavailable')
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write('Set your overall availability status:')
                    new_status = st.radio(
                        'Status',
                        ['available', 'unavailable'],
                        index=0 if current_status == 'available' else 1,
                        horizontal=True
                    )
                    
                    if current_status == 'available':
                        st.success('✅ You are currently available for mentorship')
                    else:
                        st.warning('⏸️ You are currently unavailable for mentorship')
                
                with col2:
                    st.write('')
                    st.write('')
                    if st.button('Update Status', type='primary', use_container_width=True):
                        update_data = {'availability_status': new_status}
                        update_response = requests.put(
                            f'http://web-api:4000/alumni/{current_alumni_id}',
                            json=update_data
                        )
                        if update_response.status_code == 200:
                            st.success('Status updated!')
                            st.rerun()
                        else:
                            st.error('Failed to update status')
        except Exception as e:
            st.warning(f'Unable to load current status: {str(e)}')
    
    else:
        st.error('Failed to load availability schedule')

except Exception as e:
    st.error(f'Error: {str(e)}')
    logger.error(f'Error in Alumni_Availability: {str(e)}')

st.write('')
st.write('---')
st.write('### Quick Actions')
col1, col2 = st.columns(2)
with col1:
    if st.button('👤 My Profile', use_container_width=True):
        st.switch_page('pages/01_Alumni_Profile.py')
with col2:
    if st.button('🎓 Browse Students', use_container_width=True):
        st.switch_page('pages/41_Alumni_Browse_Students.py')

st.write('')
st.info("""
💡 **Tips for Managing Availability:**
- Set specific time blocks when you're available for student meetings
- Students can only schedule meetings during your available slots
- Update your status to "unavailable" when you need a break
- You can add multiple time slots per day
""")