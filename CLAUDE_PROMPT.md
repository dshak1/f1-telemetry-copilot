# Project Brief: F1 Race Engineer AI Copilot (FARVIS)

## URGENT CONTEXT
- **Time Remaining**: 4 hours until hackathon submission
- **Status**: Core C++ telemetry system is COMPLETE and working
- **Need**: Integration strategy with Gemini API + pitch refinement for judges

---

## WHAT I NEED YOU TO DO

### 1. Run & Understand the Telemetry System (Priority 1)
- Navigate to `/Users/diarshakimov/Downloads/f1-telemetry-copilot`
- Compile and run the telemetry simulator using:
  ```bash
  g++ -std=c++17 -I src src/main.cpp src/telemetry/TelemetryGenerator.cpp src/strategy/RaceSimulator.cpp src/strategy/StrategyAnalyzer.cpp src/race-control/TrackLimitsMonitor.cpp src/race-control/PenaltyEnforcer.cpp -o f1-telemetry -pthread
  ./f1-telemetry
  ```
- Observe the telemetry output and understand what data is being generated

### 2. Design Gemini API Integration (Priority 1)
**Key Constraint**: Gemini is NOT in the real-time control loop (that's C++). It operates at **lap/event timescales**.

**Propose:**
- How to capture telemetry data from C++ (JSON stream to stdout/file/socket?)
- What layer connects C++ to Gemini (Python FastAPI? Node.js?)
- When to call Gemini (every lap? on events like tire wear threshold, safety car, gap changes?)
- What data to send to Gemini (compact state summary, not raw 50Hz telemetry)
- What Gemini should return (radio-style strategy calls, 2-3 options with tradeoffs, risk warnings)

### 3. Create "Wow Moment" Demo Scenario (Priority 2)
**Idea**: Show dynamic strategy adaptation
- Example: Change driver aggression parameter mid-race → Gemini adapts pit call within 2 seconds with reasoning
- Or: Safety car event → Gemini suggests multiple strategic options (stay out vs. pit now vs. pit later)
- Should be visually/conceptually impressive for judges in 2-3 minutes

### 4. Refine Pitch Framework (Priority 2)
**Target Awards:**
- Primary: Lone Wanderer Award (solo hacker)
- Secondary: Best Use of Gemini API

**Key Messaging:**
- **NOT**: "AI drives the F1 car in real-time" (sounds unrealistic)
- **YES**: "Race Engineer Copilot for sim racing / pit wall decision support"
- **Hook**: "Every great leader has a great #2. MJ had Scottie, Iron Man had JARVIS. This is FARVIS - Fast, Adaptable, Reliable, Visionary, Insanely Stupendous"

**Technical Story:**
- "Real-time decisions (milliseconds) = deterministic C++ heuristics"
- "Strategic decisions (seconds-to-laps) = Gemini providing options + reasoning"
- "Two-layer architecture: fast local compute + intelligent advisory layer"

---

## PROJECT ASSETS (Already Complete)

### C++ Telemetry System Features
✅ Multi-threaded producer-consumer architecture with thread-safe ring buffer  
✅ 20-driver 2025 F1 grid with realistic profiles (aggression, consistency, tire management)  
✅ Real-time telemetry at 50Hz (speed, position, tire wear, fuel, sector times)  
✅ Tire degradation modeling based on aggression and track characteristics  
✅ Pit stop strategy with variable thresholds per driver  
✅ Track limits monitoring with warnings → penalties  
✅ Penalty enforcement during pit stops  
✅ Optional pre-race optimal strategy analyzer  
✅ Beautiful color-coded terminal display with live leaderboard  

### My Background (Relevant Skills)
- Strong in C++, Python, AI
- Built: RISC-V pipeline simulator, cache simulator, NIDS using GAN, AI agent debate system
- Taking CMPT 310 (AI course) - understand fast vs slow AI, search algorithms, optimization

---

## CONSTRAINTS & PREFERENCES

### What I DON'T Want
❌ Generic v0/Lovable front-end slop (I'd rather have CLI/terminal dashboard)  
❌ Claiming "real-time millisecond AI decision making" (not realistic)  
❌ Half-baked integration that doesn't actually work  

### What I DO Want
✅ Authentic, technically deep project I'm proud of  
✅ Clear separation: C++ does real-time compute, Gemini does strategic reasoning  
✅ Working demo that showcases both systems playing to their strengths  
✅ Compelling pitch that judges will remember  
✅ Something that could actually be useful for sim racers / esports  

---

## DELIVERABLES NEEDED

1. **Integration Architecture Plan**
   - Specific code/tools needed to connect C++ → Gemini
   - Data format and API call timing strategy
   - Estimated implementation time (I have 4 hours total)

2. **Demo Script**
   - Step-by-step scenario showing the "wow moment"
   - What to say/show to judges
   - Parameters to change, expected Gemini responses

3. **Pitch Refinement**
   - Elevator pitch (30 seconds)
   - Technical explanation (2 minutes)
   - Value proposition for judges

4. **Implementation Roadmap**
   - Prioritized tasks for next 4 hours
   - What's essential vs. nice-to-have
   - Fallback plan if something doesn't work

---

## QUESTIONS FOR YOU

- Is my two-layer architecture (C++ real-time + Gemini strategic) the right approach?
- What's the fastest way to get telemetry from C++ to a Gemini API call?
- Should I output telemetry to JSON file and have Python read it, or use stdout pipe, or something else?
- What specific Gemini API features should I highlight in my pitch?
- Do you see any technical risks in the next 4 hours I should plan for?

---

**LET'S BUILD SOMETHING IMPRESSIVE. I'M READY TO EXECUTE.**
