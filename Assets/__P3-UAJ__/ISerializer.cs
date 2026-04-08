public interface ISerializer
{
    // Transforma el evento a datos en un formato concreto
    string Serialize(TrackerEvent trackerEvent);
}