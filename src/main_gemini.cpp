#include "ingestion/RingBuffer.h"
#include "telemetry/TelemetryGenerator.h"
#include "strategy/StrategyAnalyzer.h"
#include "data/season_data.h"
#include "race-control/TrackLimitsMonitor.h"
#include "race-control/PenaltyEnforcer.h"
#include <thread>
#include <chrono>
#include <iostream>
#include <fstream>
#include <vector>
#include <atomic>
#include <algorithm>
#include <sstream>

using namespace std;

// JSON output for Gemini integration
void outputJsonTelemetry(const TelemetryFrame& frame, 
                         const DriverProfile& driver,
                         uint32_t optimal_pit_lap,
                         uint32_t total_laps,
                         float overtaking_difficulty,
                         float safety_car_prob) {
    // Output compact JSON to stdout for Python to consume
    cout << "{";
    cout << "\"driver_id\":" << frame.driver_id << ",";
    cout << "\"driver_name\":\"" << driver.driver_id << "\",";
    cout << "\"current_lap\":" << frame.lap << ",";
    cout << "\"total_laps\":" << total_laps << ",";
    cout << "\"race_position\":" << int(frame.race_position) << ",";
    cout << "\"sector\":" << int(frame.sector) << ",";
    cout << "\"tire_wear_percent\":" << (frame.tire_wear * 100) << ",";
    cout << "\"speed_kmh\":" << frame.speed_kph << ",";
    cout << "\"throttle\":" << frame.throttle << ",";
    cout << "\"brake\":" << frame.brake << ",";
    cout << "\"is_pitting\":" << (frame.speed_kph == 0.0f ? "true" : "false") << ",";
    cout << "\"aggression\":" << driver.aggression << ",";
    cout << "\"tire_management\":" << driver.tire_management << ",";
    cout << "\"consistency\":" << driver.consistency << ",";
    cout << "\"optimal_pit_lap\":" << optimal_pit_lap << ",";
    cout << "\"overtaking_difficulty\":" << overtaking_difficulty << ",";
    cout << "\"safety_car_prob\":" << safety_car_prob;
    cout << "}" << endl;
}

vector<uint32_t> parseDriverIds(const string& input, size_t max_id){
    vector<uint32_t> driver_ids;
    stringstream ss(input);
    string id;
    while(getline(ss, id, ',')){
        if(id.empty()) continue;
        try {
            int val = stoi(id);
            if(val >= 0 && static_cast<size_t>(val) < max_id) {
                driver_ids.push_back(static_cast<uint32_t>(val));
            }
        } catch(...) {
            // Skip invalid entries
        }
    }
    return driver_ids;
}

