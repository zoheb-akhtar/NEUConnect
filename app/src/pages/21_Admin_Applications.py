import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

st.title("Pending Applications to Review")
st.write("Review and approve or reject student applications")

current_admin_id = int(st.session_state.get('user_id', 1))

try:
    response = requests.get('http://web-api:4000/applications?status=pending')
    
    if response.status_code == 200:
        applications = response.json()
        
        if applications:
            st.write(f"**{len(applications)} pending applications**")
            st.write('')
            
            for app in applications:
                student_id = app.get('student_id')
                
                try:
                    student_response = requests.get(f'http://web-api:4000/students/{student_id}')
                    if student_response.status_code == 200:
                        student = student_response.json()
                        
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.subheader(f"👤 {student.get('name', 'N/A')}")
                                st.write(f"**Email:** {student.get('email', 'N/A')}")
                                st.write(f"**Major:** {student.get('major_name', 'N/A')}")
                                st.write(f"**Graduation Year:** {student.get('graduation_year', 'N/A')}")
                                st.caption(f"Applied: {app.get('submission_date', 'N/A')}")
                                
                                if student.get('profile_summary'):
                                    with st.expander('Profile Summary'):
                                        st.write(student['profile_summary'])
                            
                            with col2:
                                st.write('')
                                st.write('')
                                
                                col_approve, col_reject = st.columns(2)
                                
                                with col_approve:
                                    if st.button('✅ Approve', key=f"approve_{app['application_id']}", 
                                               use_container_width=True, type='primary'):
                                        update_data = {
                                            'status': 'approved',
                                            'admin_id': current_admin_id
                                        }
                                        update_response = requests.put(
                                            f"http://web-api:4000/applications/{app['application_id']}", 
                                            json=update_data
                                        )
                                        if update_response.status_code == 200:
                                            st.success('Application approved!')
                                            st.rerun()
                                        else:
                                            st.error('Failed to approve')
                                
                                with col_reject:
                                    if st.button('❌ Reject', key=f"reject_{app['application_id']}", 
                                               use_container_width=True):
                                        update_data = {
                                            'status': 'rejected',
                                            'admin_id': current_admin_id
                                        }
                                        update_response = requests.put(
                                            f"http://web-api:4000/applications/{app['application_id']}", 
                                            json=update_data
                                        )
                                        if update_response.status_code == 200:
                                            st.success('Application rejected')
                                            st.rerun()
                                        else:
                                            st.error('Failed to reject')
                            
                            st.divider()
                except Exception as e:
                    st.error(f'Error loading application details: {str(e)}')
        else:
            st.info('No pending applications')
    else:
        st.error('Failed to load applications')

except Exception as e:
    st.error(f'Error: {str(e)}')

st.write('')
st.write('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('← Back to Dashboard', use_container_width=True):
        st.switch_page('pages/20_Admin_Home.py')
with col2:
    if st.button('View Reports', use_container_width=True):
        st.switch_page('pages/22_Admin_Reports.py')