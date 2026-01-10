# 📋 FARVIS PROJECT INDEX

Quick navigation to all project files and their purposes.

---

## 🚀 START HERE

**First time?** → `READY_TO_SUBMIT.md`
**Quick reference?** → `DEMO_CHEAT_SHEET.md`
**Full overview?** → `PROJECT_SUMMARY.md`

---

## 📁 FILE GUIDE

### 🏃 Executable Scripts (READY TO RUN)

| File | Purpose | When to Use |
|------|---------|-------------|
| `test_setup.sh` | Verify everything works | Before anything else |
| `run_traditional.sh` | C++ only mode | Test telemetry system |
| `run_farvis_demo.sh` | **C++ + Gemini (MAIN DEMO)** | **Demo for judges** |
| `create_submission_package.sh` | Generate submission files | Before submitting |

---

### 📚 Documentation (READ FOR DEMO)

#### Essential (Read These!)
| File | Purpose | Audience |
|------|---------|----------|
| `READY_TO_SUBMIT.md` | **Complete submission guide** | **You (prep)** |
| `DEMO_SCRIPT.md` | **2-3 minute presentation** | **You (judges)** |
| `DEMO_CHEAT_SHEET.md` | **Quick reference card** | **You (during demo)** |
| `DEVPOST_SUBMISSION.md` | **Full Devpost writeup** | **Copy to Devpost** |
| `README_NEW.md` | **Main project README** | **Use as README.md** |

#### Supporting (Reference)
| File | Purpose | When Needed |
|------|---------|-------------|
| `PROJECT_SUMMARY.md` | Complete overview | Understanding scope |
| `ARCHITECTURE.md` | Visual diagrams | Technical questions |
| `IMPLEMENTATION_CHECKLIST.md` | What's done/next | Status tracking |
| `INDEX.md` | This file! | Navigation |

#### Context (Historical)
| File | Purpose | Note |
|------|---------|------|
| `CLAUDE_PROMPT.md` | Original brief | Background only |
| `context.md` | Brainstorming | Background only |
| `f1telemetryreadme.md` | Early notes | Background only |
| `README.md` | Old README | Replace with README_NEW.md |

---

### 💻 Source Code

#### Python (Gemini Integration)
| File | Purpose | Lines |
|------|---------|-------|
| `gemini_race_engineer.py` | **AI integration layer** | ~400 |
| `requirements.txt` | Python dependencies | ~2 |

#### C++ (Telemetry System)
| File | Purpose | Key Features |
|------|---------|--------------|
| `src/main.cpp` | Original simulation | Terminal display |
| `src/main_gemini.cpp` | **JSON output version** | **Gemini integration** |

#### C++ Headers/Implementation
```
src/
├── common/
│   └── types.h              # Core data structures (TelemetryFrame, etc.)
│
├── data/
│   └── season_data.h        # 2025 F1 grid (20 drivers, 10 teams)
│
├── ingestion/
│   └── RingBuffer.h         # Thread-safe ring buffer template
│
├── race-control/
│   ├── TrackLimitsMonitor.cpp/h  # 3 strikes → penalty
│   └── PenaltyEnforcer.cpp/h     # Penalty state machine
│
├── strategy/
│   ├── RaceSimulator.cpp/h       # Full race simulation
│   └── StrategyAnalyzer.cpp/h    # Pre-race optimization
│
└── telemetry/
    └── TelemetryGenerator.cpp/h  # 50Hz telemetry generation
```

---

### ⚙️ Configuration

| File | Purpose | Action Needed |
|------|---------|---------------|
| `.env.example` | API key template | Copy to `.env` and add key |

---

## 🎯 QUICK ACCESS BY TASK

### "I want to test the project"
1. `./test_setup.sh` - Verify everything works
2. `bash run_traditional.sh` - Test C++ system
3. `bash run_farvis_demo.sh` - Test full integration

### "I want to prepare for demo"
1. `DEMO_CHEAT_SHEET.md` - Quick reference
2. `DEMO_SCRIPT.md` - Presentation flow
3. `READY_TO_SUBMIT.md` - Complete guide

### "I want to submit to Devpost"
1. `DEVPOST_SUBMISSION.md` - Copy content from here
2. `./create_submission_package.sh` - Generate files
3. `READY_TO_SUBMIT.md` - Follow checklist

### "I want to understand the code"
1. `ARCHITECTURE.md` - Visual diagrams
2. `src/main_gemini.cpp` - Main integration
3. `gemini_race_engineer.py` - AI layer

### "I want to answer judge questions"
1. `DEMO_SCRIPT.md` - Q&A section
2. `DEMO_CHEAT_SHEET.md` - Quick answers
3. `ARCHITECTURE.md` - Technical details

---

