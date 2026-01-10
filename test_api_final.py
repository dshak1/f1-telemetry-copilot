#!/usr/bin/env python3
"""Quick API test with correct model name"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Testing models/gemini-3-flash-preview...")

try:
    model = genai.GenerativeModel("models/gemini-3-flash-preview")
    response = model.generate_content("You are an F1 race engineer. The driver is on lap 10 with 65% tire wear. Give a brief radio call.")
    print("\nSUCCESS! Gemini API is working:")
    print("=" * 60)
    print(response.text)
    print("=" * 60)
    print("\n✓ Real Gemini API confirmed working!")
except Exception as e:
    print(f"\nERROR: {e}")
