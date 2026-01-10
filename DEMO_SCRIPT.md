# FARVIS Demo Script for Judges

## Setup (30 seconds)
1. Open terminal
2. Navigate to project directory
3. Run: `bash run_farvis_demo.sh`

## Demo Flow (2-3 minutes)

### Opening Hook (15 seconds)
"Every great leader has a great #2. MJ had Scottie Pippen. Iron Man had JARVIS. 
This is FARVIS - Fast, Adaptable, Reliable, Visionary, Insanely Stupendous - 
an F1 Race Engineer AI Copilot that helps drivers make split-second strategic decisions."

### Technical Showcase (90 seconds)

**Part 1: The Real-Time Layer (30 seconds)**
- Show the C++ telemetry display
- Point out:
  - 20 drivers racing in real-time
  - 50Hz telemetry updates (tire wear, fuel, positions)
  - Track limits monitoring
  - Penalty enforcement
  - Multi-threaded producer-consumer architecture

"This is the FAST layer - deterministic C++ computing real-time race state at 50Hz. 
Millisecond decisions happen here: tire degradation, fuel burn, position updates."

**Part 2: The AI Strategic Layer (60 seconds)**
- Show Gemini AI output appearing
- Highlight key features:
  - Compact state summary (not raw 50Hz data)
  - Radio-style strategic calls
  - Multiple options with tradeoffs
  - Risk assessment and confidence levels

"This is the SMART layer - Gemini operates at lap/event timescales. 
It sees: 'Tire wear at 73%, optimal pit window lap 24, currently lap 22, P3, gap to P2 is 3.2s'
It outputs: 'Box next lap for undercut. Alternative: Stay out 2 more laps, risk tire cliff.'"

**Part 3: The "Wow Moment" (30 seconds)**
- Scroll back to show a strategic decision
- Explain the context: "Here, tire wear crossed 70% threshold"
- Show how Gemini provided 3 options within 2 seconds:
  - Option A: Pit now (safe)
  - Option B: Extend 1 lap (balanced)
  - Option C: Go long (risky, gamble on safety car)

"This is what race engineers do - they don't drive the car, they provide strategic guidance 
with reasoning. FARVIS does this with AI, making it accessible to sim racers and esports teams."

### Technical Deep Dive (if judges ask)

**Architecture:**
```
┌─────────────────────┐
│  C++ Telemetry      │  ← Real-time layer (50Hz)
│  - Thread-safe      │     Deterministic heuristics
│  - Ring buffer      │     Millisecond decisions
│  - Low latency      │
└──────┬──────────────┘
       │ JSON stream (stdout)
       ▼
┌─────────────────────┐
│  Python Bridge      │  ← Integration layer
│  - Reads JSON       │     Event detection
│  - Detects events   │     Call throttling
└──────┬──────────────┘
       │ Compact state summary
       ▼
┌─────────────────────┐
│  Gemini API         │  ← Strategic layer
│  - Context-aware    │     Lap/event timescale
│  - Options + risks  │     Natural language reasoning
└─────────────────────┘
```

**Why Two Layers?**
- "You can't wait 200ms for an LLM when you need to adjust brake pressure in a corner"
- "But you CAN wait 1-2 seconds for strategic guidance between laps"
- "This is 'fast and slow AI' - we learned this in AI class (CMPT 310)"
- "Real F1 teams use similar architecture: real-time ECU + strategic pit wall"

**Data Flow:**
- C++ outputs ~3 JSON objects per lap (lap boundaries + key events)
- Each JSON is ~300 bytes (not MB of raw telemetry)
- Gemini sees: driver profile, tire %, fuel %, position, gaps, optimal windows
- Gemini returns: radio message, reasoning, 3 options, risk level, confidence

**Key Events That Trigger Strategy Calls:**
1. Lap boundaries
2. Tire wear > 70% threshold
3. Position changes in top 5
4. Gap changes > 2 seconds
5. (Future: Safety car, rain, mechanical issues)

### Value Proposition (30 seconds)

**Who is this for?**
- Sim racing community (iRacing, F1 games, Assetto Corsa)
- Esports teams wanting coaching/strategy
- Track day enthusiasts learning racecraft
- Educational tool for understanding F1 strategy

