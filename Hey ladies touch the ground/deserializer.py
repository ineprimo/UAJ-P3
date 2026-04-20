import json
import os
import pandas as pd
import matplotlib.pyplot as plt

folder_path = "./"

def gameSession(event_list):
    sessionMatchesTimes = []
    clicks = []

    for currentEvent in event_list:
        if currentEvent["eventType"] == "match_start":
            tsMatchStart = currentEvent["timestamp"]
        if currentEvent["eventType"] == "match_end":
            tsMatchEnd = currentEvent["timestamp"]
            sessionMatchesTimes.append(tsMatchEnd - tsMatchStart)
        if currentEvent["eventType"] == "mouse_click":
            clicks.append((currentEvent["x"], currentEvent["y"]))


    return sessionMatchesTimes, clicks

def processTimes(session_times, session_number):
    i = 0
    for matchTime in session_times:
        totalSeconds = matchTime / 1000
        minutes = int(totalSeconds / 60)
        remainingSeconds = totalSeconds % 60
        print(f"Session {session_number} match {i} time: {minutes}:{remainingSeconds} minutes")

        i += 1

#TODO: que se haga por cada match y no por sesion?
def processClicks(session_clicks, session_number):
    heatmap = pd.DataFrame(session_clicks, columns=["x", "y"])

    if not heatmap.empty:
        plt.figure(figsize=(10, 6))
        
        bg_path = "background2.png" 
        if os.path.exists(bg_path):
            img = plt.imread(bg_path)
            height, width = img.shape[:2]
            plt.imshow(img, extent=[0, width, 0, height])

        plt.hist2d(heatmap["x"], heatmap["y"], bins=50, cmap="spring", alpha=0.6, 
                    range=[[0, width], [0, height]], cmin=1)
        plt.colorbar(label="Densidad de clicks")
        plt.title(f"Mapa de Calor de Clicks - Sesión {session_number}")
        plt.show()

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

            sessionMatchesTimes, clicks = gameSession(data)

            processTimes(sessionMatchesTimes, s)
            processClicks(clicks, s)

            s += 1



            
    


