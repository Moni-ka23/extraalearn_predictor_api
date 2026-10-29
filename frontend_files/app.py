
import os
import requests
import pandas as pd
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860").rstrip("/")

st.set_page_config(
    page_title="ExtraaLearn Lead Conversion Prediction",
    layout="centered"
)

st.title("ExtraaLearn Lead Conversion Prediction")
st.write(
    "Enter the lead details below to predict whether the lead "
    "is likely to convert into a paid customer."
)

st.info("Complete all fields and click Predict to get a result.")

with st.form("lead_prediction_form"):

    st.subheader("Lead Information")

    age = st.number_input(
        "Age", min_value=18, max_value=100, value=30
    )

    current_occupation = st.selectbox(
        "Current Occupation",
        ["Professional", "Unemployed", "Student"]
    )

    first_interaction = st.selectbox(
        "First Interaction",
        ["Website", "Mobile App"]
    )

    profile_completed = st.selectbox(
        "Profile Completed",
        ["Low", "Medium", "High"]
    )

    website_visits = st.number_input(
        "Website Visits", min_value=0, value=3
    )

    time_spent_on_website = st.number_input(
        "Time Spent on Website", min_value=0, value=120
    )

    page_views_per_visit = st.number_input(
        "Page Views per Visit",
        min_value=0.0, value=3.0, step=0.5
    )

    last_activity = st.selectbox(
        "Last Activity",
        [
            "Email Activity",
            "Phone Activity",
            "Website Activity"
        ]
    )

    st.subheader("Marketing Channels")

    print_media_type1 = st.selectbox(
        "Print Media Type 1", ["No", "Yes"]
    )

    print_media_type2 = st.selectbox(
        "Print Media Type 2", ["No", "Yes"]
    )

    digital_media = st.selectbox(
        "Digital Media", ["No", "Yes"]
    )

    educational_channels = st.selectbox(
        "Educational Channels", ["No", "Yes"]
    )

    referral = st.selectbox(
        "Referral", ["No", "Yes"]
    )

    submitted = st.form_submit_button(
        "Predict Lead Conversion",
        use_container_width=True
    )

if submitted:

    lead_data = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }

    st.subheader("Prediction Result")

    try:
        with st.spinner("Getting prediction..."):
            response = requests.post(
                f"{BACKEND_URL}/v1/extraalearn",
                json=lead_data,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

        st.success("Prediction received successfully!")
        st.json(result)

    except requests.exceptions.RequestException as error:
        st.error(
            "Unable to get a prediction from the backend. "
            "Check that the backend is running and the API endpoint "
            "and request format are correct."
        )
        st.caption(str(error))
