import streamlit as st
import requests
from datetime import datetime

API_BASE_URL = "http://web-api:4000"

st.set_page_config(page_title="Job Postings - NU Connect", page_icon="💼", layout="wide")

if 'user_id' not in st.session_state:
    st.warning("Please log in to view job postings.")
    st.stop()

st.title("💼 Job Postings")
st.markdown("Browse job and internship opportunities posted by alumni mentors")

try:
    response = requests.get(f"{API_BASE_URL}/job-postings")
    
    if response.status_code == 200:
        job_postings = response.json()
        
        if not job_postings:
            st.info("No job postings available at this time. Check back soon!")
        else:
            search_col, filter_col1, filter_col2 = st.columns([2, 1, 1])
            
            with search_col:
                search_term = st.text_input("🔍 Search jobs", placeholder="Search by title or description...")
            
            with filter_col1:
                all_majors = ["All"] + list(set([job.get('preferred_major') for job in job_postings if job.get('preferred_major')]))
                selected_major = st.selectbox("Preferred Major", all_majors)
            
            with filter_col2:
                all_statuses = ["All"] + list(set([job.get('status', 'active') for job in job_postings]))
                selected_status = st.selectbox("Status", all_statuses)
            
            filtered_jobs = job_postings
            
            if search_term:
                filtered_jobs = [
                    job for job in filtered_jobs
                    if search_term.lower() in job.get('title', '').lower() or
                       search_term.lower() in job.get('description', '').lower()
                ]
            
            if selected_major != "All":
                filtered_jobs = [job for job in filtered_jobs if job.get('preferred_major') == selected_major]
            
            if selected_status != "All":
                filtered_jobs = [job for job in filtered_jobs if job.get('status') == selected_status]
            
            st.markdown(f"### Found {len(filtered_jobs)} job posting(s)")
            st.markdown("---")
            
            for job in filtered_jobs:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
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
                        
                        if st.button("View Details", key=f"view_{job.get('posting_id')}", use_container_width=True):
                            try:
                                detail_response = requests.get(f"{API_BASE_URL}/job-postings/{job.get('posting_id')}")
                                if detail_response.status_code == 200:
                                    detail = detail_response.json()
                                    with st.expander("📋 Full Details", expanded=True):
                                        if detail.get('alumni_name'):
                                            st.markdown(f"**Posted by:** {detail['alumni_name']}")
                                        if detail.get('current_role'):
                                            st.markdown(f"**Alumni Role:** {detail['current_role']}")
                                        if detail.get('company_name'):
                                            st.markdown(f"**Company:** {detail['company_name']}")
                                        if detail.get('alumni_email'):
                                            st.markdown(f"**Contact:** {detail['alumni_email']}")
                            except Exception as e:
                                st.error(f"Could not load details: {str(e)}")
                    
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
        st.error(f"Failed to load job postings. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the server: {str(e)}")
    st.info("Please make sure the API server is running.")