int main(){

    atomic<bool> done(false);

    TrackProfile track = {
        .track_id = 1,
        .sectors = 3,
        .lap_length_km = 10.0f,
        .tire_wear_factor = 1.0f,
        .overtaking_difficulty = 0.1f,
        .safety_car_probability = 0.01f,
    };
    
    const vector<DriverProfile>& drivers = SeasonData::DRIVERS;
    const vector<CarProfile>& cars = SeasonData::CARS;

    uint32_t total_laps = 52;

    // Check for Gemini mode (output JSON for AI integration)
    bool gemini_mode = false;
    if(getenv("FARVIS_GEMINI_MODE")) {
        gemini_mode = true;
        cerr << "FARVIS MODE: Outputting JSON telemetry for Gemini AI\n";
    }

    // Ask user about strategy optimization
    if(!gemini_mode) {
        cerr << "\nRun strategy analysis? (y/n): ";
    }
    string response;
    getline(cin, response);

    map<uint32_t, uint32_t> optimal_strategies;

    if (response == "y" || response == "Y") {
        if(!gemini_mode) {
            cerr << "\nAvailable drivers:\n";
            for(uint32_t i = 0; i < drivers.size(); i++) {
                cerr << i << ": " << drivers[i].driver_id << "\n";
            }
            
            cerr << "\nEnter driver IDs to optimize (comma-separated, no spaces): ";
        }
        string input;
        getline(cin, input);
        
        vector<uint32_t> driver_ids = parseDriverIds(input, drivers.size());
        
        if(!driver_ids.empty()) {
            if(!gemini_mode) {
                cerr << "\nAnalyzing strategies (this may take 10-30 seconds)...\n";
            }
            
            StrategyAnalyzer analyzer(track, drivers, cars, total_laps);
            vector<StrategyResult> results = analyzer.analyzeStrategies(driver_ids);
            
            if(!gemini_mode) {
                cerr << "\nStrategy Analysis Results:\n";
                cerr << "==========================\n";
            }
            for(const auto& result : results) {
                if(!gemini_mode) {
                    cerr << drivers[result.driver_id].driver_id 
                        << ": Pit lap " << result.optimal_pit_lap 
                        << " (finish time: " << (result.finish_time_seconds / 60.0f) << " min)\n";
                }
                optimal_strategies[result.driver_id] = result.optimal_pit_lap;
            }
            if(!gemini_mode) cerr << "\n";
        }
    }

    auto penalty_enforcer = std::make_shared<PenaltyEnforcer>(drivers);

    RingBuffer<TelemetryFrame> buffer(1024);
    TelemetryGenerator generator(track, drivers, cars, total_laps, penalty_enforcer);
    TrackLimitsMonitor track_limits_monitor(track, drivers, penalty_enforcer);

    if(!optimal_strategies.empty()) {
        generator.setOptimalStrategies(optimal_strategies);
    }

    // Select driver for FARVIS AI coaching (Gemini mode only)
    vector<uint32_t> json_output_drivers;
    
    if(gemini_mode) {
        cerr << "\n╔══════════════════════════════════════════════════════════╗\n";
        cerr << "║  FARVIS - Choose Your Driver for AI Coaching            ║\n";
        cerr << "╚══════════════════════════════════════════════════════════╝\n\n";
        
        cerr << "Available drivers:\n";
        for(uint32_t i = 0; i < drivers.size(); i++) {
            cerr << "  " << i << ": " << drivers[i].driver_id;
            cerr << " (Aggression: " << drivers[i].aggression;
            cerr << ", Tire Mgmt: " << drivers[i].tire_management << ")\n";
        }
        
        cerr << "\nEnter driver number (0-" << (drivers.size()-1) << "): ";
        string input;
        getline(cin, input);
        
        try {
            int driver_choice = stoi(input);
            if(driver_choice >= 0 && static_cast<size_t>(driver_choice) < drivers.size()) {
                json_output_drivers.push_back(static_cast<uint32_t>(driver_choice));
                cerr << "\nFARVIS will coach " << drivers[driver_choice].driver_id << "!\n";
            } else {
                cerr << "\nInvalid choice, defaulting to Verstappen\n";
                json_output_drivers.push_back(0);
            }
        } catch(...) {
            cerr << "\nInvalid input, defaulting to Verstappen\n";
            json_output_drivers.push_back(0);
        }
        
        cerr << "\nPress Enter to start race...\n";
        string start;
        getline(cin, start);
        cerr << "\n🏁 Starting race with FARVIS coaching...\n\n";
    } else {
        cerr << "\nRace strategies:\n";
        cerr << "================\n";
        for (uint32_t i = 0; i < drivers.size(); i++) {
            cerr << drivers[i].driver_id << ": ";
            auto it = optimal_strategies.find(i);
            if (it != optimal_strategies.end()) {
                cerr << "Optimal pit lap " << it->second << "\n";
            } else {
                cerr << "Wear-based pitting\n";
            }
        }
        cerr << "\nPress Enter to start race...\n";
        cerr.flush();
        {
            string start;
            getline(cin, start);
        }
        cerr << "\nStarting race...\n\n";
        
        // Default: top 3 for non-Gemini mode
        json_output_drivers = {0, 1, 2};
    }

    thread producer([&]() {
        while(!done.load()){
            auto frames = generator.next();

            if(generator.isRaceFinished()) {
                done.store(true);
                buffer.shutdown();
                
                string winner = "";
                for(const auto& frame : frames) {
                    if(frame.race_position == 1) {
                        winner = drivers[frame.driver_id].driver_id;
                        break;
                    }
                }
                
                if(!gemini_mode) {
                    cerr << "\n🏁 RACE FINISHED! 🏁\n";
                    cerr << "🏆 Winner: " << winner << " 🏆\n";
                }

                break;
            }

            for(const auto &frame : frames){
                if(!buffer.push(frame)){
                    TelemetryFrame old_frame;
                    buffer.pop(old_frame);
                    if(!gemini_mode) {
                        cerr << "[Telemetry] Buffer full, dropping frame " << drivers[old_frame.driver_id].driver_id << "\n";
                    }
                    buffer.push(frame);
                }
            }
            this_thread::sleep_for(chrono::milliseconds(20));
        }
    });

    thread consumer([&]() {
        vector<TelemetryFrame> latestFrames(drivers.size());
        for(size_t i = 0; i < latestFrames.size(); i++) {
            latestFrames[i].driver_id = static_cast<uint32_t>(i);
            latestFrames[i].race_position = static_cast<uint8_t>(i + 1);
            latestFrames[i].lap = 0;
            latestFrames[i].sector = 1;
        }
        
        // Track last lap output per driver
        map<uint32_t, uint32_t> last_json_output_lap_per_driver;
        
        while(!done.load()){
            TelemetryFrame frame;

            if(!buffer.pop(frame)) {
                break;
            }

            track_limits_monitor.processFrame(frame);
            latestFrames[frame.driver_id] = frame;
            
            // Output JSON for Gemini (every lap for chosen driver)
            if(gemini_mode && 
               find(json_output_drivers.begin(), json_output_drivers.end(), frame.driver_id) != json_output_drivers.end()) {
                
                uint32_t current_lap = frame.lap;
                uint32_t last_lap = last_json_output_lap_per_driver[frame.driver_id];
                
                // Output at lap completion (sector 1 of new lap)
                if(current_lap > last_lap && frame.sector == 1 && current_lap > 1) {
                    auto opt_it = optimal_strategies.find(frame.driver_id);
                    uint32_t opt_pit = (opt_it != optimal_strategies.end()) ? opt_it->second : 0;
                    
                    outputJsonTelemetry(frame, drivers[frame.driver_id], opt_pit, 
                                      total_laps, track.overtaking_difficulty, 
                                      track.safety_car_probability);
                    
                    last_json_output_lap_per_driver[frame.driver_id] = current_lap;
                }
            }
            
            static size_t frameCount = 0;
            frameCount++;
            
            if(!gemini_mode && frameCount % drivers.size() == 0) {
                cerr << "\033[2J\033[H";
                
                uint32_t currentLap = 0;
                for(const auto& f : latestFrames) {
                    if(f.lap > currentLap) currentLap = f.lap;
                }
                
                cerr << "\n🏁 LAP " << currentLap << "/" << total_laps << " 🏁\n";
                cerr << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
                
                vector<TelemetryFrame> sortedFrames = latestFrames;
                sort(sortedFrames.begin(), sortedFrames.end(), 
                        [](const TelemetryFrame& a, const TelemetryFrame& b) {
                            return a.race_position < b.race_position;
                        });
                
                for(const auto& f : sortedFrames) {
                    string posColor = "\033[1;33m";
                    if(f.race_position == 1) posColor = "\033[1;93m";
                    else if(f.race_position == 2) posColor = "\033[1;37m";
                    else if(f.race_position == 3) posColor = "\033[1;91m";
                    
                    cerr << posColor << "P" << int(f.race_position);
                    if(f.race_position < 10) cerr << " ";
                    cerr << "\033[0m ";
                    
                    string emoji = "⚫";
                    string teamName = cars[f.driver_id].car_id;
                    if(teamName == "Red Bull") emoji = "🔵";
                    else if(teamName == "Ferrari") emoji = "🔴";
                    else if(teamName == "Mercedes") emoji = "⚪";
                    else if(teamName == "McLaren") emoji = "🟠";
                    else if(teamName == "Aston Martin") emoji = "🟢";
                    else if(teamName == "Alpine") emoji = "💙";
                    else if(teamName == "Haas") emoji = "⚪";
                    else if(teamName == "Racing Bulls") emoji = "🔷";
                    else if(teamName == "Williams") emoji = "💙";
                    else if(teamName == "Kick Sauber") emoji = "🟢";
                    
                    cerr << emoji << " ";
                    
                    string name = drivers[f.driver_id].driver_id;
                    cerr << "\033[1m" << name << "\033[0m";
                    for(size_t i = name.length(); i < 20; i++) cerr << " ";
                    
                    int barLength = 10;
                    float progress = (f.sector - 1) / float(track.sectors);
                    int filled = int(progress * barLength);
                    cerr << " ";
                    for(int i = 0; i < barLength; i++) {
                        if(i < filled) cerr << "█";
                        else cerr << "░";
                    }
                    
                    cerr << " Lap " << f.lap;
                    
                    if(f.speed_kph == 0.0f) {
                        cerr << "  \033[1;35m[IN PITS]\033[0m";
                    } else {
                        string speedColor = "\033[32m";
                        if(f.speed_kph < 150) speedColor = "\033[31m";
                        else if(f.speed_kph < 200) speedColor = "\033[33m";
                        
                        cerr << "  Speed: " << speedColor << int(f.speed_kph) << " kph\033[0m";
                    }
                    
                    float tirePercent = f.tire_wear * 100;
                    string tireColor = "\033[32m";
                    if(tirePercent > 70) tireColor = "\033[31m";
                    else if(tirePercent > 40) tireColor = "\033[33m";
                    
                    cerr << "  Tire: " << tireColor << int(tirePercent) << "%\033[0m";
                    
                    cerr << "\n";
                }
                
                cerr << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
                
                cerr << "\nTRACK LIMITS VIOLATIONS:\n";
                bool any_violations = false;
                for(const auto& f : sortedFrames) {
                    TrackLimitsState state = track_limits_monitor.getDriverState(f.driver_id);
                    DriverPenaltyInfo penalty = penalty_enforcer->getPenaltyInfo(f.driver_id);
                    
                    if(state.warnings > 0) {
                        any_violations = true;
                        cerr << "   " << drivers[f.driver_id].driver_id << ": ";
                        cerr << state.warnings << " warning" << (state.warnings > 1 ? "s" : "");
                        
                        if(penalty.state == PenaltyState::PENDING) {
                            cerr << " \033[1;33m[PENALTY PENDING]\033[0m";
                        } else if(penalty.state == PenaltyState::SERVING) {
                            cerr << " \033[1;31m[SERVING PENALTY]\033[0m";
                        } else if(penalty.state == PenaltyState::SERVED) {
                            cerr << " \033[1;32m[PENALTY SERVED]\033[0m";
                        }
                        cerr << "\n";
                    }
                }

                if(!any_violations) {
                    cerr << "   \033[90mNone\033[0m\n";
                }
                
                cerr << "\033[90mRace runs until finish\033[0m\n";
                cerr.flush();
            }
        }
    });

    producer.join();
    consumer.join();

    return 0;
}
