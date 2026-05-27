import json
import os
import pandas as pd
import matplotlib.pyplot as plt


folder_path = os.path.dirname(os.path.abspath(__file__))


# gestiona el spawn de las distracciones
def distraction_spawned(event, distracciones, clave_partida, tiempos_reaccion, ts):
    tipo_dist = event.get("distractionType", "Desconocida")
    dist_id = event.get("distractionId")
    distracciones[clave_partida]["aparecidas"] += 1
    
    if tipo_dist not in distracciones[clave_partida]["tipos"]:
        distracciones[clave_partida]["tipos"][tipo_dist] = 0
    distracciones[clave_partida]["tipos"][tipo_dist] += 1
    
    distracciones[clave_partida]["lista"].append({
        "accion": "Aparece",
        "tipo": tipo_dist,
        "id": dist_id,
        "ts": ts
    })

    tiempos_reaccion.append({
        "clave_partida": clave_partida,
        "distractionId": event.get("distractionId"),
        "timestamp": ts,
        "type": "spawn"
    })

# gestiona el despawn de las distracciones
def distraction_despawned(event, distracciones, clave_partida, tiempos_reaccion, ts):
    distracciones[clave_partida]["quitadas"] += 1
    tipo_dist = event.get("distractionType", "Desconocida")
    dist_id = event.get("distractionId")
    distracciones[clave_partida]["lista"].append({
        "accion": "Desaparece",
        "tipo": tipo_dist,
        "id": dist_id,
        "ts": ts
    })

    tiempos_reaccion.append({
        "clave_partida": clave_partida,
        "distractionId": event.get("distractionId"),
        "timestamp": ts,
        "type": "despawn"
    })

# gestiona los parpadeos y bebidas
def drinks_blink(bebidas, clave_partida, parpadeos, ts):
    bebidas[clave_partida].append(ts)
    parpadeos[clave_partida]["ciclos"].append({
        "blinks": parpadeos[clave_partida]["blinks_actuales"],
        "fin_motivo": "Bebida Energética",
        "fin_ts": ts
    })
    parpadeos[clave_partida]["blinks_actuales"] = []

# gestiona cuando acaba la partida
def match_end(parpadeos, clave_partida, ts):
    if len(parpadeos[clave_partida]["blinks_actuales"]) > 0:
        parpadeos[clave_partida]["ciclos"].append({
            "blinks": parpadeos[clave_partida]["blinks_actuales"],
            "fin_motivo": "Fin de Partida",
            "fin_ts": ts
        })
        parpadeos[clave_partida]["blinks_actuales"] = []

# gestiona el tiempo de reaccion
def reaction_time(tiempos_reaccion, df_reaccion, resumen_m6):

    if not df_reaccion.empty and 'type' in df_reaccion.columns and 'timestamp' in df_reaccion.columns:
        spawn = df_reaccion[df_reaccion['type'] == 'spawn'][['clave_partida', 'distractionId', 'timestamp']]
        despawn = df_reaccion[df_reaccion['type'] == 'despawn'][['clave_partida', 'distractionId', 'timestamp']]
        
        if not spawn.empty and not despawn.empty:
            tabla_reaccion = pd.merge(spawn, despawn, on=['clave_partida', 'distractionId'], suffixes=('_start', '_end'))
            if not tabla_reaccion.empty:
                tabla_reaccion['segundos'] = (pd.to_numeric(tabla_reaccion['timestamp_end']) - pd.to_numeric(tabla_reaccion['timestamp_start'])) / 1000.0
                resumen_m6 = tabla_reaccion.groupby('clave_partida')['segundos'].mean().to_dict()


## metodos para escribir cada metrica
def print_M1(partida, latas):
    print(f"   [M1] Latas Generadas: {latas[partida]}\n")

def print_M2(partida, rendimiento):
    aciertos = rendimiento[partida]["aciertos"]
    fallos = rendimiento[partida]["fallos"]
    total_throws = aciertos + fallos
    if total_throws > 0:
        tasa = (aciertos / total_throws) * 100
        print(f"   [M2] Rendimiento: {tasa:.2f}% acierto ({aciertos} aciertos, {fallos} fallos)")
        print()
    else:
        print("   [M2] Rendimiento: 0 lanzamientos\n")

def print_M4_M5(partida, distracciones, t_inicio):
    ap = distracciones[partida]["aparecidas"]
    qu = distracciones[partida]["quitadas"]
    if ap > 0:
        pct = (qu / ap) * 100
        print(f"   [M4] Distracciones por tipo: {distracciones[partida]['tipos']}\n")
        print(f"   [M5] Distracciones resueltas: {pct:.2f}% ({qu}/{ap})\n")

        print("   [Distracciones]:")
        for d in distracciones[partida]["lista"]:
            t_transcurrido = (d["ts"] - t_inicio) / 1000.0
            mins = int(t_transcurrido / 60)
            secs = t_transcurrido % 60
            print(f"      - {d['accion']} {d['tipo']} (ID: {d['id']}) en el minuto {mins}:{secs:05.2f}")
            print()
    else:
        print("   [M4/M5] Sin distracciones en esta partida.\n")

def print_M6(partida, resumen_m6):
    if partida in resumen_m6:
        print(f"   [M6] Tiempo medio reacción: {resumen_m6[partida]:.2f} seg\n")
    else:
        print("   [M6] No se pudo calcular tiempo de reacción.\n")

