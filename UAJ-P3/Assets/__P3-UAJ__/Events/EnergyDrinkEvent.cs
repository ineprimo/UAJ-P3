using UnityEngine;


public class EnergyDrinkEvent : TrackerEvent
{
    //public TargetType targetType; // destino

    public EnergyDrinkEvent(string session, byte matchId)
        : base("energy_drink_used", session, matchId)
    {
      //targetType = _targetType;
    }
}
