using System;

public class SessionStart : TrackerEvent
{
    public SessionStart(string session)
        : base("session_start", session)
    {
    }
}