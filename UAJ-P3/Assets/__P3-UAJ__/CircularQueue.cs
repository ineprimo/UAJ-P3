using System;

// Cola circular que me he sacado de GeeksForGeeks adaptada para tipos genericos
class CircularQueue<T>
{
    // fixed-size array
    private T[] arr;   
    // index of front element
    private int front;    
    // current number of elements
    private int size;    
    // maximum capacity
    private int capacity;   
    
    public int Count => size;

    public CircularQueue(int cap) {
        capacity = cap;
        arr = new T[capacity];
        front = 0;
        size = 0;
    }

    // Insert an element at the rear
    public void Enqueue(T x) {
        if (size == capacity) {
            return;
        }
        int rear = (front + size) % capacity;
        arr[rear] = x;
        size++;
    }

    // Remove an element from the front
    public T Dequeue() {
        if (size == 0) {
            throw new InvalidOperationException("No se puede desencolar (Dequeue): La cola está vacía.");
        }
        T res = arr[front];
        front = (front + 1) % capacity;
        size--;
        return res;
    }

    // Get the front element
    public T GetFront() {
        if (size == 0) throw new InvalidOperationException("La cola está vacía.");;
        return arr[front];
    }

    // Get the rear element
    public T GetRear() {
        if (size == 0) throw new InvalidOperationException("La cola está vacía.");;
        int rear = (front + size - 1) % capacity;
        return arr[rear];
    }
}