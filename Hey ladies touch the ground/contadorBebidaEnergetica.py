import json
import os


folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_bebidas_energeticas():
    print("\n=======================================================")
    print("\nBEBIDAS ENERGETICAS USADAS\n")
    
    archivos_validos = 0
    
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding='utf-8') as f:
                events = [json.loads(line) for line in f]
            
            bebidas_por_partida = {}
            inicio_partida = {} 
            
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} / Partida {match_id}"
                    
                    if clave_partida not in bebidas_por_partida:
                        bebidas_por_partida[clave_partida] = []
                    
                    if event["eventType"] == "match_start":
                        inicio_partida[clave_partida] = event["timestamp"]
                    
                    if event["eventType"] == "energy_drink_used":
                        bebidas_por_partida[clave_partida].append(event["timestamp"])
            

            print(f"[{filename}]")
            for partida, timestamps in bebidas_por_partida.items():
                total = len(timestamps) 
                
                if total == 0:
                    print(f" -> {partida}: Ninguna bebida usada.")
                else:
                    print(f" -> {partida}: {total} bebidas usadas.")
                    
                    tiempo_inicio = inicio_partida.get(partida, 0)
                    
                    for i, ts in enumerate(timestamps):
                        tiempo_transcurrido = ts - tiempo_inicio
                        
                        totalSeconds = tiempo_transcurrido / 1000
                        minutes = int(totalSeconds / 60)
                        remainingSeconds = totalSeconds % 60
                        
                        print(f"      - Bebida {i+1} usada en el minuto {minutes}:{remainingSeconds:05.2f}")
            print("-------------------------------------------------------")
            

if __name__ == "__main__":
    calculate_bebidas_energeticas()