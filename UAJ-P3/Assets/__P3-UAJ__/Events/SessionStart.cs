using System;

public class SessionStart : TrackerEvent
{
    // true si esta en la fase de parpadeo y false en el caso contrario 
    public bool blinkState;

    public SessionStart(string session)
        : base("session_start", session)
    {
    }
}