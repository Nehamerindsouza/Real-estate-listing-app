import os
import streamlit as st
from openai import OpenAI # Corrected import

# For Streamlit Cloud secrets and local .streamlit/secrets.toml
# Do NOT include a hardcoded API key as the default value here.
# st.secrets.get will retrieve it if available, otherwise it will be None.
openai_api_key = st.secrets.get("openai_api_key")

# Ensure the API key is set before initializing the client
if not openai_api_key:
    # If running locally and not using .streamlit/secrets.toml,
    # you might want to fall back to environment variable or raise an error.
    # For Streamlit Cloud, st.secrets is the primary mechanism.
    st.error("OpenAI API key not found. Please set it in your Streamlit secrets or environment variables.")
    st.stop() # Stop the app if API key is missing

st.title("🏠 Real Estate Listing Generator")
st.markdown("Generate professional property listings using property features and neighborhood info.")

with st.form("listing_form"):
    st.subheader("📌 Property Features")
    property_details = st.text_area("Describe the property", height=150, placeholder="e.g. 3 BHK, 2 baths, 1500 sqft, balcony...")

    st.subheader("📍 Neighborhood Info")
    neighborhood_info = st.text_area("Describe the area", height=120, placeholder="e.g. Near central park, metro nearby, schools...")

    submitted = st.form_submit_button("Generate Listing")

if submitted:
    if not property_details or not neighborhood_info:
        st.warning("Please provide both sections.")
    else:
        prompt = f"""
        Write a compelling real estate listing using:

        Property:
        {property_details}

        Neighborhood:
        {neighborhood_info}

        Keep it appealing and easy to read.
        """

        try:
            # Initialize the OpenAI client with the retrieved API key
            client = OpenAI(api_key=openai_api_key) # Corrected initialization

            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            listing = completion.choices[0].message.content.strip()
            st.success("Listing generated!")
            st.text_area("Generated Listing", listing, height=200)

        except Exception as e:
            st.error(f"Error generating listing: {e}")
            st.info("Please ensure your OpenAI API key is correct and you have sufficient credits.")