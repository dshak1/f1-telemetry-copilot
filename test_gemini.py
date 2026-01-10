#!/usr/bin/env python3
"""Quick test of Gemini API with realistic F1 telemetry"""

from dotenv import load_dotenv
load_dotenv()

from gemini_race_engineer import RaceEngineerCopilot

# Create copilot
print("🏎️  Testing FARVIS with real Gemini API...\n")
copilot = RaceEngineerCopilot()

# Simulate realistic telemetry
test_telemetry = {
    "driver_id": 0,
    "driver_name": "Verstappen",
    "current_lap": 22,
    "race_position": 1,
    "sector": 2,
    "tire_wear_percent": 73.5,
    "speed_kmh": 287.3,
    "throttle": 0.95,
    "brake": 0.0,
    "is_pitting": "false",
    "aggression": 0.85,
    "tire_management": 0.65,
    "consistency": 0.90,
    "optimal_pit_lap": 24,
}

race_context = {
    "total_laps": 52,
    "safety_car_prob": 0.01,
    "overtaking_difficulty": 0.1,
}

# Get strategy recommendation
print("Calling Gemini API...\n")
strategy = copilot.get_strategy_recommendation(test_telemetry, race_context)

# Display result
print(copilot.format_strategy_output(strategy, test_telemetry))

print("\n✅ Test complete! If you see real strategic output above, Gemini is working!")
print(f"   API calls: {copilot.api_call_count}, Errors: {copilot.api_errors}")
