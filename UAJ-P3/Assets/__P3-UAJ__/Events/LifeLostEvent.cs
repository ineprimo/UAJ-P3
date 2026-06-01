using System;

[Serializable]
public class LifeLostEvent : TrackerEvent
{

    public LifeLostEvent(string session)
        : base("life_lost", session)
    {}
}