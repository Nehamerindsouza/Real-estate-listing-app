import streamlit as st
import cohere  # Use Cohere instead of OpenAI

# Get Cohere API key from secrets
cohere_api_key = st.secrets.get("cohere_api_key")

if not cohere_api_key:
    st.error("Cohere API key not found. Please set it in your Streamlit secrets as 'cohere_api_key'.")
    st.stop()

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

st.title("🏠 Real Estate Listing Generator (Cohere)")
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
            response = co.generate(
                model='command',  # Or try 'command-light'
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            listing = response.generations[0].text.strip()
            st.success("Listing generated!")
            st.text_area("Generated Listing", listing, height=200)

        except Exception as e:
            st.error(f"Error generating listing: {e}")
            st.info("Please ensure your Cohere API key is correct and active.")
