using System;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Experimental.GlobalIllumination;

public class LightController : MonoBehaviour
{
    [SerializeField] private Light _light;
    public Animator palancaAnimator;

    private byte _myDistractionId;

    private void Start()
    {
        GetComponent<MeshCollider>().enabled = false;
    }
    public void TurnOn()
    {
        _light.intensity = 3.57f;
        palancaAnimator.SetTrigger("Trigger");
        GetComponent<MeshCollider>().enabled = false;
        if (Tracker.Instance != null)
        {
            Tracker.Instance.TrackEvent(new DistractionDespawnedEvent(Tracker.Instance.getSessionId(), Tracker.Instance.getMatchId(), DistractionType.Light, gameObject));
        }

    }

    public void TurnOff()
    {
        _light.intensity = 0.1f;
        palancaAnimator.SetTrigger("Trigger");
        GetComponent<MeshCollider>().enabled = true;

        if (Tracker.Instance != null)
        {
            Tracker.Instance.TrackEvent(new DistractionSpawnedEvent(Tracker.Instance.getSessionId(), Tracker.Instance.getMatchId(), DistractionType.Light, gameObject));
        }
    }
}
