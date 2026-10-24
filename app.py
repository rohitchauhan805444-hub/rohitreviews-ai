import streamlit as st
import google.generativeai as genai
import random
import os

# Page Configuration
st.set_page_config(
    page_title="RohitReviews Reel AI",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 @rohitreviews Reel Creator")
st.caption("AI-powered live pop-culture radar & high-retention scriptwriter.")

# Retrieve API key
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    st.error("Missing Gemini API Key! Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Dynamic angles to ensure fresh content on every run
ANGLES = [
    "Hot Take / Unpopular Opinion (controversial, sparks debate in comments)",
    "Hidden Easter Egg / Detail everyone missed",
    "Behind-the-Scenes Chaos / Drama / Casting what-if",
    "Box Office & Review Disasters / Shocking Wins",
    "Fan Theory that actually makes total sense",
    "Breaking Trailer / Casting News reaction"
]

selected_angle = random.choice(ANGLES)

def get_active_model():
    """Dynamically finds the best active model so it never hits a 404 error."""
    try:
        available_models = [
            m.name for m in genai.list_models() 
            if "generateContent" in m.supported_generation_methods
        ]
        # Prefer the newest flash models
        for preference in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]:
            for m in available_models:
                if preference in m:
                    return m
        # Fallback to any model with 'flash'
        for m in available_models:
            if "flash" in m:
                return m
        # Otherwise fallback to the first supported model
        return available_models[0]
    except Exception:
        # Default safety fallback
        return "gemini-2.0-flash"

def generate_reel_script(angle):
    model_name = get_active_model()
    model = genai.GenerativeModel(model_name=model_name)
    
    prompt = f"""
    You are the head creative writer for the Instagram movie & pop-culture page '@rohitreviews'.
    Target Audience: Gen-Z and Millennials who love cinema, OTT shows, MCU, DC, anime, and internet drama.
    
    Task:
    1. Pick ONE exciting, viral, or trending movie/TV show/pop-culture topic.
    2. Frame it using this angle: "{angle}".
    3. Write a 30 to 45-second high-retention Instagram Reel script.

    Output format:
    ---
    ### 📌 The Concept & News Headline
    - **Topic:** [Name of movie/show/actor]
    - **The Hook Idea:** [Why people will stop scrolling in 0.5s]

    ### 🎬 Reel Script (30-45s)
    - **[0:00 - 0:03] HOOK:**
      - **Visual:** (Exact B-Roll or facecam instruction + On-screen text)
      - **Voiceover:** (High energy, immediate curiosity gap)
    - **[0:03 - 0:25] THE MEAT / DRAMA:**
      - **Visuals:** (Fast-paced image/clip suggestions)
      - **Voiceover:** (Casual, punchy, no filler words)
    - **[0:25 - 0:35] HOT TAKE / CONCLUSION:**
      - **Voiceover:** (Rohit's personal verdict)
    - **[0:35 - 0:40] OUTRO / CTA:**
      - **Voiceover:** (Question to prompt comments + "Follow @rohitreviews for more")

    ### 📱 Captions & Audio Suggestion
    - **Trending Audio Vibe:** (e.g., tense suspense, retro synth, phonk)
    - **Caption:** (Punchy, 2-line caption with a debate question)
    - **Hashtags:** (10 targeted hashtags)
    ---
    Make it sound human, energetic, and engaging—avoid boring AI jargon.
    """
    
    response = model.generate_content(prompt)
    return response.text

if st.button("⚡ Generate New Reel Idea & Script", type="primary", use_container_width=True):
    with st.spinner(f"Scouting idea with a '{selected_angle}' angle..."):
        try:
            script = generate_reel_script(selected_angle)
            st.markdown(script)
        except Exception as e:
            st.error(f"Error generating script: {e}")
else:
    st.info("Tap the button above to scout a fresh reel idea and script.")
