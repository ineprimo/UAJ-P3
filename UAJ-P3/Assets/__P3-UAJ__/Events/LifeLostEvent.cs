using System;

[Serializable]
public class LifeLostEvent : TrackerEvent
{

    public LifeLostEvent(string session, byte matchId)
        : base("life_lost", session, matchId)
    {}
}