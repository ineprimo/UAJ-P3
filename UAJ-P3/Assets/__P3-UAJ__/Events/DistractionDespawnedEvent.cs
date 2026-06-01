using System;
using UnityEngine;

[Serializable]
public class DistractionDespawnedEvent : DistractionEvent
{
    public DistractionDespawnedEvent(string session, DistractionType type, GameObject obj)
        : base("distraction_despawned", session, type, obj, false) { }
}