**Why is this better than existing solutions?**
- Most sim racing is "drive blind" - no strategic guidance
- Real F1 teams have 50+ engineers doing this
- FARVIS makes that accessible to everyone
- It's technically sound - not claiming unrealistic "AI drives the car"

### Closing (15 seconds)
"I built this solo in [X hours] because I love F1, low-latency systems, and AI. 
The C++ telemetry system is production-quality with thread safety and realistic modeling. 
The Gemini integration shows what's possible when you combine fast deterministic compute 
with intelligent reasoning. This is FARVIS - your AI race engineer."

## Anticipated Judge Questions

**Q: "How fast is the Gemini response time?"**
A: "Typically 1-2 seconds for the API call. That's fine because we call it at lap boundaries 
or key events, not in the middle of corners. Real F1 radio calls happen at similar timescales."

**Q: "Couldn't the C++ code just calculate the optimal strategy?"**
A: "It can and does - you can see the optimal pit lap from pre-race simulation. But racing 
is dynamic: gaps change, safety cars happen, tires behave differently than expected. 
Gemini adapts to the ACTUAL race state with natural language reasoning that explains WHY, 
not just WHAT. That's valuable for learning and trust."

**Q: "Is this just a wrapper around the Gemini API?"**
A: "No - the C++ telemetry system is fully custom: multithreaded architecture, realistic 
tire degradation modeling, penalty enforcement, track limits monitoring, position calculations. 
The Gemini integration is the cherry on top, showing how AI can augment (not replace) 
real-time systems."

**Q: "Why not use real F1 game telemetry?"**
A: "I could integrate with F1 23/24's UDP telemetry output. But for a hackathon, 
building the full stack shows systems thinking and control. Plus, I can model any scenario 
I want - safety cars, aggressive vs conservative drivers, different track characteristics."

**Q: "What's the Lone Wanderer story?"**
A: "Solo hacker. I wrote every line of C++ and Python. No frontend frameworks, no AI slop. 
Just technical depth: thread safety, ring buffers, producer-consumer patterns, API integration, 
realistic F1 modeling. This is the kind of project I'm proud to show."

## Technical Challenges Overcome

1. **Thread-safe telemetry with ring buffer** - Producer-consumer pattern with proper synchronization
2. **Realistic F1 modeling** - Driver profiles (aggression, consistency, tire mgmt), car performance, tire degradation
3. **Position calculation** - Accurate race positions accounting for laps, sector progress, pit stops
4. **Penalty system** - Track limits warnings, penalty enforcement during pit stops
5. **JSON output without breaking display** - stdout for JSON, stderr for human display
6. **Event-driven AI calls** - Smart throttling to avoid spam, trigger on meaningful events
7. **Prompt engineering** - Compact state representation, structured output format, radio-style language

## Demo Failure Contingency Plans

**If Gemini API is down:**
- "No problem - I have a mock mode that shows the architecture"
- "The C++ telemetry system is the real showcase anyway"

**If compilation fails:**
- Have pre-compiled binary ready
- Have screen recording as backup

**If terminal display is messy:**
- Clear and restart
- Have screenshots of good runs

**If JSON parsing breaks:**
- Fall back to traditional mode (pure C++ display)
- Explain what WOULD happen with integration

## Post-Demo: Devpost Assets

**Title:**
"FARVIS - F1 Race Engineer AI Copilot (Powered by Gemini)"

**Tagline:**
"Every great leader has a great #2. This is JARVIS for F1 drivers."

**Technologies:**
- C++17 (multithreading, real-time systems)
- Python 3
- Google Gemini 2.0 Flash
- Terminal UI (no frontend frameworks)

**Tracks:**
- Best Use of Gemini API (primary)
- Lone Wanderer Award (solo hacker)

**Video:**
- 2 minute screen recording
- Show C++ telemetry + Gemini output
- Explain architecture
- Highlight "wow moment"

**GitHub:**
- Clean README
- Architecture diagram
- Setup instructions
- Example output

## Timing Breakdown

- **Setup**: 30 seconds
- **Hook**: 15 seconds
- **Technical showcase**: 90 seconds
- **Questions**: 60 seconds
- **Total**: ~3 minutes (perfect for hackathon judging)
