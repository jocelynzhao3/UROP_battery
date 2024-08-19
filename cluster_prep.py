import csv
import pandas as pd
import pickle
import time

a = time.time()

# CSV is being APPENDED, make sure to clear it before adding new/more data
with open('cluster_data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'discharge_cap', 'capacity', 'resistance', 'gradient_positive', 'gradient_separator', 'gradient_negative'])

    df = pd.read_csv('mini_dataset/master.csv')

    for index, row in df.iterrows():

        crack_multipler = 12 + (index-25)/5
        name = f'crack={crack_multipler};100_cycles'
        discharge_cap = row['Discharge Cap']
        capacity = row['Capacity']

        # Path to the pickle file
        file_path = f'mini_dataset/last_state_{index}.pkl'

        # Open the pickle file in binary read mode
        with open(file_path, 'rb') as file:
            # Load the object from the file
            last_state = pickle.load(file)  # solution object

        # what vars do we want from the last state?
        # voltage, energy, resistance, capacitance, gradient, volatility
        # just knowing the ending voltage is not very helpful - you'd need the voltage curve

        resistance = last_state['Local ECM resistance [Ohm]'].entries[-1]
        gradient_positive = last_state["Gradient of positive electrode potential [V.m-1]"].entries[-1][-1]
        gradient_separator = last_state["Gradient of separator electrolyte potential [V.m-1]"].entries[-1][-1]
        gradient_negative = last_state["Gradient of negative electrolyte potential [V.m-1]"].entries[-1][-1]

        # # Write rows one by one
        writer.writerow([name, discharge_cap, capacity, resistance, gradient_positive, gradient_separator, gradient_negative])

b = time.time()

print(f'done in {b-a} seconds')
# runs into missing file error at end, should be fine

'''
In cluster_data.csv, I deleted the last few rows where 'porosity at the negative electrode–separator interface reaches zero'
This causes battery to behave unexpectedly, hence the sudden change in numbers
'''
