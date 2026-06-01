using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Destructor3000Rojo : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    private void OnTriggerEnter(Collider other)
    {
        Destroy(other);
        Debug.Log("Destrcutor");

        if (Tracker.Instance != null)
            Tracker.Instance.TrackEvent(new DunkCanEvent("can_landed", Tracker.Instance.getSessionId(), (CanType)other.GetComponent<Producto>().color(), TargetType.RedBin));
    }
}
