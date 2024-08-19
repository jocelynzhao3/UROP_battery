'''
Basic battery capacity measurement: Capacity (mAh) = Rated Current (mA) * Usage Time (hours)
Use: Open-circuit voltage at 0% SOC [V]': 2.5, Open-circuit voltage at 100% SOC [V]': 4.2
(Lower voltage cutoff and upper voltage cutoff do the same thing)

More accurate capacity measurement: Capacity (Wh) = Current(A) * Voltage(V) * Time (hours)
In short: Capacity (Wh) = Power (Watts) * Time (Hours)
Li-ion can assume stable voltage while discharging??

Can try plotting power, terminal power, etc.
Useful resource: https://www.youtube.com/watch?v=2SrfbpVnXwI

To age a battery, try 'termination' step in experiments until 80% capacity
Learn to use 'starting solution'
'''

import pybamm
import numpy as np
import matplotlib.pyplot as plt
import time

a = time.time()

pybamm.set_logging_level("NOTICE")

params = pybamm.ParameterValues('OKane2022')
# params.update({"SEI kinetic rate constant [m.s-1]": 1e-14})
spm = pybamm.lithium_ion.DFN({"SEI": "ec reaction limited"})

exp = pybamm.Experiment([
    ("Charge at 1C until 4.2V",
     "Hold at 4.2V until C/50",
     "Discharge at 1C until 3V",
     "Rest for 1 hour")
] * 10000,
termination="80% capacity")
sim = pybamm.Simulation(spm, experiment=exp, parameter_values=params)
sol= sim.solve()

b = time.time()
print(f'run time in sec: {b-a}' )

for i in sol.summary_variables.keys():
    print(i)

x = np.arange(len(sol.summary_variables["Capacity [A.h]"]))
y = sol.summary_variables["Capacity [A.h]"]
plt.plot(x, y, color='red')
plt.xlabel('cycle')
plt.ylabel('capacity in A.h')
plt.title('Battery degradation with DFN')
plt.show()
