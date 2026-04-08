using UnityEngine;

public class JsonSerializer : ISerializer
{
    public string Serialize(TrackerEvent trackerEvent)
    {
        // TOJson convierto los objetos en json
        return JsonUtility.ToJson(trackerEvent);
    }
}