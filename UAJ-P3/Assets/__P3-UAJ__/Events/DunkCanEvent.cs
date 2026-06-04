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
    public DunkCanEvent(string type, CanType _canType, TargetType _targetType) : base(type)
    {
        canType = _canType;
        targetType = _targetType;
    }
}
