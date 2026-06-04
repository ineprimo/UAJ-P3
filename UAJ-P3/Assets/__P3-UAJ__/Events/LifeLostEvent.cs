using System;

[Serializable]
public class LifeLostEvent : TrackerEvent
{

    public LifeLostEvent()
        : base("life_lost")
    {}
}