using System;
using UnityEngine;

[Serializable]
public class DistractionDespawnedEvent : DistractionEvent
{
    public DistractionDespawnedEvent(string session, byte matchId, DistractionType type, GameObject obj)
        : base("distraction_despawned", session, matchId, type, obj, false) { }
}