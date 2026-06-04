using UnityEngine;

public class SueloDetector : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }


    private void OnTriggerEnter(Collider other)
    {
        if (other.GetComponent<Producto>() != null && !other.GetComponent<Producto>().hasBeenSuelo)
        {
            Debug.Log("Can landed on the floor");
            other.GetComponent<Producto>().hasBeenSuelo = true;
            if (Tracker.Instance != null)
                Tracker.Instance.TrackEvent(new DunkCanEvent("can_landed", (CanType)other.GetComponent<Producto>().color(), TargetType.Floor));
        }
    }
}