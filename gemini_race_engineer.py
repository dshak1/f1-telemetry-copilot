#!/usr/bin/env python3
"""
FARVIS - Fast Adaptable Reliable Visionary Insanely Stupendous
F1 Race Engineer AI Copilot powered by Google Gemini API

This layer sits ABOVE the real-time C++ telemetry system and provides
strategic decision-making at lap/event timescales (not millisecond control).
"""

import os
import json
import time
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set. Using mock mode.")
    MOCK_MODE = True
else:
    genai.configure(api_key=GEMINI_API_KEY)
    MOCK_MODE = False
    print(f"Gemini API configured (key: {GEMINI_API_KEY[:10]}...)")

@dataclass
class StrategyCall:
    """A race engineer's strategic recommendation"""
    radio_message: str
    reasoning: str
    alternatives: List[str]
    risk_level: str  # LOW, MEDIUM, HIGH
    confidence: float


class RaceEngineerCopilot:
    """
    Race Engineer AI that provides strategic guidance based on telemetry.
    
    Key Design Principles:
    - NOT in the real-time control loop (C++ handles that)
    - Operates at lap/event timescales (seconds, not milliseconds)
    - Provides 2-3 strategic options with tradeoffs
    - Speaks in concise "radio-style" language
    """
    
    def __init__(self, model_name: str = "models/gemini-3-flash-preview"):
        """
        Initialize Race Engineer Copilot with Gemini API.
        Using models/gemini-3-flash-preview - Gemini 3 with 5 RPM, 20 RPD limits.
        """
        global MOCK_MODE
        self.model_name = model_name
        if not MOCK_MODE:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"Using Gemini model: {model_name}")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                print("   Falling back to mock mode")
                MOCK_MODE = True
        
        # Track state for event detection
        self.last_lap_processed: Dict[int, int] = {}
        self.pit_recommendations_given: Dict[int, bool] = {}
        self.last_strategy_call_time = 0
        self.min_call_interval = 15.0  # 15s interval = 4 calls/min (under 5 RPM limit)
        self.api_call_count = 0
        self.api_errors = 0
        
    def should_provide_strategy(self, telemetry: Dict, force: bool = False) -> bool:
        """
        Determine if we should call Gemini based on:
        - Lap boundaries (end of lap)
        - Key events (tire wear threshold, position changes, safety car)
        - Time since last call (throttling)
        """
        if force:
            return True
            
        current_time = time.time()
        if current_time - self.last_strategy_call_time < self.min_call_interval:
            return False
        
        driver_id = telemetry.get("driver_id", 0)
        current_lap = telemetry.get("current_lap", 0)
        
        # Event 1: Lap boundary (provide strategy every lap)
        if current_lap != self.last_lap_processed.get(driver_id, 0):
            self.last_lap_processed[driver_id] = current_lap
            return True
        
        # Event 2: High tire wear (approaching pit window)
        tire_wear = telemetry.get("tire_wear_percent", 0)
        if tire_wear > 70 and driver_id not in self.pit_recommendations_given:
            self.pit_recommendations_given[driver_id] = True
            return True
        
        # Event 3: Position changes in top 5
        position = telemetry.get("race_position", 99)
        if position <= 5:
            return True
        
        return False
    
    def create_strategy_prompt(self, telemetry: Dict, race_context: Dict) -> str:
        """
        Create a compact, focused prompt for Gemini.
        We send STATE SUMMARY, not raw 50Hz telemetry.
        """
        prompt = f"""You are FARVIS, an F1 Race Engineer AI providing strategic guidance.

CURRENT RACE STATE:
Driver: {telemetry.get('driver_name', 'Unknown')}
Lap: {telemetry.get('current_lap', 0)}/{race_context.get('total_laps', 52)} (Sector {telemetry.get('sector', 1)})
Position: P{telemetry.get('race_position', '?')}
Tire Wear: {telemetry.get('tire_wear_percent', 0):.1f}%
Speed: {telemetry.get('speed_kmh', 0):.1f} km/h
Throttle: {telemetry.get('throttle', 0):.1%}
Brake: {telemetry.get('brake', 0):.1%}
In Pits: {telemetry.get('is_pitting', 'false')}

DRIVER PROFILE:
Aggression: {telemetry.get('aggression', 0.5):.2f} (0=conservative, 1=aggressive)
Tire Management: {telemetry.get('tire_management', 0.5):.2f}
Consistency: {telemetry.get('consistency', 0.5):.2f}

PIT STRATEGY:
Optimal Pit Window: Lap {telemetry.get('optimal_pit_lap', 'Unknown')}

RACE CONTEXT:
Safety Car Probability: {race_context.get('safety_car_prob', 0.01):.2%}
Track Overtaking Difficulty: {race_context.get('overtaking_difficulty', 0.1):.2f}

YOUR TASK:
Provide a strategic recommendation in this EXACT format:

RADIO: [One concise sentence, max 15 words, like real F1 radio]
REASONING: [2-3 sentences explaining the strategy]
OPTION_A: [Primary recommendation with brief rationale]
OPTION_B: [Alternative approach with tradeoff]
OPTION_C: [Conservative backup option]
RISK: [LOW/MEDIUM/HIGH]
CONFIDENCE: [0.0-1.0]

Be decisive, concise, and speak like a real F1 race engineer (not verbose).
"""
        return prompt
    
    def get_strategy_recommendation(self, telemetry: Dict, race_context: Dict) -> StrategyCall:
        """
        Call Gemini API to get strategic recommendation.
        Falls back to mock mode if API fails (rate limits, network issues, etc.)
        """
        if MOCK_MODE:
            return self._mock_strategy_call(telemetry)
        
        try:
            self.api_call_count += 1
            prompt = self.create_strategy_prompt(telemetry, race_context)
            response = self.model.generate_content(prompt)
            
            # Parse structured response
            text = response.text
            result = self._parse_strategy_response(text)
            
            # Log success
            if self.api_call_count % 5 == 0:
                print(f"Gemini API: {self.api_call_count} calls, {self.api_errors} errors")
            
            return result
            
        except Exception as e:
            self.api_errors += 1
            error_msg = str(e)
            
            if "429" in error_msg or "quota" in error_msg.lower():
                print(f"Gemini API rate limit hit (call #{self.api_call_count})")
                print(f"   Free tier: 15 RPM, 1500 RPD. Wait 60s or use mock mode.")
                print(f"   Tip: Reduce call frequency in code (currently every {self.min_call_interval}s)")
            elif "404" in error_msg:
                print(f"Gemini model not available. Check model name: {self.model_name}")
            else:
                print(f"Gemini API error: {e}")
            
            # Use mock mode for this call
            return self._mock_strategy_call(telemetry)
    
    def _parse_strategy_response(self, text: str) -> StrategyCall:
        """Parse Gemini's structured response"""
        lines = text.strip().split('\n')
        parsed = {}
        
        for line in lines:
            if line.startswith('RADIO:'):
                parsed['radio'] = line.replace('RADIO:', '').strip()
            elif line.startswith('REASONING:'):
                parsed['reasoning'] = line.replace('REASONING:', '').strip()
            elif line.startswith('OPTION_A:'):
                parsed['option_a'] = line.replace('OPTION_A:', '').strip()
            elif line.startswith('OPTION_B:'):
                parsed['option_b'] = line.replace('OPTION_B:', '').strip()
            elif line.startswith('OPTION_C:'):
                parsed['option_c'] = line.replace('OPTION_C:', '').strip()
            elif line.startswith('RISK:'):
                parsed['risk'] = line.replace('RISK:', '').strip()
            elif line.startswith('CONFIDENCE:'):
                try:
                    parsed['confidence'] = float(line.replace('CONFIDENCE:', '').strip())
                except:
                    parsed['confidence'] = 0.7
        
        return StrategyCall(
            radio_message=parsed.get('radio', 'Box box, box box'),
            reasoning=parsed.get('reasoning', 'Strategy analysis in progress'),
            alternatives=[
                parsed.get('option_a', 'Option A'),
                parsed.get('option_b', 'Option B'),
                parsed.get('option_c', 'Option C')
            ],
            risk_level=parsed.get('risk', 'MEDIUM'),
            confidence=parsed.get('confidence', 0.7)
        )
    
    def _mock_strategy_call(self, telemetry: Dict) -> StrategyCall:
        """Fallback mock strategy for demo when API key not set"""
        tire_wear = telemetry.get('tire_wear_percent', 0)
        current_lap = telemetry.get('current_lap', 0)
        
        if tire_wear > 75:
            return StrategyCall(
                radio_message="Box this lap, box this lap. Tires critical.",
                reasoning=f"Tire wear at {tire_wear:.0f}%, pit now to avoid catastrophic degradation",
                alternatives=[
                    "Pit now: Fresh tires, rejoin P5-P6, strong pace to end",
                    "Stay out 1 more lap: Risk tire failure, potential track position",
                    "Go long: Gamble on safety car, high risk strategy"
                ],
                risk_level="HIGH" if tire_wear > 85 else "MEDIUM",
                confidence=0.85
            )
        elif tire_wear > 60:
            return StrategyCall(
                radio_message="Approaching pit window. Prepare for undercut.",
                reasoning=f"Optimal pit window opening, lap {current_lap}. Monitor competitors.",
                alternatives=[
                    "Pit in 2 laps: Standard timing, safe strategy",
                    "Undercut now: Jump cars ahead, aggressive play",
                    "Overcut: Stay out, hope for clear air advantage"
                ],
                risk_level="MEDIUM",
                confidence=0.75
            )
        else:
            return StrategyCall(
                radio_message="Pace is good. Push now, manage delta.",
                reasoning="Tire condition strong, focus on building gap or closing",
                alternatives=[
                    "Push mode: Build gap, manage tire temps",
                    "Conservation: Extend stint, late pit advantage",
                    "Attack mode: Prepare overtake, use ERS wisely"
                ],
                risk_level="LOW",
                confidence=0.8
            )
    
    def format_strategy_output(self, call: StrategyCall, telemetry: Dict) -> str:
        """Format strategy call for beautiful terminal display"""
        driver = telemetry.get('driver_name', 'Unknown')
        lap = telemetry.get('current_lap', 0)
        position = telemetry.get('race_position', '?')
        
        output = f"""
╔══════════════════════════════════════════════════════════════╗
║  FARVIS RACE ENGINEER - LAP {lap} - P{position} - {driver.upper()}  
╚══════════════════════════════════════════════════════════════╝

RADIO: "{call.radio_message}"

REASONING: {call.reasoning}

STRATEGIC OPTIONS:
   A) {call.alternatives[0]}
   B) {call.alternatives[1]}
   C) {call.alternatives[2]}

RISK LEVEL: {call.risk_level}
CONFIDENCE: {call.confidence:.0%}

{'═' * 64}
"""
        return output


