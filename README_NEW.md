# 🏎️ FARVIS - F1 Race Engineer AI Copilot

**F**ast **A**daptable **R**eliable **V**isionary **I**nsanely **S**tupendous

> *"Every great leader has a great #2. MJ had Scottie, Iron Man had JARVIS. This is FARVIS - your AI race engineer."*

An F1 race strategy system combining low-latency C++ telemetry with Google Gemini AI for intelligent strategic decision-making.

## 🎯 Project Overview

FARVIS is a two-layer race strategy system that demonstrates the principle of "fast and slow AI" - some decisions need milliseconds (handled by deterministic C++), while others can take seconds for deeper reasoning (handled by Gemini).

### The Problem
- Real F1 teams have 50+ engineers analyzing telemetry and making strategic calls
- Sim racers and esports teams lack this strategic support
- Existing tools provide data but no actionable strategic guidance
- AI needs to fit naturally into racing workflows (not claim to "drive the car")

### The Solution
**Layer 1: Real-Time Telemetry (C++)**
- Multi-threaded race simulation with 20 F1 drivers
- 50Hz telemetry generation (tire wear, fuel, positions, speeds)
- Thread-safe ring buffer for data management
- Track limits monitoring and penalty enforcement
- Realistic driver profiles and tire degradation

**Layer 2: Strategic AI (Gemini)**
- Receives compact race state summaries
- Operates at lap/event timescales (not milliseconds)
- Provides radio-style strategic calls with reasoning
- Offers multiple options with tradeoffs
- Adapts to dynamic race conditions

## 🚀 Quick Start

### Prerequisites
- C++ compiler with C++17 support (g++/clang)
- Python 3.8+
- Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Setup & Run

```bash
# 1. Set up your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 2. Run the demo
bash run_farvis_demo.sh
```

This will:
1. Compile the C++ telemetry system
2. Set up Python environment
3. Install dependencies
4. Start the race with Gemini integration

### Alternative: Traditional Mode (No AI)

```bash
bash run_traditional.sh
```

This runs just the C++ telemetry system without Gemini integration.

## 📁 Project Structure

```
f1-telemetry-copilot/
├── src/
│   ├── main.cpp              # Traditional race simulation
│   ├── main_gemini.cpp       # Gemini-integrated version
│   ├── common/
│   │   └── types.h           # Core data structures
│   ├── data/
│   │   └── season_data.h     # 2025 F1 grid data
│   ├── ingestion/
│   │   └── RingBuffer.h      # Thread-safe ring buffer
│   ├── race-control/
│   │   ├── TrackLimitsMonitor.cpp
│   │   └── PenaltyEnforcer.cpp
│   ├── strategy/
│   │   ├── RaceSimulator.cpp
│   │   └── StrategyAnalyzer.cpp
│   └── telemetry/
│       └── TelemetryGenerator.cpp
├── gemini_race_engineer.py   # Gemini AI integration layer
├── requirements.txt          # Python dependencies
├── run_farvis_demo.sh       # Main demo script
├── run_traditional.sh       # Traditional mode script
├── DEMO_SCRIPT.md           # Judge presentation guide
└── DEVPOST_SUBMISSION.md    # Full project writeup
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│  C++ Real-Time Telemetry System         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  • 50Hz telemetry generation            │
│  • Multi-threaded (producer-consumer)   │
│  • Thread-safe ring buffer              │
│  • Tire degradation modeling            │
│  • Track limits & penalties             │
│  • Position calculations                │
└──────────────┬──────────────────────────┘
               │ JSON stream (stdout)
               ▼
┌─────────────────────────────────────────┐
│  Python Integration Layer               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  • Event detection                      │
│  • JSON parsing                         │
│  • Call throttling                      │
│  • Context building                     │
└──────────────┬──────────────────────────┘
               │ Compact state summary (~300 bytes)
               ▼
┌─────────────────────────────────────────┐
│  Google Gemini 2.0 Flash API            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│  • Strategic reasoning                  │
│  • Multi-option analysis                │
│  • Risk assessment                      │
│  • Natural language output              │
└─────────────────────────────────────────┘
```

## ✨ Key Features

### Real-Time Telemetry (C++)
- **20 drivers** from 2025 F1 grid with unique profiles
- **Thread-safe architecture** with producer-consumer pattern
- **Realistic physics**: tire degradation, fuel burn, speed variation
- **Track limits**: FIA-style 3 warnings → 5-second penalty
- **Penalty enforcement** during pit stops
- **Beautiful terminal UI** with color-coded positions

### AI Strategic Layer (Gemini)
- **Event-driven**: Triggers on laps, tire thresholds, position changes
- **Smart throttling**: Max 1 call per 3 seconds (no spam)
- **Compact context**: ~300 bytes vs MB of raw telemetry
- **Structured output**: Radio message, reasoning, 3 options, risk, confidence
- **Radio-style language**: Concise, actionable (like real F1)

