using System;


public class TrackerEvent
{
    // Atributos comunes obligatorios
    public string eventType { get; set; } // Tipo identificador por ejemplo "LanzarLata"
    public long timestamp { get; set; } // Tiempo
    public string eventId { get; set; } // ID único de evento
    public string sessionId { get; set; } // ID de la sesión de juego
    public byte matchId { get; set; } // ID de la partida en la sesion

    // Constructor base
    public TrackerEvent(string type, string session, byte match)
    {
        this.eventType = type;
        this.sessionId = session;
        this.matchId = match;

        // Generamos el timestamp actual
        this.timestamp = ((DateTimeOffset)DateTime.UtcNow).ToUnixTimeMilliseconds();

        // Generamos un ID único para este evento
        this.eventId = Guid.NewGuid().ToString();
    }
}