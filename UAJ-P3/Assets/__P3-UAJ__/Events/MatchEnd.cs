using System;

public class MatchEnd : TrackerEvent
{
    public MatchEnd(string session)
        : base("match_end", session)
    {
    }
}