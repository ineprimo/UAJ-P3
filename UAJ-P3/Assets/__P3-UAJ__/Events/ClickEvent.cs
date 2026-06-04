using System;
using System.Numerics;


public class ClickEvent : TrackerEvent
{

    public float x;
    public float y;
    
    public ClickEvent(string type, Vector2 p) : base(type)
    {
        x = p.X;
        y = p.Y;
    }
}
