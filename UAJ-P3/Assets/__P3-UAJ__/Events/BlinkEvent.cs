using System;

public class BlinkEvent : TrackerEvent
{
    // true si esta en la fase de parpadeo y false en el caso contrario 
    public bool blinkState;

    public BlinkEvent(bool state)
        : base("blink")
    {
        blinkState = state;
    }
}