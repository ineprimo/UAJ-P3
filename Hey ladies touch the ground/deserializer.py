import json
import os

folder_path = "./"

def gameSession(event_list):
    sessionMatchesTimes = []

    for currentEvent in event_list:
        if currentEvent["eventType"] == "match_start":
            tsMatchStart = currentEvent["timestamp"]
        if currentEvent["eventType"] == "match_end":
            tsMatchEnd = currentEvent["timestamp"]
            sessionMatchesTimes.append(tsMatchEnd - tsMatchStart)

    return sessionMatchesTimes

### Main section ###
if __name__ == "__main__":
    s = 0
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):

            file_path = os.path.join(folder_path, filename)

            print("Processing file: " + file_path)

            with open(file_path, "r") as f:
                data = []
                for line in f:
                    data.append(json.loads(line))

            sessionMatchesTimes = gameSession(data)
            i = 0
            for matchTime in sessionMatchesTimes:
                totalSeconds = matchTime / 1000
                minutes = int(totalSeconds / 60)
                remainingSeconds = totalSeconds % 60
                print("Session " + str(s) + " match " + str(i) + " time: " + str(minutes) + ":" + str(remainingSeconds) + " minutes")

                i += 1
            s += 1


            
    


