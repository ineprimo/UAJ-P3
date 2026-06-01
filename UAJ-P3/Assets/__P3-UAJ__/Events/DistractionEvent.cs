using System;
using System.Collections.Generic;
using UnityEngine;

public enum DistractionType // no se si deberia ir aqui como lo de los destinos de las latas lol
{
    Cat,
    Fly,
    Light,
    Coworkers
}


public abstract class DistractionEvent : TrackerEvent
{
    private static Dictionary<GameObject, byte> _registry = new Dictionary<GameObject, byte>();
    private static byte _idCounter = 0;

    public string distractionType;
    public byte distractionId;

    public DistractionEvent(string type, string session, DistractionType distType, GameObject obj, bool isSpawn)
        : base(type, session)
    {
        this.distractionType = distType.ToString();

        if (isSpawn)
        {
            // Generamos nuevo ID y registramos el objeto
            _idCounter++;
            _registry[obj] = _idCounter;
            this.distractionId = _idCounter;
        }
        else
        {
            // Buscamos el ID que tenia este objeto y lo borramos del registro
            if (obj != null && _registry.TryGetValue(obj, out byte id))
            {
                this.distractionId = id;
                _registry.Remove(obj);
            }
            else
            {
                this.distractionId = 0; // ID por defecto si no se encuentra
            }
        }
    }
}