def main():
    """
    Main demo loop: Read telemetry from C++ (stdin or file) and provide strategy
    """
    print("FARVIS - F1 Race Engineer AI Copilot")
    print("=" * 64)
    
    if MOCK_MODE:
        print("Running in MOCK MODE (set GEMINI_API_KEY to use real API)")
    else:
        print("Gemini API configured")
    
    print("=" * 64)
    print("\nWaiting for telemetry data from C++ simulation...\n")
    
    copilot = RaceEngineerCopilot()
    
    race_context = {
        'total_laps': 52,
        'safety_car_prob': 0.01,
        'overtaking_difficulty': 0.1
    }
    
    # Demo: Read from stdin (piped from C++ output)
    # In production, this could be a socket, shared memory, or file watch
    
    for line in sys.stdin:
        try:
            # Expect JSON telemetry frames from C++
            telemetry = json.loads(line.strip())
            
            # Check if we should provide strategy
            if copilot.should_provide_strategy(telemetry):
                call = copilot.get_strategy_recommendation(telemetry, race_context)
                print(copilot.format_strategy_output(call, telemetry))
                copilot.last_strategy_call_time = time.time()
                
        except json.JSONDecodeError:
            # Not JSON, probably regular C++ output - ignore
            pass
        except KeyboardInterrupt:
            print("\n\nRace Engineer signing off. Good race!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
