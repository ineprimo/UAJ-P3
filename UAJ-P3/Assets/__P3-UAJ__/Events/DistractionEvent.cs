using System;
using System.Collections.Generic;
using UnityEngine;

public enum DistractionType // no se si deberia ir aqui como lo de los destinos de las latas lol
{
    Cat,
    Fly,
    Light,
    Coworkers
}


public abstract class DistractionEvent : TrackerEvent
{
    public string distractionType;
    public int distractionId;

    public DistractionEvent(string type, string session, DistractionType distType, int instanceId)
         : base(type, session)
    {
        this.distractionType = distType.ToString();
        this.distractionId = instanceId;
    }
}