using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class FilePersistence : IPersistence
{
    private ISerializer serializer;
    private Queue<string> queue; //eventos
    private string filePath;

    public FilePersistence(ISerializer serializer, string sessionId)
    {
        this.serializer = serializer;
        this.queue = new Queue<string>();

        // Application.persistentDataPath --> aqui es donde unity guarda las cosas
        this.filePath = Path.Combine(Application.persistentDataPath, "telemetria_sesion_" + sessionId + ".json");

        Debug.Log("Archivo creado en: " + this.filePath); //para ver la ruta donde se ha creado
    }

    public void Send(TrackerEvent trackerEvent)
    {
        // Convertimos el evento en texto y lo a�adimos
        string data = serializer.Serialize(trackerEvent);
        queue.Enqueue(data);
    }

    public void Flush()
    {
        //Debug.Log("Eventos a escribir: " + queue.Count);
        if (queue.Count == 0) return;  // cola vac�a

        //Debug.Log("Escribiendo en: " + this.filePath);
        // Abrimos el archivo y mientras tengamos la cola con cosas las vamos a�adiendo
        using (StreamWriter writer = new StreamWriter(filePath, true))
        {
            while (queue.Count > 0)
            {
                //Debug.Log(queue.Peek());
                writer.WriteLine(queue.Dequeue());
            }
        }
    }
}