using System;
using System.Numerics;


public class ClickEvent : TrackerEvent
{
    
    public Vector2 position { get; set; } // Tiempo

    public ClickEvent(string type, string session, byte matchId, Vector2 p) : base(type, session, matchId)
    {
        position = p;
    }
}
