import json
import os

# Usamos la misma ruta para leer los archivos de la carpeta
folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_m5():
    print("\n=======================================================")
    print("\nMÉTRICA 5: PORCENTAJE DE DISTRACCIONES RESUELTAS\n")
    
    archivos_validos = 0
    
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding='utf-8') as f:
                events = [json.loads(line) for line in f]
            
            # { "Sesion X / Partida Y": {"aparecidas": 2, "quitadas": 1} }
            distracciones_por_partida = {}
            
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} / Partida {match_id}"
                    
                    if clave_partida not in distracciones_por_partida:
                        distracciones_por_partida[clave_partida] = {
                            "aparecidas": 0,
                            "quitadas": 0
                        }
                    
                    # aparece la distraccion, sumamos a aparecidas
                    if event["eventType"] == "distraction_spawned":
                        distracciones_por_partida[clave_partida]["aparecidas"] += 1
                        
                    # desaparece/quita la distracción, sumamos a quitadas
                    elif event["eventType"] == "distraction_despawned":
                        distracciones_por_partida[clave_partida]["quitadas"] += 1
            
            print(f"[{filename}]")
            for partida, conteos in distracciones_por_partida.items():
                aparecidas = conteos["aparecidas"]
                quitadas = conteos["quitadas"]
                
                if aparecidas == 0:
                    print(f" -> {partida}: No hubo distracciones.")
                else:
                    # calculamos el porcentaje
                    porcentaje = (quitadas / aparecidas) * 100
                    print(f" -> {partida}: {porcentaje:.2f}% resueltas ({quitadas} quitadas / {aparecidas} aparecidas)")
                    
            print("-------------------------------------------------------")
            
    if archivos_validos == 0:
        print("No se encontraron archivos de telemetría en el directorio.")
                
    print("\n=======================================================\n")

if __name__ == "__main__":
    calculate_m5()