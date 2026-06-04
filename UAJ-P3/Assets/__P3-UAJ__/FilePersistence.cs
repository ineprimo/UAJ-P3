using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class FilePersistence : IPersistence
{
    private ISerializer serializer;
    private CircularQueue<TrackerEvent> queue; //eventos
    private string filePath;

    private StreamWriter writer;

    private int maxQueueCapacity = 500;

    public FilePersistence(ISerializer serializer, string sessionId)
    {
        this.serializer = serializer;
        this.queue = new CircularQueue<TrackerEvent>(maxQueueCapacity);

        // Application.persistentDataPath --> aqui es donde unity guarda las cosas
        this.filePath = Path.Combine(Application.persistentDataPath, "telemetria_sesion_" + sessionId + ".json");

        try
        {
            // Mantenemos el writer ABIERTO durante toda la sesion
            writer = new StreamWriter(this.filePath, true);
            Debug.Log("Archivo creado en: " + this.filePath); //para ver la ruta donde se ha creado
        }
        catch (IOException e)
        {
            Debug.LogError($"[FilePersistence] Error de IO al crear archivo: {e.Message}");
        }
        
    }

    public void Send(TrackerEvent trackerEvent)
    {
        if (queue.Count >= maxQueueCapacity)
        {
            queue.Dequeue();
            Debug.LogWarning("[FilePersistence] Cola llena. Descartando evento antiguo.");
        }

        // lo dejamos sin serializar
        queue.Enqueue(trackerEvent);
    }

    public void Flush()
    {
        if (queue.Count == 0 || writer == null) return;

        // Abrimos el archivo y mientras tengamos la cola con cosas las vamos a�adiendo
        try
        {
            while (queue.Count > 0)
            {
                //Debug.Log("Escribiendo en: " + this.filePath);

                // serializamos los datos
                string data = serializer.Serialize(queue.Dequeue());
                
                // escribimos los datos
                writer.WriteLine(data);
            }
            writer.Flush();
        }
        catch (IOException ex)
        {
            Debug.LogError($"[FilePersistence] Error al escribir (Flush): {ex.Message}");
        }
    }

    public void Close()
    {
        if (writer != null)
        {
            try
            {
                writer.Close();
                writer.Dispose();
            }
            catch (IOException ex)
            {
                Debug.LogError($"[FilePersistence] Error al cerrar archivo: {ex.Message}");
            }
        }
    }
}