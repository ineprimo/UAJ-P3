using System;
using UnityEngine;

[Serializable]
public class DistractionSpawnedEvent : DistractionEvent
{
    public DistractionSpawnedEvent(string session, DistractionType type, GameObject obj)
        : base("distraction_spawned", session, type, obj, true) { }
}