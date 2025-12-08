import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
import nu_connect as neu_con
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('Alumni Profile')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# Get alumni ID from session state
alumni_id = st.session_state.get("alumni_id")

if alumni_id is None:
    st.error("No Alumni profile available")
    st.button(
        "Return to Alumni Home Page",
        on_click=lambda: st.switch_page("pages/00_Alumni_Home.py"),
    )
else:
    # API endpoint
    API_URL = f"http://web-api:4000/alumni/{alumni_id}"

    try:
        # Fetch NGO details
        response = requests.get(API_URL)

        if response.status_code == 200:
            alumni = response.json()

            # Display basic information
            st.header(alumni["Name"])

            col1 = st.columns(1)

            with col1:
                st.subheader("About You")
                st.write(f"**Email:** {alumni['email']}")
                st.write(f"**Graduation Year:** {alumni['graduation_year']}")
                st.write(f"**Current Role:** {alumni['current_role']}")
                st.write(f"**Company Name:** {alumni['company_name']}")
                st.write(f"**Industry:** {alumni['industry']}")
                st.write(f"**Graduation Year:** {alumni['graduation_year']}")
                st.write(f"**Field:** {alumni['field']}")
                st.write(f"**Bio:** {alumni['bio']}")
                st.write(f"**Location:** {alumni['city']}, {alumni['state']}, {alumni['country']}")
                st.write(f"**Availability Status:** {alumni['availability_status']}")



    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

# Add a button to return to the NGO Directory
if st.button("Return to Alumni home page"):
    # Clear the selected NGO ID from session state
    if "selected_ngo_id" in st.session_state:
        del st.session_state["selected_ngo_id"]
    st.switch_page("pages/00_Alumni_Home.py")
