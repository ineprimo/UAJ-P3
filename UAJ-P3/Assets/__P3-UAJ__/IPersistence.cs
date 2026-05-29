public interface IPersistence
{
    // Recibe el evento para procesarlo
    void Send(TrackerEvent trackerEvent);

    // Llamada para el guardado/volcado de los datos
    void Flush();

    // Cierra el recurso utilizado
    void Close();
}