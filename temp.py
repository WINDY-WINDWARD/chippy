import threading
import time

# Shared data structure to communicate between threads
shared_data = {"message": None}

# Condition variable for synchronization
condition = threading.Condition()

def thread1_func():
    global shared_data
    # Simulate some work in Thread 1
    time.sleep(2)
    
    # Acquire the condition lock
    with condition:
        # Set a message in the shared data
        shared_data["message"] = "Hello from Thread 1"
        
        # Notify Thread 2 that the message is ready
        condition.notify()

    # Continue with the rest of Thread 1's tasks
    print("Thread 1 is doing its work")

def thread2_func():
    global shared_data
    # Acquire the condition lock
    with condition:
        # Wait for the message from Thread 1
        while shared_data["message"] is None:
            condition.wait()
        
        # Process the message from Thread 1
        message = shared_data["message"]
        print(f"Thread 2 received message: {message}")

def thread3_func():
    global shared_data
    # Monitor and log activities of other threads
    x = 0
    while x<20:
        print("Thread 3 is monitoring...")
        time.sleep(1)
        x+=1

# Create threads
thread1 = threading.Thread(target=thread1_func)
thread2 = threading.Thread(target=thread2_func)
thread3 = threading.Thread(target=thread3_func)

# Start threads
thread1.start()
thread2.start()
thread3.start()

# Wait for all threads to finish
thread1.join()
thread2.join()

# Wait for thread 3 to finish

thread3.join()


