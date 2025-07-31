import streamlit as st
import cohere

# --- Streamlit Page Configuration (Must be the first Streamlit command) ---
st.set_page_config(
    page_title="AI-Powered Listing Creator",
    page_icon="🏡",
    layout="wide", # Use wide layout for more space for design elements
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Advanced Styling & Animations ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Open+Sans:wght@300;400&display=swap');

/* Overall App Background & Font */
.stApp {
    background: linear-gradient(135deg, #FF6B6B 0%, #FFD166 50%, #4ECDC4 100%); /* Warm & cool gradient */
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite; /* Subtle background animation */
    font-family: 'Open Sans', sans-serif;
    color: #333; /* Dark text for contrast against light gradient */
}

/* Keyframe for background animation */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* --- Hero Section (Main Title & Subtitle) --- */
.hero-container {
    background: rgba(255, 255, 255, 0.95); /* Nearly opaque white for clarity */
    border-radius: 25px;
    padding: 40px 60px;
    margin-bottom: 3em;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    border: 2px solid #FFD166; /* Accent border */
    animation: fadeInUp 1s ease-out; /* Fade in animation for hero */
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

.main-app-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 4.8em !important; /* Larger, more impactful title */
    color: #E74C3C; /* Striking red */
    text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    margin-bottom: 0.1em;
    letter-spacing: -1px; /* Tighter letter spacing for boldness */
    font-weight: 800; /* Extra bold */
}

.title-icon {
    display: inline-block;
    animation: bounce 2s infinite; /* Bouncing icon */
    margin: 0 10px;
}
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

.app-subtitle {
    font-family: 'Open Sans', sans-serif;
    font-size: 1.8em !important;
    color: #555; /* Darker grey for good contrast */
    margin-top: 0;
    margin-bottom: 1.5em;
    font-weight: 400;
}

/* --- Form Container --- */
.stForm {
    background: rgba(255, 255, 255, 0.9); /* Slightly transparent white for form */
    border-radius: 20px;
    padding: 35px 50px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    border: 1px solid #ddd;
    margin-bottom: 30px;
    transition: transform 0.3s ease-in-out;
}
.stForm:hover {
    transform: translateY(-5px); /* Slight lift on hover for the entire form */
}

/* Subheaders within the form */
.stForm h3 {
    font-family: 'Montserrat', sans-serif;
    color: #4ECDC4; /* Teal color for subheaders */
    font-size: 2.2em; /* Larger subheaders */
    font-weight: 700;
    text-align: center;
    margin-bottom: 1.8em;
    position: relative;
}
.stForm h3::after {
    content: '';
    display: block;
    width: 60px;
    height: 4px;
    background: linear-gradient(to right, #FF6B6B, #FFD166); /* Gradient underline */
    margin: 10px auto 0;
    border-radius: 2px;
}


/* Input Text Areas */
.stTextArea label {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.3em; /* Larger labels */
    font-weight: 600;
    color: #E74C3C; /* Red for labels */
    margin-bottom: 12px;
}
.stTextArea textarea {
    background-color: #f8f8f8; /* Off-white input background */
    border: 2px solid #ddd;
    border-radius: 12px;
    padding: 18px;
    font-size: 1.1em;
    color: #333;
    transition: all 0.3s ease-in-out;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
    resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #4ECDC4; /* Teal border on focus */
    box-shadow: 0 0 0 0.3rem rgba(78, 205, 196, 0.25), inset 0 2px 5px rgba(0,0,0,0.1);
    outline: none;
    background-color: #ffffff;
}
/* Placeholder text color */
.stTextArea textarea::placeholder {
    color: #888;
}

/* Submit Button Styling */
.stButton button {
    background: linear-gradient(45deg, #E74C3C, #FFD166); /* Red-to-Orange gradient */
    color: white;
    padding: 18px 40px;
    border-radius: 12px;
    border: none;
    font-size: 1.4em; /* Larger button text */
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 8px 20px rgba(231, 76, 60, 0.4);
    transition: all 0.3s ease-in-out;
    width: 100%;
    letter-spacing: 1px;
    text-transform: uppercase; /* Uppercase text */
}
.stButton button:hover {
    background: linear-gradient(45deg, #FFD166, #E74C3C); /* Reverse gradient on hover */
    transform: translateY(-5px) scale(1.02); /* More pronounced lift and scale */
    box-shadow: 0 12px 30px rgba(255, 209, 102, 0.6);
}
.stButton button:active {
    transform: translateY(0);
    box-shadow: 0 4px 10px rgba(231, 76, 60, 0.3);
}

/* Horizontal Rule for separation */
hr {
    border-top: 1px solid rgba(255, 255, 255, 0.4);
    margin: 3em 0;
}

/* Streamlit specific alerts (success, warning, error) */
.stAlert {
    border-radius: 10px;
    font-size: 1.1em;
    margin-top: 25px;
}
.stAlert > div {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    color: #333 !important;
    border-left: 8px solid !important;
}
.stAlert.streamlit-container.st-emotion-cache-1kyxgrx p {
    color: #333 !important;
}
.stAlert.success > div { border-left-color: #28a745 !important; }
.stAlert.warning > div { border-left-color: #ffc107 !important; }
.stAlert.error > div { border-left-color: #dc3545 !important; }

/* Generated Listing Output Box - ensure it matches the new theme */
.generated-listing-box {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #4ECDC4; /* Teal border */
    border-radius: 20px;
    padding: 35px;
    margin-top: 40px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    font-family: 'Open Sans', sans-serif;
    line-height: 1.8;
    color: #333;
    font-size: 1.1em;
    animation: fadeIn 1s ease-out;
}
.generated-listing-box p {
    margin-bottom: 1em;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# --- Cohere API Key Initialization ---
cohere_api_key = st.secrets.get("cohere_api_key")

if not cohere_api_key:
    st.error("Cohere API key not found. Please set it in your Streamlit secrets as 'cohere_api_key'.")
    st.stop()

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

# --- Application UI Layout: MODIFIED SECTION START ---

# Hero Section (Title and Subtitle)
st.markdown(
    f"""
    <div class="hero-container">
        <h1 class="main-app-title">
            <span class="title-icon">🏠</span> Elite Property AI <span class="title-icon">✨</span>
        </h1>
        <p class="app-subtitle">
            Generate stunning, professional real estate listings with cutting-edge AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Main Input Form
with st.form("listing_form", clear_on_submit=False):
    st.markdown("<h3>Property Details & Location Vibes</h3>", unsafe_allow_html=True)

    # Using columns for a side-by-side layout for input text areas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Property Features")
        property_details = st.text_area(
            "Describe all key features, amenities, and unique selling points.",
            height=180, # Increased height for more visual space
            placeholder="e.g. 3 luxurious bedrooms, 2 spa-like bathrooms, 2200 sqft, gourmet kitchen with island, private rooftop terrace, smart home technology, ample natural light...",
            key="prop_details_ui" # Changed key to avoid conflict if any in future
        )

    with col2:
        st.subheader("📍 Neighborhood Info")
        neighborhood_info = st.text_area(
            "What's the vibe? Describe the area's charm, amenities, and lifestyle opportunities.",
            height=180, # Increased height
            placeholder="e.g. Situated in the bustling arts district, steps from vibrant nightlife, walking distance to gourmet grocery stores, excellent public transport access, serene parkland nearby, top-tier schools in catchment...",
            key="neigh_info_ui" # Changed key
        )

    st.markdown("---") # Another separator before the button

    # Centering the submit button visually using columns
    col_empty1, col_btn, col_empty2 = st.columns([1.5, 2, 1.5]) # Adjusted ratios for centering
    with col_btn:
        submitted = st.form_submit_button("🚀 Create My Listing!", use_container_width=True)

# --- Application UI Layout: MODIFIED SECTION END ---


# --- Output Section (Remains the same as before, with error handling fix) ---
if submitted:
    if not property_details or not neighborhood_info:
        st.warning("All fields are required to craft your masterpiece! Please provide details for both **Property Features** and **Neighborhood Info**.")
    else: # This 'else' block ensures the prompt is only generated if inputs are present
        prompt = f"""
        You are a highly skilled and creative real estate copywriter. Your goal is to craft an irresistibly compelling, attractive, and professional property listing.
        Focus on evoking emotions and painting a vivid picture for potential buyers.
        Highlight the most appealing unique selling points of the property and emphasize the benefits and lifestyle offered by the neighborhood.
        Use engaging language, strong descriptive verbs, and a positive, enthusiastic tone.
        The listing should be well-structured, easy to read, and persuasive.

        Property Details:
        {property_details}

        Neighborhood Information:
        {neighborhood_info}

        Start with an attention-grabbing headline (e.g., "Discover Your Oasis in [Neighborhood]!" or "Elegance Meets Convenience in [Address]!").
        Then, elaborate on the property features, followed by a section on the neighborhood, and conclude with a strong call to action.
        """

        try:
            with st.spinner('✨ Conjuring your dream listing... This might take a moment!'):
                response = co.generate( # This line was correctly indented
                    model='command', # <--- IMPORTANT: Changed from 'command-r' to 'command'
                                    # 'command-r' is typically for the Chat API, not the Generate API.
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.7,
                    p=0.9,
                    k=0
                )
            # --- FIX STARTS HERE ---
            listing = response.generations[0].text.strip() # THIS LINE WAS MIS-INDENTED
            st.success("🎉 Your Captivating Listing is Ready! Feast your eyes:") # THIS LINE WAS MIS-INDENTED
            st.markdown("<div class='generated-listing-box'>", unsafe_allow_html=True) # THIS LINE WAS MIS-INDENTED
            st.write(listing) # THIS LINE WAS MIS-INDENTED
            st.markdown("</div>", unsafe_allow_html=True) # THIS LINE WAS MIS-INDENTED
            # --- FIX ENDS HERE ---

        # This except block is correctly indented relative to the 'try' block.
        except Exception as e:
            st.error(f"🚫 An error occurred while generating the listing: {e}")
            st.info("Please double-check your Cohere API key, ensure you have sufficient credits, and try again later.")

# --- Dynamic Footer ---
# This footer section is correctly placed at the top-level indentation of the script.
st.markdown("---")
st.markdown("<p style='text-align: center; color: rgba(51, 51, 51, 0.7); font-weight: 300;'>Powered by <span style='color: #E74C3C; font-weight: 600;'>Cohere AI</span> for seamless listing generation.</p>", unsafe_allow_html=True)
