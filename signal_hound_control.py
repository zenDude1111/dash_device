import time
import sqlite3
import random

def sweep():
    try:
        print("Performing sweep operation...")
        time.sleep(2)  # Simulate a time delay

        # Generate mock sweep data for frequencies 1-100 and amplitudes 0-100
        data = [random.randint(0, 100) for _ in range(100)]
        
        # Get current date and time as Unix Time (integer)
        current_unix_time = int(time.time())

        # Connect to the SQLite database
        with sqlite3.connect('signal_hound_data.db') as conn:
            cursor = conn.cursor()

            # Insert each frequency's data into the database
            for freq_idx, amp_mW in enumerate(data, start=1):
                frequency_MHz = freq_idx  # Example frequency value
                cursor.execute('''
                    INSERT INTO sweep_data (unix_time, frequency_MHz, amp_mW)
                    VALUES (?, ?, ?)
                ''', (current_unix_time, frequency_MHz, amp_mW))

        print("Sweep completed successfully.")

    except Exception as e:
        print(f"Error during sweep: {e}")
        raise e

if __name__ == "__main__":
    sweep()
