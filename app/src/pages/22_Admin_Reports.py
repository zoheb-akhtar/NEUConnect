import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

st.title("Reported Issues by Users")
st.write("Review and resolve user-reported issues")

current_admin_id = int(st.session_state.get('user_id', 1))

status_filter = st.selectbox('Filter by Status', ['All', 'pending', 'reviewed', 'solved'])

try:
    params = {}
    if status_filter != 'All':
        params['status'] = status_filter
    
    response = requests.get('http://web-api:4000/reports', params=params)
    
    if response.status_code == 200:
        reports = response.json()
        
        if reports:
            st.write(f"**{len(reports)} reports found**")
            st.write('')
            
            for report in reports:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(f"Report #{report.get('report_id')}")
                        st.write(f"**Reporter:** {report.get('reporter_type').title()} ID {report.get('reporter_id')}")
                        st.write(f"**Reported User:** {report.get('reported_user_type').title()} ID {report.get('reported_user_id')}")
                        st.write(f"**Reason:** {report.get('reason', 'No reason provided')}")
                        st.caption(f"Reported: {report.get('date_reported', 'N/A')}")
                        
                        current_status = report.get('status', 'pending')
                        if current_status == 'pending':
                            st.warning('⏳ Pending Review')
                        elif current_status == 'reviewed':
                            st.info('👀 Under Review')
                        elif current_status == 'solved':
                            st.success('✅ Resolved')
                    
                    with col2:
                        st.write('')
                        st.write('')
                        
                        if current_status == 'pending':
                            if st.button('Mark as Reviewed', key=f"review_{report['report_id']}", 
                                       use_container_width=True):
                                update_data = {
                                    'status': 'reviewed',
                                    'admin_id': current_admin_id
                                }
                                update_response = requests.put(
                                    f"http://web-api:4000/reports/{report['report_id']}", 
                                    json=update_data
                                )
                                if update_response.status_code == 200:
                                    st.success('Marked as reviewed')
                                    st.rerun()
                                else:
                                    st.error('Failed to update')
                        
                        if current_status in ['pending', 'reviewed']:
                            if st.button('✅ Resolve', key=f"resolve_{report['report_id']}", 
                                       type='primary', use_container_width=True):
                                update_data = {
                                    'status': 'solved',
                                    'admin_id': current_admin_id
                                }
                                update_response = requests.put(
                                    f"http://web-api:4000/reports/{report['report_id']}", 
                                    json=update_data
                                )
                                if update_response.status_code == 200:
                                    st.success('Report resolved!')
                                    st.rerun()
                                else:
                                    st.error('Failed to resolve')
                    
                    st.divider()
        else:
            st.info(f'No {status_filter} reports' if status_filter != 'All' else 'No reports found')
    else:
        st.error('Failed to load reports')

except Exception as e:
    st.error(f'Error: {str(e)}')

st.write('')
st.write('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('← Back to Dashboard', use_container_width=True):
        st.switch_page('pages/20_Admin_Home.py')
with col2:
    if st.button('View Applications', use_container_width=True):
        st.switch_page('pages/21_Admin_Applications.py')