def print_drinks_blinks(partida, parpadeos, bebidas, t_inicio):
    print(f"   [Fatiga] Bebidas Energéticas usadas: {len(bebidas[partida])}")
    ciclos_parpadeo = parpadeos[partida]["ciclos"]
    if len(ciclos_parpadeo) > 0:
        #t_inicio = parpadeos[partida]["inicio"]
        for num_ciclo, ciclo in enumerate(ciclos_parpadeo):
            total_blinks = len(ciclo["blinks"])
            motivo = ciclo["fin_motivo"]
            
            fin_transcurrido = (ciclo["fin_ts"] - t_inicio) / 1000.0
            mins_f = int(fin_transcurrido / 60)
            secs_f = fin_transcurrido % 60
            
            print(f"      > Ciclo {num_ciclo + 1} (Terminó por {motivo} en {mins_f}:{secs_f:05.2f})")
            if total_blinks == 0:
                print("         => 0 parpadeos antes de terminar el ciclo.")
            else:
                print(f"         => {total_blinks} parpadeos previos:")
                for i, blink_ts in enumerate(ciclo["blinks"]):
                    t_blink = (blink_ts - t_inicio) / 1000.0
                    mins_b = int(t_blink / 60)
                    secs_b = t_blink % 60
                    print(f"            - Parpadeo {i+1} en el minuto {mins_b}:{secs_b:05.2f}")
            print()
    else:
        print("      - No se registraron parpadeos ni uso de bebidas.\n")

def print_lifes(partida, vidas_perdidas, inicio_partida):
    total_vidas = len(vidas_perdidas[partida])
    print(f"   [Vidas] Total perdidas: {total_vidas}")
    if total_vidas > 0:
        t_inicio = inicio_partida.get(partida, 0)
        for i, ts_vida in enumerate(vidas_perdidas[partida]):
            t_transcurrido = (ts_vida - t_inicio) / 1000.0
            mins = int(t_transcurrido / 60)
            secs = t_transcurrido % 60
            print(f"      - Vida {i+1} perdida en el minuto {mins}:{secs:05.2f}\n")


# mapa de calor
def heatmap(session_clicks, filename):
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
        plt.title(f"Mapa de Calor de Clicks - Sesión {filename}")


def analizar_telemetria_completa():
    print("\n====================")
    print("ANÁLISIS DE TELEMETRÍA")
    print("====================")

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
            session_clicks = []
            inicio_partida = {}
            vidas_perdidas = {}

            # lectura eventos
            for event in events:
                if "matchId" in event and "sessionId" in event:
                    match_id = event["matchId"]
                    session_id = event["sessionId"]
                    clave_partida = f"Sesión {session_id} | Partida {match_id}\n"
                    
                    # DIccionarios en partida nueva
                    if clave_partida not in latas:
                        latas[clave_partida] = 0
                        rendimiento[clave_partida] = {"aciertos": 0, "fallos": 0}
                        distracciones[clave_partida] = {"tipos": {}, "aparecidas": 0, "quitadas": 0, "lista": []}
                        bebidas[clave_partida] = []
                        parpadeos[clave_partida] = {"inicio": 0, "ciclos": [], "blinks_actuales": []}
                        clicks_count[clave_partida] = 0
                        vidas_perdidas[clave_partida] = []
                    
                    t_event = event["eventType"]
                    ts = event["timestamp"]

                    if t_event == "match_start":
                        inicio_partida[clave_partida] = ts
                        parpadeos[clave_partida]["inicio"] = ts
                        parpadeos[clave_partida]["blinks_actuales"] = []

                    elif t_event == "match_end":
                        match_end(parpadeos, clave_partida, ts)
                    
                    elif t_event == "mouse_click":
                        clicks_count[clave_partida] += 1
                        session_clicks.append((event["x"], event["y"]))

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
                        distraction_spawned(event, distracciones, clave_partida, tiempos_reaccion, ts)

                    elif t_event == "distraction_despawned":
                        distraction_despawned(event, distracciones, clave_partida, tiempos_reaccion, ts)
                        
                    # Bebida y Parpadeos
                    elif t_event == "energy_drink_used":
                       drinks_blink(bebidas, clave_partida, parpadeos, ts)
                        
                    elif t_event == "blink" and event.get("blinkState") == True:
                        parpadeos[clave_partida]["blinks_actuales"].append(ts)

                    elif t_event == "life_lost":
                        vidas_perdidas[clave_partida].append(ts)


            # Calculo M6
            df_reaccion = pd.DataFrame(tiempos_reaccion)
            resumen_m6 = {}
            reaction_time(tiempos_reaccion, df_reaccion, resumen_m6)

            # finaliza el analisis
            print("\n====================")
            print(f"REPORTE DE ARCHIVO: {filename}")
            print("====================\n")

            
            for partida in latas.keys():

                if partida not in inicio_partida and latas[partida] == 0 and clicks_count[partida] == 0:
                    continue

                print(f" {partida.upper()}")
                t_inicio = inicio_partida.get(partida, 0)
                
                # M1
                print_M1(partida, latas)
                
                # M2
                print_M2(partida, rendimiento)
                
                # M4 y M5
                print_M4_M5(partida, distracciones, t_inicio)
                    
                # M6
                print_M6(partida, resumen_m6)

                # Bebidas y parpadeos
                print_drinks_blinks(partida, parpadeos, bebidas, t_inicio)

                #Vidas Perdidas
                print_lifes(partida, vidas_perdidas, inicio_partida)

                # Clicks
                print(f"   [Clicks] Total: {clicks_count[partida]}\n")
            
            # Mapa de calor de clicks
            heatmap(session_clicks, filename)
            
    plt.show()

    print("\n====================")
    print("ANÁLISIS COMPLETADO")
    print("====================")

if __name__ == "__main__":
    analizar_telemetria_completa()


