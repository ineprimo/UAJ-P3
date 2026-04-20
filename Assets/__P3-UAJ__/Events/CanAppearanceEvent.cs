using UnityEngine;

// no se donde poner esto tbh
public enum CanType
{
    Blue,
    Red,
    Other
}

public class CanAppearanceEvent : TrackerEvent
{
    public CanType canType; // tipo de lata
    public CanAppearanceEvent(string type, string session, byte matchId, CanType _canType) : base(type, session, matchId)
    {
        canType = _canType;

    }
}
