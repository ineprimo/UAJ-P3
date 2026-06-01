using System;

public class SessionEnd : TrackerEvent
{
    public SessionEnd(string session)
        : base("session_end", session)
    {
    }
}