import json
import os

folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_blinks():
    print("\n=======================================================")
    print("\nANÁLISIS DE PARPADEOS\n")
    
    archivos_validos = 0
    
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding='utf-8') as f:
                events = [json.loads(line) for line in f]
            
            estado_partidas = {} 
            
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    clave_partida = f"Sesión {event['sessionId']} / Partida {event['matchId']}"
                    
                    if clave_partida not in estado_partidas:
                        estado_partidas[clave_partida] = {
                            "inicio": 0,
                            "ciclos": [],
                            "blinks_actuales": [] #Guardamos los blinks hasta que beba
                        }
                    
                    #Guardamos el tiempo de inicio
                    if event["eventType"] == "match_start":
                        estado_partidas[clave_partida]["inicio"] = event["timestamp"]
                        estado_partidas[clave_partida]["blinks_actuales"] = []
                    
                    #Detectamos parpadeo
                    elif event["eventType"] == "blink" and event.get("blinkState") == True:
                        estado_partidas[clave_partida]["blinks_actuales"].append(event["timestamp"])
                    
                    #Detectamos bebida energetica
                    elif event["eventType"] == "energy_drink_used":
                        estado_partidas[clave_partida]["ciclos"].append({
                            "blinks": estado_partidas[clave_partida]["blinks_actuales"],
                            "fin_motivo": "Bebida Energética",
                            "fin_ts": event["timestamp"]
                        })
                 
                        estado_partidas[clave_partida]["blinks_actuales"] = []
                        
                    #Si la partida termina y sigue en estado de parpadeo
                    elif event["eventType"] == "match_end":
                        if len(estado_partidas[clave_partida]["blinks_actuales"]) > 0:
                            estado_partidas[clave_partida]["ciclos"].append({
                                "blinks": estado_partidas[clave_partida]["blinks_actuales"],
                                "fin_motivo": "Fin de Partida (Murió/Acabó sin beber)",
                                "fin_ts": event["timestamp"]
                            })
                            estado_partidas[clave_partida]["blinks_actuales"] = []

            print(f"[{filename}]")
            for partida, datos in estado_partidas.items():
                print(f" -> {partida}:")
                tiempo_inicio = datos["inicio"]
                
                if len(datos["ciclos"]) == 0:
                    print("      - No hubo parpadeos ni bebidas en esta partida.")
                    continue
                
                ciclo_num = 1
                for ciclo in datos["ciclos"]:
                    total_blinks = len(ciclo["blinks"])
                    motivo_fin = ciclo["fin_motivo"]
                    
                    print(f"    [Ciclo {ciclo_num} - Terminó por: {motivo_fin}]")
                    
                    # Imprimimos cada blink de ese ciclo
                    for i, blink_ts in enumerate(ciclo["blinks"]):
                        tiempo_transcurrido = (blink_ts - tiempo_inicio) / 1000
                        mins, secs = int(tiempo_transcurrido / 60), tiempo_transcurrido % 60
                        print(f"      - Parpadeo {i+1}: minuto {mins}:{secs:05.2f}")
                    
                    fin_transcurrido = (ciclo["fin_ts"] - tiempo_inicio) / 1000
                    mins_fin, secs_fin = int(fin_transcurrido / 60), fin_transcurrido % 60
                    
                    if total_blinks == 0:
                         print(f"      => Se tomó bebida en {mins_fin}:{secs_fin:05.2f} SIN haber parpadeado previamente.\n")
                    else:
                         print(f"      => Resultado: Hizo {total_blinks} parpadeos hasta '{motivo_fin}' en el minuto {mins_fin}:{secs_fin:05.2f}\n")
                    
                    ciclo_num += 1
                    
            print("-------------------------------------------------------")
            


if __name__ == "__main__":
    calculate_blinks()