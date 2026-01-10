#!/usr/bin/env python3
"""Quick test to verify Gemini API model availability"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: No API key found")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("Testing Gemini models...")
print("=" * 60)

models_to_test = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash",
    "gemini-flash-latest",
    "models/gemini-1.5-flash",
]

for model_name in models_to_test:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'OK' if you can read this.")
        print(f"  SUCCESS: {response.text.strip()}")
        print(f"  >>> USE THIS MODEL: {model_name}")
        break
    except Exception as e:
        print(f"  FAILED: {str(e)[:100]}")

print("\n" + "=" * 60)
