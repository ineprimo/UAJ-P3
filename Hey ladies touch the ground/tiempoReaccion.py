import pandas as pd
import json
import os

folder_path = os.path.dirname(os.path.abspath(__file__))

def calculate_m6():
    print("\n=======================================================")
    print("MÉTRICA 6: TIEMPO DE REACCIÓN MEDIO POR PARTIDA")
    
    for filename in os.listdir(folder_path):
        if filename.startswith("telemetria_sesion_") and filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            df = pd.read_json(file_path, lines=True)

            if 'distractionId' not in df.columns or 'distractionType' not in df.columns:
                print(f"\nArchivo: {filename}")
                print(" -> No se registraron distracciones en esta sesión.")
                continue
            
            # apariciones y desapariciones en una tabla
            spawn = df[df['eventType'] == 'distraction_spawned'][['matchId', 'distractionId', 'timestamp', 'distractionType']]
            despawn = df[df['eventType'] == 'distraction_despawned'][['distractionId', 'timestamp']]
            
            # crea una tabla con: matchId, distractionId, timestamp_spawn, timestamp_despawn
            tabla_reaccion = pd.merge(spawn, despawn, on='distractionId', suffixes=('_start', '_end'))
            
            if tabla_reaccion.empty:
                continue

            # tratar timestamps como ints antes de restar
            inicio = pd.to_numeric(tabla_reaccion['timestamp_start'])
            fin = pd.to_numeric(tabla_reaccion['timestamp_end'])

            # calculamos la diferencia y convertimos a segundos
            tabla_reaccion['delta_ms'] = fin - inicio
            tabla_reaccion['segundos'] = tabla_reaccion['delta_ms'] / 1000.0
            
            # agrupamos por partida para obtener la media
            resumen = tabla_reaccion.groupby('matchId')['segundos'].mean()
            
            print(f"\nArchivo: {filename}")
            for match_id, media in resumen.items():
                print(f" -> Partida {match_id}: {media:.2f} segundos de reacción media.")
                
    print("\n=======================================================\n")

if __name__ == "__main__":
    calculate_m6()