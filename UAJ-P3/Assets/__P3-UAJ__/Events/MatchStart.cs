using System;

public class MatchStart : TrackerEvent
{
    public MatchStart(string session)
        : base("match_start", session)
    {
    }
}