using System;
using UnityEngine;

[Serializable]
public class DistractionSpawnedEvent : DistractionEvent
{
    public DistractionSpawnedEvent(DistractionType type, int instanceId)
         : base("distraction_spawned", type, instanceId) { }
}