## 📊 FILE STATISTICS

### Documentation
- **Essential docs**: 5 files (~15,000 words)
- **Supporting docs**: 4 files (~10,000 words)
- **Context docs**: 4 files (~2,000 words)

### Code
- **C++ files**: 15 files (~2,000 lines)
- **Python files**: 1 file (~400 lines)
- **Scripts**: 4 files (~300 lines)

### Total Project
- **~30 files**
- **~2,700 lines of code**
- **~27,000 words of documentation**
- **Documentation : Code ratio = 10:1** (thorough!)

---

## 🎬 DEMO DAY WORKFLOW

### Pre-Demo (30 min before)
1. Open `DEMO_CHEAT_SHEET.md` on second screen
2. Run `./test_setup.sh` to verify
3. Review `DEMO_SCRIPT.md` once more
4. Set font size to 14-16 in terminal
5. Clear any sensitive info from desktop

### During Demo (2-3 min)
1. Follow `DEMO_SCRIPT.md` flow
2. Reference `DEMO_CHEAT_SHEET.md` if stuck
3. Run `bash run_farvis_demo.sh`
4. Show strategic outputs
5. Explain architecture

### Post-Demo Q&A
1. Use `DEMO_CHEAT_SHEET.md` for quick answers
2. Reference `ARCHITECTURE.md` for technical depth
3. Point to `DEVPOST_SUBMISSION.md` for details

---

## 🏆 SUBMISSION WORKFLOW

### Assets Needed
- [ ] Demo video (from recording session)
- [ ] 3-5 screenshots (terminal, outputs, architecture)
- [ ] GitHub repo URL (or submission package ZIP)
- [ ] Content from `DEVPOST_SUBMISSION.md`

### Devpost Form Sections
1. **Title/Tagline** → Copy from `DEVPOST_SUBMISSION.md`
2. **What it does** → Copy from `DEVPOST_SUBMISSION.md`
3. **How we built it** → Copy from `DEVPOST_SUBMISSION.md`
4. **Challenges** → Copy from `DEVPOST_SUBMISSION.md`
5. **Accomplishments** → Copy from `DEVPOST_SUBMISSION.md`
6. **What we learned** → Copy from `DEVPOST_SUBMISSION.md`
7. **What's next** → Copy from `DEVPOST_SUBMISSION.md`

### Prize Tracks
- ☑ Best Use of Gemini API (primary)
- ☑ Lone Wanderer Award (solo)

---

## 💡 PRO TIPS

### When Reading Code:
- Start with `src/main_gemini.cpp` (integration)
- Then `gemini_race_engineer.py` (AI layer)
- Then `src/telemetry/TelemetryGenerator.cpp` (core)

### When Preparing Demo:
- Read `DEMO_CHEAT_SHEET.md` first
- Practice with `DEMO_SCRIPT.md`
- Reference `READY_TO_SUBMIT.md` for details

### When Answering Questions:
- Technical: `ARCHITECTURE.md`
- Strategy: `DEVPOST_SUBMISSION.md`
- Quick facts: `DEMO_CHEAT_SHEET.md`

---

## 🔍 FIND SPECIFIC CONTENT

### "Where's the elevator pitch?"
→ `DEMO_CHEAT_SHEET.md` (30-second version)
→ `DEMO_SCRIPT.md` (full version)

### "Where's the architecture diagram?"
→ `ARCHITECTURE.md` (visual ASCII art)
→ `DEVPOST_SUBMISSION.md` (text description)

### "Where's the judge Q&A prep?"
→ `DEMO_SCRIPT.md` (detailed Q&A)
→ `DEMO_CHEAT_SHEET.md` (quick answers)

### "Where's the Devpost content?"
→ `DEVPOST_SUBMISSION.md` (complete writeup)

### "Where's the technical depth?"
→ `ARCHITECTURE.md` (system design)
→ `src/` (code)

### "Where's the prize justification?"
→ `DEMO_SCRIPT.md` (detailed)
→ `DEMO_CHEAT_SHEET.md` (summary)
→ `PROJECT_SUMMARY.md` (comprehensive)

---

## ✅ QUICK HEALTH CHECK

Run these commands to verify everything is ready:

```bash
# All files present?
ls -1 *.md *.sh *.py src/ 2>&1 | grep -v "cannot access"

# Scripts executable?
ls -la *.sh | grep "^-rwx"

# Code compiles?
./test_setup.sh

# Documentation readable?
wc -w *.md

# Ready to demo?
echo "YES!" # You are!
```

---

## 🎉 YOU'RE READY!

Every file serves a purpose. Every document is complete. Every script works.

**Now go build your demo and win this thing!** 🏎️🏆

---

**Questions? Check the relevant file above. Everything you need is here.**
