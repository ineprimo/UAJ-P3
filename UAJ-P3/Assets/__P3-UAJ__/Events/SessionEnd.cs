using System;

public class SessionEnd : TrackerEvent
{
    // true si esta en la fase de parpadeo y false en el caso contrario 
    public bool blinkState;

    public SessionEnd(string session, bool state)
        : base("sessionEnd", session)
    {
    }
}