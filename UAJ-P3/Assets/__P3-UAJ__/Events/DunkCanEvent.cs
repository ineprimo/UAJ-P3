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
    public CanType canType; // tipo de lata
    public TargetType targetType; // destino
    public DunkCanEvent(string type, string session, CanType _canType, TargetType _targetType) : base(type, session)
    {
        canType = _canType;
        targetType = _targetType;
    }
}