## 🎮 Example Output

### C++ Telemetry Display
```
🏁 LAP 22/52 🏁
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P1  🔴 Leclerc            ████████░░ Lap 22  Speed: 289 kph  Tire: 68%
P2  🔵 Verstappen         ████████░░ Lap 22  Speed: 287 kph  Tire: 71%
P3  ⚪ Hamilton           ████████░░ Lap 22  Speed: 285 kph  Tire: 73%
...
```

### Gemini Strategic Output
```
╔══════════════════════════════════════════════════════════════╗
║  🏎️  FARVIS RACE ENGINEER - LAP 22 - P3 - HAMILTON
╚══════════════════════════════════════════════════════════════╝

📻 RADIO: "Approaching pit window. Prepare for undercut."

🧠 REASONING: Tire wear at 73%, optimal pit window lap 24. 
Current gap to P2 is 2.1s - undercut opportunity available.

📊 STRATEGIC OPTIONS:
   A) Pit in 2 laps: Standard timing, safe strategy
   B) Undercut now: Jump Verstappen ahead, aggressive play  
   C) Overcut: Stay out, hope for clear air advantage

⚠️  RISK LEVEL: MEDIUM
📈 CONFIDENCE: 75%
```

## 🧠 Technical Deep Dive

### Why Two Layers?

**Fast Thinking (C++):**
- Brake pressure adjustments: 1-5ms
- Tire temperature modeling: 20ms (50Hz)
- Position calculations: Every frame
- Track limits detection: Real-time

**Slow Thinking (Gemini):**
- Pit stop timing: 1-2 seconds acceptable
- Strategy adaptation: Between laps
- Multi-option analysis: When you have time to think
- Learning explanations: For post-lap review

### Key Technical Achievements

1. **Thread-Safe Ring Buffer**
   - Producer thread: 50Hz telemetry generation
   - Consumer thread: Display and JSON output
   - Lock-free where possible, mutexes where needed

2. **Realistic F1 Modeling**
   - Driver aggression affects tire wear
   - Tire degradation is non-linear
   - Pit stops have variable durations
   - Track characteristics affect strategy

3. **Event-Driven AI Integration**
   - Don't call Gemini every frame (wasteful)
   - Trigger on: lap boundaries, tire thresholds, position changes
   - Throttle to prevent duplicate calls
   - Cache results to reduce API usage

4. **Clean Data Flow**
   - C++: stderr for human display, stdout for JSON
   - Python: stdin for JSON, stdout for Gemini output
   - No file I/O needed (pure pipes)

## 📈 Performance Metrics

- **Telemetry Rate**: 50Hz (20ms intervals)
- **JSON Output**: ~3 objects per lap per driver
- **Gemini Latency**: 1-2 seconds typical
- **Memory Usage**: <50MB for full simulation
- **CPU Usage**: ~30% on single core (multithreaded)

## 🎓 What I Learned

### Technical
- C++ concurrency patterns (mutexes, atomics, ring buffers)
- Producer-consumer architecture at scale
- Real-time vs batch processing tradeoffs
- Prompt engineering for structured LLM output

### Domain
- F1 strategy: undercut, overcut, tire cliffs, fuel saving
- Race engineering: what data matters, how to communicate
- Sim racing community needs and gaps

### AI
- When to use AI vs deterministic algorithms
- LLM latency characteristics
- Structured output with prompt engineering
- Building trust through multi-option reasoning

## 🏆 Hackathon Strategy

**Target Awards:**
1. **Best Use of Gemini API** - Novel sports strategy application
2. **Lone Wanderer Award** - Solo hacker, no frameworks, deep technical work

**Key Differentiators:**
- Not claiming "AI drives the car" (realistic framing)
- Two-layer architecture shows systems thinking
- Production-quality C++ code (thread safety, performance)
- Clear value proposition for sim racing community

## 🔮 Future Enhancements

**Near-term:**
- Live F1 game integration (UDP telemetry from F1 23/24)
- Voice output for hands-free operation
- Safety car event modeling
- Weather and tire compound strategies

**Long-term:**
- Esports team dashboard
- Educational platform for racecraft
- Track day telemetry analysis
- Multiplayer strategy coordination

## 🤝 Contributing

This is a hackathon solo project, but ideas and feedback are welcome!

## 📄 License

MIT License - see LICENSE file

## 👤 Author

Built by a solo hacker passionate about F1, systems programming, and AI.

**Other projects:**
- RISC-V pipeline simulator
- Cache simulator with LRU/MRU policies
- Network Intrusion Detection using GANs
- AI agent debate system

---

**FARVIS**: Because every great driver deserves a great race engineer. 🏎️🏆
