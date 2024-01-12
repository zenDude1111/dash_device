import random
import time

def sweep():
    try:
        # Simulating a sweep operation with a random chance of failure
        print("Performing sweep operation...")
        time.sleep(2)  # Simulating a delay for the sweep operation

        if random.random() < 0.1:  # 10% chance to simulate an error
            raise Exception("Signal Hound device not responding")

        # Simulate successful sweep data
        sweep_data = [random.uniform(-100, 0) for _ in range(10)]  # Example sweep data
        print("Sweep successful:", sweep_data)
        return "Success", None
    except Exception as e:
        # Return the error message if an exception occurs
        return "Error", str(e)

if __name__ == "__main__":
    # For testing the sweep function directly
    status, error = sweep()
    if status == "Error":
        print(f"Error occurred during sweep: {error}")
    else:
        print("Sweep operation completed successfully")
