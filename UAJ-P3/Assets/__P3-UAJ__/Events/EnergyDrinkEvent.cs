using UnityEngine;


public class EnergyDrinkEvent : TrackerEvent
{
    //public TargetType targetType; // destino

    public EnergyDrinkEvent(string session)
        : base("energy_drink_used", session)
    {
      //targetType = _targetType;
    }
}
