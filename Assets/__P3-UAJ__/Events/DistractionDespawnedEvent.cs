using UnityEngine;

public class DistractionDespawnedEvent : TrackerEvent
{
    public DistractionType distractionType; // tipo de distraccion
    public byte distractionId;              // el mismo ID de cuando aparecio?

    public DistractionDespawnedEvent(string session, byte matchId, DistractionType type, byte distId)
        : base("distraction_despawned", session, matchId)
    {
        distractionType = type;
        distractionId = distId;
    }
}
