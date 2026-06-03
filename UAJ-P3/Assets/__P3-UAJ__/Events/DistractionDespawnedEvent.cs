using System;
using UnityEngine;

[Serializable]
public class DistractionDespawnedEvent : DistractionEvent
{
    public DistractionDespawnedEvent(string session, DistractionType type, int instanceId)
         : base("distraction_despawned", session, type, instanceId) { }
}