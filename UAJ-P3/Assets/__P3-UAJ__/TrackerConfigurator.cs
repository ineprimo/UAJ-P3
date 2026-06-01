using System;
using Unity.VisualScripting;
using UnityEngine;

public class TrackerConfigurator : MonoBehaviour
{
    public static TrackerConfigurator Instance;
    private Tracker tracker;
    [SerializeField]
    private SessionIDConfig sessionIDConfig;
    
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
            tracker = Tracker.Instance;
            tracker.SetSessionOptions(sessionIDConfig);
            tracker.Init();
        }
        else
        {
            Destroy(gameObject);
        }
    }
    void OnApplicationQuit()
    {
        // se acaba la sesion
        if (Tracker.Instance != null)
            Tracker.Instance.TrackEvent(new SessionEnd(Tracker.Instance.getSessionId()));

        tracker.TrackerQuit();
    }

    [Serializable]
    public struct SessionIDConfig
    {
        [Tooltip("Longitud del id generado")]
        public int length;
        [Tooltip("Si el id debe utilizar números")]
        public bool useNumbers;
        [Tooltip("Si el id debe utilizar caracteres especiales")]
        public bool useSpecialCharacters;
        [Tooltip("Si los ids generados deben ser secuenciales")]
        public bool generateSequential;
    }
}
