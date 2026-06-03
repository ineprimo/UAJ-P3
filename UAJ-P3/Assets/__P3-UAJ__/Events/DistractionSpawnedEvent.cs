using System;
using UnityEngine;

[Serializable]
public class DistractionSpawnedEvent : DistractionEvent
{
    public DistractionSpawnedEvent(string session, DistractionType type, int instanceId)
         : base("distraction_spawned", session, type, instanceId) { }
}