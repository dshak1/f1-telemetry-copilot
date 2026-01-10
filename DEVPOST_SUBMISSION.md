# FARVIS - F1 Race Engineer AI Copilot

## 🏎️ Inspiration

*"Every great leader has a great #2."*

Michael Jordan had Scottie Pippen. Iron Man had JARVIS. In Formula 1, every World Champion has a brilliant race engineer behind them - the strategic voice that turns real-time data into winning decisions.

**FARVIS (Fast, Adaptable, Reliable, Visionary, Insanely Stupendous)** brings that F1 race engineer experience to sim racing, esports, and amateur motorsport enthusiasts through AI-powered strategic guidance.

## 🎯 What It Does

FARVIS is a two-layer race strategy system:

### Layer 1: Real-Time Telemetry (C++)
- Simulates 20-driver F1 races with realistic physics
- Generates 50Hz telemetry: tire wear, fuel consumption, lap times, positions
- Enforces track limits with penalties
- Computes race positions accounting for pit stops and sector progress
- Thread-safe producer-consumer architecture with ring buffer

### Layer 2: Strategic AI (Gemini API)
- Receives compact race state summaries (not raw 50Hz data)
- Operates at lap/event timescales (seconds, not milliseconds)
- Provides radio-style strategic calls with reasoning
- Offers 2-3 options with tradeoffs and risk assessment
- Adapts to dynamic race conditions in real-time

## 🛠️ How I Built It

### Architecture
```
┌─────────────────────┐
│  C++ Telemetry      │  ← Real-time layer (50Hz)
│  - Thread-safe      │     Deterministic heuristics
│  - Ring buffer      │     Millisecond decisions
│  - 20 F1 drivers    │
└──────┬──────────────┘
       │ JSON stream (stdout)
       ▼
┌─────────────────────┐
│  Python Bridge      │  ← Integration layer
│  - Event detection  │     Smart throttling
│  - JSON parsing     │     Context building
└──────┬──────────────┘
       │ Compact state summary (~300 bytes)
       ▼
┌─────────────────────┐
│  Gemini 2.0 Flash   │  ← Strategic layer
│  - Context-aware    │     Natural language reasoning
│  - Multi-option     │     Risk assessment
│  - Radio-style      │     Confidence scoring
└─────────────────────┘
```

### Technical Implementation

**C++ Real-Time System:**
- Multi-threaded producer-consumer pattern
- Thread-safe ring buffer for telemetry frames
- Realistic driver profiles (aggression, consistency, tire management)
- Dynamic tire degradation modeling
- Track limits monitoring with 3-strike penalty system
- Penalty enforcement during pit stops
- Position calculation with lap-accurate distance tracking

**Python Integration Layer:**
- Reads JSON telemetry from C++ stdout
- Event-driven architecture (triggers on lap boundaries, tire thresholds, position changes)
- Throttles API calls to avoid spam (max 1 call per 3 seconds)
- Builds compact race state summaries for Gemini

**Gemini AI Integration:**
- Structured prompt engineering for consistent output format
- Radio-style language (concise, actionable)
- Multiple strategic options with tradeoffs
- Risk level and confidence scoring
- Context-aware reasoning based on driver profile and race state

### Key Technical Challenges Solved

1. **Separating Fast and Slow AI**
   - Learned in CMPT 310: some decisions need milliseconds, others can take seconds
   - C++ handles the "fast thinking", Gemini handles the "slow thinking"

2. **Thread-Safe Telemetry**
   - Producer thread generates frames at 50Hz
   - Consumer thread processes and displays
   - Ring buffer with proper synchronization prevents data races

3. **JSON Output Without Breaking Display**
   - C++ writes human-readable output to stderr
   - Writes JSON to stdout for Python to consume
   - Clean separation of concerns

4. **Event-Driven AI Calls**
   - Don't spam Gemini with every frame (50Hz would be wasteful)
   - Trigger on meaningful events: lap boundaries, tire wear thresholds, position changes
   - Smart throttling prevents duplicate calls

5. **Realistic F1 Modeling**
   - 2025 F1 grid with accurate driver profiles
   - Tire degradation based on aggression and track characteristics
   - Pit stop timing optimization
   - Track limits monitoring (FIA-style 3 warnings = penalty)

## 🚀 What's Next for FARVIS

### Near-Term Enhancements
- **Live F1 game integration**: Read UDP telemetry from F1 23/24, iRacing, Assetto Corsa
- **Voice output**: Text-to-speech for hands-free radio-style calls
- **Safety car events**: Model VSC/SC and strategic opportunities
- **Multi-driver comparison**: "Your teammate is 0.3s faster in Sector 2, adjust line"
- **Historical analysis**: Post-race debriefs with "what if" scenarios

