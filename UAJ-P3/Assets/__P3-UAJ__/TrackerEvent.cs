using System;

[Serializable]
public class TrackerEvent
{
    // Atributos comunes obligatorios
    public string eventType; // Tipo identificador por ejemplo "LanzarLata"
    public long timestamp; // Tiempo
    public string eventId; // ID �nico de evento
    public string sessionId; // ID de la sesi�n de juego

    // Constructor base
    public TrackerEvent(string type)
    {
        this.eventType = type;
        this.sessionId = null;

        // Generamos el timestamp actual
        this.timestamp = ((DateTimeOffset)DateTime.UtcNow).ToUnixTimeMilliseconds();

        // Generamos un ID �nico para este evento
        this.eventId = Guid.NewGuid().ToString();
    }
}