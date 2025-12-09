import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

if not st.session_state.get('authenticated'):
    st.switch_page('Home.py')

if st.session_state.get('role') != 'administrator':
    st.switch_page('Home.py')

st.title("Community Guidelines Management")
st.write("Create, edit, and manage community guidelines")

current_admin_id = int(st.session_state.get('user_id', 1))

st.write('### Add New Guideline')

with st.form('new_guideline_form'):
    guideline_text = st.text_area('Guideline Text', 
                                  placeholder='e.g., Respect other members of the community',
                                  height=100)
    
    submitted = st.form_submit_button('Add Guideline', type='primary', use_container_width=True)
    
    if submitted:
        if guideline_text:
            guideline_data = {
                'guideline_text': guideline_text,
                'created_by_admin_id': current_admin_id
            }
            
            try:
                create_response = requests.post('http://web-api:4000/guidelines', json=guideline_data)
                if create_response.status_code == 201:
                    st.success('✅ Guideline added successfully!')
                    st.rerun()
                else:
                    st.error('Failed to add guideline')
            except Exception as e:
                st.error(f'Error: {str(e)}')
        else:
            st.error('Please enter guideline text')

st.write('')
st.write('---')
st.write('### Current Community Guidelines')

try:
    response = requests.get('http://web-api:4000/guidelines')
    
    if response.status_code == 200:
        guidelines = response.json()
        
        if guidelines:
            st.write(f"**{len(guidelines)} total guidelines**")
            st.write('')
            
            for guideline in guidelines:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.session_state.get(f'editing_{guideline["guideline_id"]}'):
                            with st.form(f'edit_form_{guideline["guideline_id"]}'):
                                new_text = st.text_area('Edit Guideline', 
                                                       value=guideline.get('guideline_text', ''),
                                                       key=f'edit_text_{guideline["guideline_id"]}')
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    save = st.form_submit_button('Save', type='primary', use_container_width=True)
                                with col_cancel:
                                    cancel = st.form_submit_button('Cancel', use_container_width=True)
                                
                                if save:
                                    update_data = {'guideline_text': new_text}
                                    update_response = requests.put(
                                        f"http://web-api:4000/guidelines/{guideline['guideline_id']}", 
                                        json=update_data
                                    )
                                    if update_response.status_code == 200:
                                        st.success('Guideline updated!')
                                        st.session_state[f'editing_{guideline["guideline_id"]}'] = False
                                        st.rerun()
                                    else:
                                        st.error('Failed to update')
                                
                                if cancel:
                                    st.session_state[f'editing_{guideline["guideline_id"]}'] = False
                                    st.rerun()
                        else:
                            st.write(f"**{guideline.get('guideline_text', 'N/A')}**")
                            st.caption(f"Created: {guideline.get('date_created', 'N/A')}")
                    
                    with col2:
                        if not st.session_state.get(f'editing_{guideline["guideline_id"]}'):
                            st.write('')
                            
                            if st.button('✏️ Edit', key=f"edit_{guideline['guideline_id']}", 
                                       use_container_width=True):
                                st.session_state[f'editing_{guideline["guideline_id"]}'] = True
                                st.rerun()
                            
                            if st.button('🗑️ Delete', key=f"delete_{guideline['guideline_id']}", 
                                       use_container_width=True):
                                delete_response = requests.delete(
                                    f"http://web-api:4000/guidelines/{guideline['guideline_id']}"
                                )
                                if delete_response.status_code == 200:
                                    st.success('Guideline deleted')
                                    st.rerun()
                                else:
                                    st.error('Failed to delete')
                    
                    st.divider()
        else:
            st.info('No community guidelines set yet')
    else:
        st.error('Failed to load guidelines')

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