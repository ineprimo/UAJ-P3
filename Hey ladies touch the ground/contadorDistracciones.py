import json
import os

folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_m4():
    print("\n=======================================================")
    print("\nMÉTRICA 4: CANTIDAD DE DISTRACCIONES DE CADA TIPO\n")
    
    archivos_validos = 0
    
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding='utf-8') as f:
                events = [json.loads(line) for line in f]
            
            distracciones_por_partida = {}
            
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} / Partida {match_id}"
                    
                    if clave_partida not in distracciones_por_partida:
                        distracciones_por_partida[clave_partida] = {}
                    
                    if event["eventType"] == "distraction_spawned":
                        if "distractionType" in event:
                            tipo_distraccion = event["distractionType"]
                            
                            if tipo_distraccion not in distracciones_por_partida[clave_partida]:
                                distracciones_por_partida[clave_partida][tipo_distraccion] = 0
                                
                            # suma
                            distracciones_por_partida[clave_partida][tipo_distraccion] += 1
            
            print(f"[{filename}]")
            for partida, conteo_tipos in distracciones_por_partida.items():
                print(f" -> {partida}:")
                if not conteo_tipos:
                    print("      - Ninguna distracción registrada en esta partida.")
                else:
                    for tipo, total in conteo_tipos.items():
                        print(f"      - {tipo}: {total}")
            print("-------------------------------------------------------")
            
    if archivos_validos == 0:
        print("No se encontraron archivos de telemetría en el directorio.")
                
    print("\n=======================================================\n")

if __name__ == "__main__":
    calculate_m4()