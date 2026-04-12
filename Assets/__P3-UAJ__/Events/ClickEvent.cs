using System;
using System.Numerics;


public class ClickEvent : TrackerEvent
{

    public float x;
    public float y;
    
    public ClickEvent(string type, string session, byte matchId, Vector2 p) : base(type, session, matchId)
    {
        x = p.X;
        y = p.Y;
    }
}
