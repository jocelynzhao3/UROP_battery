import matplotlib.pyplot as plt

# Example data
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# # Plot with specified color
# plt.plot(x, y, color='red')  # Specifying color by name
# # or plt.plot(x, y, color='#FF5733')  # Specifying color by hexadecimal code
# # or plt.plot(x, y, color=(0.1, 0.2, 0.5))  # Specifying color by RGB tuple
# # or plt.plot(x, y, color='0.75')  # Specifying color by grayscale intensity

# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Line plot with specified color')
# plt.grid(True)
# plt.show()

# import numpy as np

# x = [i for i in np.arange(10)]
# print(x)

# x = [1, 2, 3, 4, 5, 6]
# y = [5-item for item in x]
# print(y)


import pybamm

param = pybamm.ParameterValues("OKane2022")
for i, v in param.items():
    print(i, v)

# print(param["Positive electrode Paris' law constant b"]) # multiply this one?
# print(param["Positive electrode Paris' law constant m"])

a = 2

print(f'hi {a}')
