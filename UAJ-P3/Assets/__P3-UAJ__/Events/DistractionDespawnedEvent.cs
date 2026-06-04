using System;
using UnityEngine;

[Serializable]
public class DistractionDespawnedEvent : DistractionEvent
{
    public DistractionDespawnedEvent(DistractionType type, int instanceId)
         : base("distraction_despawned", type, instanceId) { }
}