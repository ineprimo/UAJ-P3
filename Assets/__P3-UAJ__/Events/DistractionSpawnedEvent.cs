using System;
using UnityEngine;

[Serializable]
public class DistractionSpawnedEvent : DistractionEvent
{
    public DistractionSpawnedEvent(string session, byte matchId, DistractionType type, GameObject obj)
        : base("distraction_spawned", session, matchId, type, obj, true) { }
}