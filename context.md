# Hackathon Context Summary (for Claude/Copilot)

## Constraints / Setup
- I’m a **solo hacker** (“Lone Wanderer” eligible).
- I have **~5 hours left** to build + submit on **Devpost** (overview + details + working demo/video).
- I want something I’m **actually proud of** and that aligns with my interests (not a generic front-end).
- I’m willing to use a minimal/no-UI approach (CLI/logs/terminal dashboard) and **avoid a sloppy v0/Lovable front-end**.

## Prize Tracks Mentioned
1. **Best use of Gemini API**
2. **Best pitch using Alpha Foundry**
3. **Best UI by Huion** (NOT targeting; I don’t have/plan to use Huion)
4. **Surge Choice Award** (general “best project” vibe)
5. **Lone Wanderer Award** (solo hacker award — primary target)

## What I’m Targeting (Strategy)
- Primary target: **Lone Wanderer Award**
- Secondary target: **Best use of Gemini API**
- Surge Choice is possible if demo is memorable, but not the main plan.

## High-Level Project Idea (Selected Direction)
**Race Strategist / Race Engineer Copilot**
- Core: a **thread-safe, low-latency C++ race simulator** (existing/repurposable project).
- Sim outputs **telemetry/state** (JSON/log stream): lap times, gaps, tire wear/temps, fuel, aggression params, traffic, events (safety car, etc.).
- A lightweight glue layer (Python/Node) can read telemetry and optionally expose an API, but UI is optional.
- **Gemini is NOT in the real-time control loop**:
  - Real-time decisions are computed by deterministic heuristics in C++/local logic.
  - Gemini is used at **lap/event timescales** to produce:
    - short “radio-style” calls (e.g., “Box lap 14”, “Plan B”),
    - 2–3 options + tradeoffs,
    - risk warnings.

## Framing / Audience (Important)
- Don’t claim “F1 driver mid-corner real-time AI.”
- Position as decision support for **pit wall / race engineer** on **seconds-to-lap** timescales.
- Even better hackathon framing: **sim racing / esports race engineer copilot** (more believable and relatable).

## Demo Style (Preferred)
- **No front-end required**.
- Demo can be:
  - CLI output + clean formatted logs, optionally a terminal dashboard.
  - Show parameter changes (aggression/tire wear/safety car probability) and how:
    - telemetry shifts,
    - heuristics detect events,
    - Gemini adapts strategy calls.

## Relevant Background / Skills / Assets I Mentioned
- Strong interest in: **C++**, **Python**, **AI**, technical/systems projects.
- Projects I can repurpose / related experience:
  - C++ multithreaded low-latency race sim (tire wear, aggression, realistic results, thread-safe updates).
  - RISC-V pipeline simulator, cache simulator, processor simulator.
  - NIDS using GAN.
  - AI agent “debate/argument” system for compliance auditing (AWS-based).
- I want the project to feel authentic, technically deep, and pitchable.

## Key Talking Point for Judges
- “Gemini isn’t running the car — it’s acting like a race engineer:
  it takes compact telemetry summaries from a real-time C++ sim and produces concise strategy/radio calls with tradeoffs.”
