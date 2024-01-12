import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def plot_sweep_data(db_file, frequency_to_plot):
    # Connect to the SQLite database
    with sqlite3.connect(db_file) as conn:
        # Read data into a pandas DataFrame
        query = f"SELECT * FROM sweep_data WHERE frequency_MHz = {frequency_to_plot}"
        df = pd.read_sql_query(query, conn)

    # Check if DataFrame is not empty
    if df.empty:
        print(f"No data found in the database for frequency {frequency_to_plot} MHz.")
        return

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['unix_time'], df['amp_mW'], label=f'Freq {frequency_to_plot} MHz')

    plt.xlabel('Unix Time')
    plt.ylabel('Amplitude (mW)')
    plt.title(f'Sweep Data Over Time for Frequency {frequency_to_plot} MHz')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    db_file = 'signal_hound_data.db'  # Path to your SQLite database
    frequency_to_plot = 1  # Set the frequency you want to plot
    plot_sweep_data(db_file, frequency_to_plot)
