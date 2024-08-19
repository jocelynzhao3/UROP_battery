import csv
import pickle

# with open('example.csv', 'a', newline='') as file:
#         writer = csv.writer(file)

#         # Write header if needed
#         writer.writerow(['Name', 'Age', 'City'])


# for i in range(6):


#     with open('example.csv', 'a', newline='') as file:
#         writer = csv.writer(file)

#         # Write rows one by one
#         writer.writerow(['Alice', i, 'New York'])

# Path to the pickle file

for i in range(0, 5):
    file_path = f'mini_dataset/last_state_{i}.pkl'

    # Open the pickle file in binary read mode
    with open(file_path, 'rb') as file:
        # Load the object from the file
        last_state = pickle.load(file)  # solution object

    print(last_state['Local ECM resistance [Ohm]'].entries[-1])  # not very useful cause its all the same
    print(last_state["Gradient of positive electrode potential [V.m-1]"].entries[-1][-1])
    print(last_state["Gradient of separator electrolyte potential [V.m-1]"].entries[-1][-1])
    print(last_state["Gradient of negative electrolyte potential [V.m-1]"].entries[-1][-1])