### Long-Term Vision
- **Esports team tool**: Real-time strategic support for competitive sim racing
- **Educational platform**: Teach racecraft and strategy to aspiring drivers
- **Track day companion**: Analyze telemetry from real amateur racing
- **Multiplayer strategy**: Coordinate team strategies in endurance races

## 💡 Key Innovation: Two-Layer Architecture

The critical insight is that **AI doesn't need to be in the real-time control loop** to be valuable.

❌ **What We DON'T Do:**
- Claim "AI controls the car in real-time" (unrealistic with LLM latency)
- Send raw 50Hz telemetry to Gemini (wasteful, expensive)
- Make millisecond decisions with cloud API calls

✅ **What We DO:**
- Let C++ handle real-time compute (it's fast and deterministic)
- Use Gemini for strategic reasoning (it's smart and context-aware)
- Call AI at lap/event timescales where 1-2 second latency is acceptable
- Provide multiple options with reasoning (builds trust and learning)

This mirrors how real F1 teams work:
- **ECU/Sensors**: Real-time data acquisition and control
- **Race Engineer**: Strategic decisions based on data analysis
- **Driver**: Executes strategy while adapting to conditions

FARVIS is the "race engineer" layer - the strategic brain that turns data into decisions.

## 🏆 Challenges & Tracks

**Primary:** Best Use of Gemini API
- Novel application of LLMs to real-time sports strategy
- Smart prompt engineering for structured, actionable output
- Event-driven architecture that respects API rate limits
- Demonstrates understanding of when/where AI adds value

**Secondary:** Lone Wanderer Award
- Solo project, every line of code written by me
- No framework slop, no copy-paste
- Deep technical implementation from systems to AI
- Authentic project I'm genuinely proud of

## 🎓 What I Learned

### Technical Skills
- **C++ concurrency**: Thread-safe patterns, mutexes, atomics, ring buffers
- **Systems design**: Separating concerns, producer-consumer, event-driven architecture
- **API integration**: Prompt engineering, structured output, error handling
- **Real-time systems**: 50Hz telemetry generation, low-latency processing

### Domain Knowledge
- **F1 strategy**: Pit windows, tire degradation, undercut/overcut tactics
- **Race engineering**: What information matters, how to communicate it
- **Sim racing**: Existing tools and gaps in the market

### AI Insights
- **Fast vs slow thinking**: Not everything needs AI (CMPT 310 concepts applied)
- **LLM limitations**: Latency makes real-time control impractical
- **LLM strengths**: Reasoning, multi-option analysis, natural language
- **Prompt design**: Structured format, compact context, clear constraints

## 🛠️ Built With

- **C++17** - Real-time telemetry system, multithreading, low-latency compute
- **Python 3** - Integration layer, JSON parsing, API calls
- **Google Gemini 2.0 Flash** - Strategic reasoning and decision support
- **Terminal UI** - No frontend frameworks (authentic, technical focus)

## 🚦 Try It Out

### Prerequisites
- C++ compiler with C++17 support
- Python 3.8+
- Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Quick Start
```bash
# Clone the repo
git clone [your-repo-url]
cd f1-telemetry-copilot

# Set up API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the demo
bash run_farvis_demo.sh
```

### What You'll See
1. C++ telemetry system compiling
2. Python environment setup
3. Race simulation starting
4. Real-time leaderboard with tire wear, positions, speeds
5. Gemini AI providing strategic calls every lap
6. Multiple options with reasoning and risk assessment

## 📊 Technical Metrics

- **C++ Code**: ~2000 lines across 15 files
- **Python Code**: ~400 lines in 1 file
- **Telemetry Frequency**: 50Hz (20ms intervals)
- **JSON Output Rate**: ~3 objects per lap per driver
- **Gemini Response Time**: 1-2 seconds typical
- **Total Race Simulation**: 52 laps, ~20 minutes real-time
- **Drivers Simulated**: 20 (full 2025 F1 grid)

## 🎥 Demo Video

[Link to screen recording showing:]
- Compilation and setup
- Race simulation running
- Gemini providing strategic guidance
- Explanation of architecture
- "Wow moment" of adaptive strategy

## 👤 About Me

Solo hacker passionate about:
- Low-latency systems and C++
- AI/ML applications
- Formula 1 and motorsport
- Building technically deep projects

Other projects:
- RISC-V pipeline simulator
- Cache simulator with LRU/MRU policies
- Network Intrusion Detection System using GANs
- AI agent debate system for compliance

Currently taking CMPT 310 (AI course) where I learned about search algorithms, optimization, and fast vs slow AI - concepts directly applied in FARVIS.

---

**FARVIS**: Because every great driver deserves a great race engineer. 🏎️🏆
