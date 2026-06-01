using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class FilePersistence : IPersistence
{
    private ISerializer serializer;
    private Queue<string> queue; //eventos
    private string filePath;

    private StreamWriter writer;

    private int maxQueueCapacity = 500;

    public FilePersistence(ISerializer serializer, string sessionId)
    {
        this.serializer = serializer;
        this.queue = new Queue<string>();

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

        // Convertimos el evento en texto y lo aniadimos
        string data = serializer.Serialize(trackerEvent);
        queue.Enqueue(data);
    }

    public void Flush()
    {
        Debug.Log("quitting " + queue.Count);

        if (queue.Count == 0 || writer == null) return;


        //Debug.Log("Escribiendo en: " + this.filePath);
        // Abrimos el archivo y mientras tengamos la cola con cosas las vamos a�adiendo
        try
        {
            while (queue.Count > 0)
            {
                Debug.Log("Escribiendo en: " + this.filePath);
                writer.WriteLine(queue.Dequeue());
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