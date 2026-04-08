using UnityEngine;


public enum DistractionType // no se si deberia ir aqui como lo de los destinos de las latas lol
{
    Cat,
    Fly,
    Light,
    Coworkers
}


public class DistractionSpawnedEvent : TrackerEvent
{
    public DistractionType distractionType; // tipo de distraccion
    public byte distractionId;              // ID único de esta distraccion

    public DistractionSpawnedEvent(string session, byte matchId, DistractionType type, byte distId)
        : base("distraction_spawned", session, matchId)
    {
        distractionType = type;
        distractionId = distId;
    }
}
