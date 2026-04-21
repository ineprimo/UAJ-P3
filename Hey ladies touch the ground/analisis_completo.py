import json
import os
import pandas as pd

folder_path = os.path.dirname(os.path.abspath(__file__))

def analizar_telemetria_completa():
    print("\n====================")
    print("ANÁLISIS DE TELEMETRÍA")
    print("\n====================")

    archivos_validos = 0

    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            archivos_validos += 1
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding='utf-8') as f:
                events = [json.loads(line) for line in f]
            
            latas = {}                  # M1
            rendimiento = {}            # M2
            distracciones = {}          # M4 y M5
            tiempos_reaccion = []       # M6
            bebidas = {}
            parpadeos = {}
            clicks_count = {}
            inicio_partida = {}

            # lectura eventos
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} | Partida {match_id}"
                    
                    # DIccionarios en partida nueva
                    if clave_partida not in latas:
                        latas[clave_partida] = 0
                        rendimiento[clave_partida] = {"aciertos": 0, "fallos": 0}
                        distracciones[clave_partida] = {"tipos": {}, "aparecidas": 0, "quitadas": 0}
                        bebidas[clave_partida] = []
                        parpadeos[clave_partida] = {"inicio": 0, "ciclos": [], "blinks_actuales": []}
                        clicks_count[clave_partida] = 0
                    
                    t_event = event["eventType"]
                    ts = event["timestamp"]

                    if t_event == "match_start":
                        inicio_partida[clave_partida] = ts
                        parpadeos[clave_partida]["inicio"] = ts
                        parpadeos[clave_partida]["blinks_actuales"] = []

                    elif t_event == "match_end":
                        if len(parpadeos[clave_partida]["blinks_actuales"]) > 0:
                            parpadeos[clave_partida]["ciclos"].append({
                                "blinks": parpadeos[clave_partida]["blinks_actuales"],
                                "fin_motivo": "Fin de Partida",
                                "fin_ts": ts
                            })
                            parpadeos[clave_partida]["blinks_actuales"] = []
                    
                    elif t_event == "mouse_click":
                        clicks_count[clave_partida] += 1

                    # M1: Latas Generadas
                    elif t_event == "can_appears":
                        latas[clave_partida] += 1
                        
                    # M2: Rendimiento
                    elif t_event == "can_landed":
                        if event.get("canType") == event.get("targetType"):
                            rendimiento[clave_partida]["aciertos"] += 1
                        else:
                            rendimiento[clave_partida]["fallos"] += 1
                            
                    # M4 + M5 + M6: Distracciones
                    elif t_event == "distraction_spawned":
                        tipo_dist = event.get("distractionType", "Desconocida")
                        distracciones[clave_partida]["aparecidas"] += 1
                        
                        if tipo_dist not in distracciones[clave_partida]["tipos"]:
                            distracciones[clave_partida]["tipos"][tipo_dist] = 0
                        distracciones[clave_partida]["tipos"][tipo_dist] += 1
                        
                        tiempos_reaccion.append({
                            "clave_partida": clave_partida,
                            "distractionId": event.get("distractionId"),
                            "timestamp": ts,
                            "type": "spawn"
                        })
                        
                    elif t_event == "distraction_despawned":
                        distracciones[clave_partida]["quitadas"] += 1
                        tiempos_reaccion.append({
                            "clave_partida": clave_partida,
                            "distractionId": event.get("distractionId"),
                            "timestamp": ts,
                            "type": "despawn"
                        })
                        
                    # Bebida y Parpadeos
                    elif t_event == "energy_drink_used":
                        bebidas[clave_partida].append(ts)
                        parpadeos[clave_partida]["ciclos"].append({
                            "blinks": parpadeos[clave_partida]["blinks_actuales"],
                            "fin_motivo": "Bebida Energética",
                            "fin_ts": ts
                        })
                        parpadeos[clave_partida]["blinks_actuales"] = []
                        
                    elif t_event == "blink" and event.get("blinkState") == True:
                        parpadeos[clave_partida]["blinks_actuales"].append(ts)


            # Calculo M6
            df_reaccion = pd.DataFrame(tiempos_reaccion)
            resumen_m6 = {}
            
            if not df_reaccion.empty and 'type' in df_reaccion.columns and 'timestamp' in df_reaccion.columns:
                spawn = df_reaccion[df_reaccion['type'] == 'spawn'][['clave_partida', 'distractionId', 'timestamp']]
                despawn = df_reaccion[df_reaccion['type'] == 'despawn'][['clave_partida', 'distractionId', 'timestamp']]
                
                if not spawn.empty and not despawn.empty:
                    tabla_reaccion = pd.merge(spawn, despawn, on=['clave_partida', 'distractionId'], suffixes=('_start', '_end'))
                    if not tabla_reaccion.empty:
                        tabla_reaccion['segundos'] = (pd.to_numeric(tabla_reaccion['timestamp_end']) - pd.to_numeric(tabla_reaccion['timestamp_start'])) / 1000.0
                        resumen_m6 = tabla_reaccion.groupby('clave_partida')['segundos'].mean().to_dict()

            print(f"REPORTE DE ARCHIVO: {filename}")
            print("\n====================")

            
            for partida in latas.keys():
                print(f" {partida.upper()}")
                
                # M1
                print(f"   [M1] Latas Generadas: {latas[partida]}")
                
                # M2
                aciertos = rendimiento[partida]["aciertos"]
                fallos = rendimiento[partida]["fallos"]
                total_throws = aciertos + fallos
                if total_throws > 0:
                    tasa = (aciertos / total_throws) * 100
                    print(f"   [M2] Rendimiento: {tasa:.2f}% acierto ({aciertos} aciertos, {fallos} fallos)")
                else:
                    print("   [M2] Rendimiento: 0 lanzamientos")
                
                # M4 y M5
                ap = distracciones[partida]["aparecidas"]
                qu = distracciones[partida]["quitadas"]
                if ap > 0:
                    pct = (qu / ap) * 100
                    print(f"   [M4] Distracciones por tipo: {distracciones[partida]['tipos']}")
                    print(f"   [M5] Distracciones resueltas: {pct:.2f}% ({qu}/{ap})")
                else:
                    print("   [M4/M5] Sin distracciones en esta partida.")
                    
                # M6
                if partida in resumen_m6:
                    print(f"   [M6] Tiempo medio reacción: {resumen_m6[partida]:.2f} seg")
                else:
                    print("   [M6] No se pudo calcular tiempo de reacción.")

                # Bebidas
                print(f"   [Bebidas] Usadas: {len(bebidas[partida])}")
                
                # Clicks
                print(f"   [Clicks] Total: {clicks_count[partida]}")
                print("\n")

    print("\n====================")
    print("ANÁLISIS COMPLETADO")
    print("\n====================")

if __name__ == "__main__":
    analizar_telemetria_completa()