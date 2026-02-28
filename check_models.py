import google.generativeai as genai

# Use the API key from secrets if available, otherwise hardcode for test
import streamlit as st
try:
    API_KEY = "AIzaSyBq8NTz3Z1ZsmCRvA0AdRq2IeHAfHRGpsY"
    genai.configure(api_key=API_KEY)

    print("--- AVAILABLE MODELS ---")
    models = genai.list_models()
    count = 0
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            count += 1
    if count == 0:
        print("No models found supporting generateContent.")
except Exception as e:
    print(f"Error: {e}")
