using UnityEngine;
using shortid;

public class Tracker : MonoBehaviour
{
    public static Tracker Instance;

    private IPersistence persistence;
    private string sessionId;
    //yo diria que tiene sentido llevar la cuenta de cuantas partidas se han jugado en el tracker, pero si veis que mejor que sea en otro lado cambiadlo
    private byte matchId;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    // inicializa sistema de telemetr�a
    public void Init()
    {
        //Los ids de sesion se pueden personalizar mucho, mirar el github de esta libreria (en uno de los documentos esta puesto el enlace tmb)
        //https://github.com/bolorundurowb/shortid

        //dado que no tenemos un servidor al que pedir que genere ids unicas, tenemos que generarlas en el propio ordenador,
        //usando un gran tama�o de ids y la posibilidad de usar numeros y caracteres especiales ademas de letras, 
        //las posibilidades de que se generen dos ids iguales en distintos ordenadores son muy bajas (aunque no nunca seran 0)
        ShortIdOptions options = new ShortIdOptions(useNumbers: true, useSpecialCharacters: true, length: 16);
        this.sessionId = ShortId.Generate(options);
        //this.sessionId = "1";
        
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

    // cuando el jugador cierre el juego
    void OnApplicationQuit()
    {
        //evento fin
        TrackEvent(new TrackerEvent("session_end", sessionId, matchId));

        // vaciamos y guardamos en archivo
        if (persistence != null)
        {
            persistence.Flush();
        }
    }
}