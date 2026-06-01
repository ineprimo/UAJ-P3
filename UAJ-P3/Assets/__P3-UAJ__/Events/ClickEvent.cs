using System;
using System.Numerics;


public class ClickEvent : TrackerEvent
{

    public float x;
    public float y;
    
    public ClickEvent(string type, string session, Vector2 p) : base(type, session)
    {
        x = p.X;
        y = p.Y;
    }
}
