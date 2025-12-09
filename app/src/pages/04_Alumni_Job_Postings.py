import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://web-api:4000"

st.set_page_config(page_title="Manage Job Postings - NU Connect", page_icon="💼", layout="wide")

if 'user_id' not in st.session_state:
    st.warning("Please log in as an alumni to manage job postings.")
    st.stop()

alumni_id = st.session_state['user_id']

st.title("💼 Manage Job Postings")

tab1, tab2 = st.tabs(["📝 Create New Posting", "📋 My Postings"])

with tab1:
    st.markdown("### Post a New Job Opportunity")
    
    with st.form("create_job_posting"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title*", placeholder="e.g., Software Engineer Intern")
            preferred_major = st.text_input("Preferred Major", placeholder="e.g., Computer Science")
        
        with col2:
            preferred_year = st.number_input("Preferred Year", 
                                            min_value=2020, 
                                            max_value=2030, 
                                            step=1,
                                            value=None,
                                            help="Graduation year")
            status = st.selectbox("Status", ["active", "closed"], index=0)
        
        description = st.text_area("Job Description*", 
                                   placeholder="Describe the role, responsibilities, requirements, and what the candidate will be doing...",
                                   height=200)
        
        submit_button = st.form_submit_button("Post Job", use_container_width=True)
        
        if submit_button:
            if not job_title or not description:
                st.error("Please fill in all required fields (marked with *)")
            else:
                job_data = {
                    "alumni_id": alumni_id,
                    "title": job_title,
                    "description": description,
                    "status": status
                }
                
                if preferred_major:
                    job_data["preferred_major"] = preferred_major
                if preferred_year:
                    job_data["preferred_year"] = preferred_year
                
                try:
                    response = requests.post(f"{API_BASE_URL}/job-postings", json=job_data)
                    
                    if response.status_code == 201:
                        st.success("✅ Job posting created successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Failed to create job posting. Status code: {response.status_code}")
                        if response.text:
                            st.error(f"Error details: {response.text}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")

with tab2:
    st.markdown("### Your Posted Jobs")
    
    try:
        response = requests.get(f"{API_BASE_URL}/job-postings", params={"alumni_id": alumni_id})
        
        if response.status_code == 200:
            my_postings = response.json()
            
            if not my_postings:
                st.info("You haven't posted any jobs yet. Create your first posting in the 'Create New Posting' tab!")
            else:
                st.markdown(f"**Total Postings:** {len(my_postings)}")
                st.markdown("---")
                
                for job in my_postings:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"### {job.get('title', 'Untitled Position')}")
                            if job.get('preferred_major'):
                                st.markdown(f"**Preferred Major:** {job['preferred_major']}")
                            if job.get('preferred_year'):
                                st.markdown(f"**Preferred Year:** {job['preferred_year']}")
                        
                        with col2:
                            status = job.get('status', 'active')
                            status_color = "🟢" if status == "active" else "🔴"
                            st.markdown(f"{status_color} **{status.upper()}**")
                            
                            if st.button("Toggle Status", key=f"toggle_{job.get('posting_id')}", 
                                       use_container_width=True):
                                new_status = "closed" if status == "active" else "active"
                                try:
                                    update_response = requests.put(
                                        f"{API_BASE_URL}/job-postings/{job.get('posting_id')}",
                                        json={"status": new_status}
                                    )
                                    
                                    if update_response.status_code == 200:
                                        st.success(f"Status updated to {new_status}!")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to update status. Status: {update_response.status_code}")
                                
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Error updating posting: {str(e)}")
                        
                        with col3:
                            if st.button("🗑️ Delete", key=f"delete_{job.get('posting_id')}", 
                                       type="secondary", use_container_width=True):
                                try:
                                    delete_response = requests.delete(
                                        f"{API_BASE_URL}/job-postings/{job.get('posting_id')}"
                                    )
                                    
                                    if delete_response.status_code == 200:
                                        st.success("Job posting deleted successfully!")
                                        st.rerun()
                                    else:
                                        st.error(f"Failed to delete posting. Status: {delete_response.status_code}")
                                
                                except requests.exceptions.RequestException as e:
                                    st.error(f"Error deleting posting: {str(e)}")
                        
                        st.markdown(f"**Description:**")
                        st.markdown(job.get('description', 'No description provided.'))
                        
                        if job.get('created_at'):
                            try:
                                created_date = datetime.fromisoformat(str(job['created_at']))
                                st.caption(f"📅 Posted: {created_date.strftime('%B %d, %Y')}")
                            except:
                                st.caption(f"📅 Posted: {job['created_at']}")
                        
                        st.markdown("---")
        else:
            st.error(f"Failed to load your postings. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {str(e)}")
        st.info("Please make sure the API server is running.")