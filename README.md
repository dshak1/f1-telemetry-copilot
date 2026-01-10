F1 telemetry using Gemini API I need a wow moment on combining F1 idea from my 310 class low latency C++ google Gemini API. F1 teams run thousands of simulations sending millions to optimize everything they can and yet there is only one winner. Every great leader has a great #2 MJ had Scotty, iron man had jarvis. This idea that all of the greats have a great number two transcends niches. Soul would hurt to give you another AI, lovable V0 slop front end. So I limited my scope to something I'm really passionate about. I hope I did alright to convey that F1 plus JARVIS equals FARVIS. What does it stand for? Fast, adaptable, reliable. Visionary. Insanely stupendous.
I need some sort of, I don't know, wow moment, probably to impress the judges. What can that be? I could change aggression and then within two seconds Gemini changes the pit call with reasons. Or for the yeah, that could be a good idea.

I need some sort of, I don't know, wow moment, probably to impress the judges. What can that be? I could change aggression and then within two seconds Gemini changes the pit call with reasons. Or for the yeah, that could be a good idea. What does does is navigate uncertainty, fast and slow. AI. We talked about this in CMPT 310 you might say which one do you need? We actually need both for something to process it and to give you an actionable insight to the driver is just not possible. These things are done at like a millionth of a 2nd and yeah.

So what I'm combining is my love for low latency threat safety plus plus and the telemetry idea and also with actionable insights from Google Gemini API. I'm not sure if I'm going to yet implement it for something to give the F 1 teams or something to give like AA thing where like for example the tire is wearing down maybe an optimized time to when to stop for the tire or whether it's like I'm going to I don't know, but basically I'm going to use Gemini API and. Include it into my thread safe simulation of the races. Kind of maybe like a jarvis for F1 drivers, like, you know, Iron Man's jarvis.maybe i should bring my shirt acc no, it might look planned and forced and not within time scope even though everything was.

:00–0:45: pick the one sim mode you can stabilize (even if it’s simplified)

0:45–1:45: C++ → telemetry JSON stream (stdout, file, or socket)

1:45–2:45: FastAPI endpoint + loop that calls Gemini every X seconds (or on key events)

2:45–3:45: quick UI (v0/Lovable) + “Start race” + display engineer output

3:45–4:30: tighten prompts + add 2–3 “event” hooks (pit window, tire cliff, overtake chance)

4:30–5:00: Devpost writeup + record a short demo video

Yeah — Devil’s Advocate is right: Gemini (or any cloud LLM) is not “F1 driver in-the-corner” fast in the sense of milliseconds. If you frame it that way, it sounds stupid.

But you don’t need it to be that to make the project legit.

Who it’s for (realistically)
Not the driver
A driver can’t read paragraphs at 300 km/h. Even real F1 radio calls are short, pre-digested: “Box box”, “Plan B”, “Strat 3”, “Push now”, “Target +0.8”.
It is for the pit wall / race engineers (decision support)
Their decisions are often on the order of:
seconds to a lap (pit windows, undercut timing, tire cliff)
reacting to events (safety car, VSC, traffic, rain, DRS train)
That’s where an LLM can help: summarize telemetry + propose 2–3 options + risks.
Even cleaner for a hackathon: sim racing / esports
Make it “Race Engineer Copilot for sim racers”:
You can look at text between corners / straights
People actually want coaching + strategy
Judges will immediately relate
So: not F1 as in “Mercedes will deploy this.” More like:
“A race-engineer copilot for sim racing / amateur track days, inspired by F1 workflows.”
That framing is honest and still hype.
Is Gemini “fast enough” for actionable insight?
If you call Gemini every 100ms: no, once per lap, or on events (tire wear crosses threshold, safety car, gap closes),
then yes, it’s totally plausible.
For the demo, you design your system so the LLM is used where it makes sense:
Two-layer system (this is the key)
Real-time layer (C++): fast, deterministic, immediate
Computes pit windows, tire cliff detection, delta pace, clean-air vs traffic penalty
Produces a small “state summary” JSON
LLM layer (Gemini): slower, but higher-level
Turns that state into a radio-style call + justification
Offers 2 alternatives + risk note
Writes in a consistent format