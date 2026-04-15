using shortid;

public class Tracker
{
    private static Tracker _instance = new Tracker();
    public static Tracker Instance { get
    {
        if (_instance == null)
        {
            _instance = new Tracker();
        }
        return _instance;
    } }

    private IPersistence persistence;
    private string sessionId;
    //yo diria que tiene sentido llevar la cuenta de cuantas partidas se han jugado en el tracker, pero si veis que mejor que sea en otro lado cambiadlo
    private byte matchId;
    private ShortIdOptions options;
    
    private Tracker()
    {
        matchId = 0;
        options = new ShortIdOptions();
    }

    // inicializa sistema de telemetr�a
    public void Init()
    {
        //pedimos un nuevo id de sesion
        sessionId = getNewSessionId();
        
        //conectamos
        ISerializer serializer = new JsonSerializer();
        persistence = new FilePersistence(serializer, sessionId);

        //inicializamos ids de partida
        matchId = 0;

        //evento start
        TrackEvent(new TrackerEvent("session_start", sessionId, matchId));
    }

    // m�todo para llamar desde el juego
    public void TrackEvent(TrackerEvent e)
    {
        //Debug.Log(e.eventType);
        if (persistence != null)
        {
            persistence.Send(e);
        }

        //quizas esta un poco feo actualizar en que partida estas de esta forma? Si se os ocurre algo mejor cambiadlo
        if (e.eventType == "match_end") 
            matchId++;
    }

    //cuando se quiera lanzar un evento se pide el id de sesion al tracker para rellenar la info del evento
    public string getSessionId() { return sessionId; }

    //cuando se quiera lanzar un evento se pide el id de partida al tracker para rellenar la info del evento
    public byte getMatchId() { return matchId; }
    
    //al iniciar la sesion generamos un id unico (si tuvieramos un servidor sustituiriamos la generacion del id por una request al servidor) 
    private string getNewSessionId()
    {
        //dado que no tenemos un servidor al que pedir que genere ids unicas, tenemos que generarlas en el propio ordenador,
        //usando un gran tama�o de ids y la posibilidad de usar numeros y caracteres especiales ademas de letras, 
        //las posibilidades de que se generen dos ids iguales en distintos ordenadores son muy bajas (aunque no nunca seran 0)
        return ShortId.Generate(options);
    }

    public void SetSessionOptions(TrackerConfigurator.SessionIDConfig op)
    {
        options = new ShortIdOptions(length: op.length, useNumbers: op.useNumbers, useSpecialCharacters: op.useSpecialCharacters, generateSequential: op.generateSequential);
    }
    
    // cuando el jugador cierre el juego
    public void TrackerQuit()
    {
        //Debug.Log("quitting");
        //evento fin
        TrackEvent(new TrackerEvent("session_end", sessionId, matchId));

        // vaciamos y guardamos en archivo
        if (persistence != null)
        {
            persistence.Flush();
        }
    } 
}