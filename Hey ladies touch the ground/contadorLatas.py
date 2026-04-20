import json
import os

# Esto es para leer directamente de la carpeta, no se pq no me va el ./ xd
folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_m1():
    print("\n====================\n")
    print("\nMETRICA DE LATAS GENERADAS\n")
    
    archivos_validos = 0
    
    # Buscamos Jsons
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r") as f:
                events = [json.loads(line) for line in f]
            
            latas_por_partida = {}
            
            for event in events:
                if "matchId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} / partida {match_id}"
                    
                    if clave_partida not in latas_por_partida:
                        latas_por_partida[clave_partida] = 0
                        
                    if event["eventType"] == "can_appears":
                        latas_por_partida[clave_partida] += 1
            
            print(f"\nArchivo analizado: {filename}\n")
            for partida, total_latas in latas_por_partida.items():
                print(f" - {partida} : {total_latas} latas generadas")
                
    print("\n====================\n\n")

### Main section ###
if __name__ == "__main__":
    calculate_m1()