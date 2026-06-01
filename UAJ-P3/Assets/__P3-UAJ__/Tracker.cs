using shortid;
using System;
using Unity.VisualScripting;
using UnityEngine;
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

    // evitar nullreferenceexceptions
    private bool isInitialized = false;

    private Tracker()
    {
        matchId = 0;
        options = new ShortIdOptions();
    }

    // inicializa sistema de telemetria
    public void Init()
    {
        if (isInitialized) 
            return;
        try
        {
            //pedimos un nuevo id de sesion
            sessionId = getNewSessionId();

            //conectamos
            ISerializer serializer = new JsonSerializer();
            persistence = new FilePersistence(serializer, sessionId);

            //inicializamos ids de partida
            matchId = 0;

            // como se ha inicializado, setteamos la variable a true
            isInitialized = true;

            //evento start
            //TrackEvent(new TrackerEvent("session_start", sessionId));
        }
        catch(System.Exception)
        {
            //Debug.LogError("Error initializing Tracker: " + e.Message);
        }
    }

    // m�todo para llamar desde el juego
    public void TrackEvent(TrackerEvent e)
    {
        Debug.Log("is Initialized " + isInitialized);

        if (!isInitialized || persistence == null) return;
        try
        {
            Debug.Log("tracker event created, sending to persistance");

            persistence.Send(e);

            if (e.eventType == "match_end")
                matchId++;
        }
        catch (System.Exception)
        {
            //Debug.LogError("Error tracking event: " + e.eventType + " - " + e.eventId + " - " + e.timestamp);
        }

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
        
        //evento fin

        // vaciamos y guardamos en archivo
        if (persistence != null)
        {
            persistence.Flush();
            persistence.Close();
        }
    } 
}