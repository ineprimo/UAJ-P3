using UnityEngine;

public enum TargetType
{
    BlueBin,
    RedBin,
    Bin,
    Floor
}

public class DunkCanEvent : TrackerEvent
{
    public CanType canType { get; set; } // tipo de lata
    public TargetType targetType { get; set; } // destino
    public DunkCanEvent(string type, string session, byte matchId, CanType _canType, TargetType _targetType) : base(type, session, matchId)
    {
        canType = _canType;
        targetType = _targetType;
    }
}
