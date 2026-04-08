using UnityEngine;


public class EnergyDrinkEvent : TrackerEvent
{  
    public TargetType targetType { get; set; } // destino

    public EnergyDrinkEvent(string session, byte matchId, TargetType _targetType)
        : base("energy_drink_used", session, matchId)
    {
      targetType = _targetType;
    }
}
