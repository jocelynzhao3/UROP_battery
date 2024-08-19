import pybamm
import numpy as np
import matplotlib.pyplot as plt

'''
look into sasha's paper about soc
try code based off online stuff - compare the two estimated SOCs
ask diego how he did soc
'''

model = pybamm.lithium_ion.DFN(
    {
        "SEI": "solvent-diffusion limited",
        "SEI porosity change": "true",
        "lithium plating": "partially reversible",
        "lithium plating porosity change": "true",  # alias for "SEI porosity change"
        "particle mechanics": ("swelling and cracking", "swelling only"),
        "SEI on cracks": "true",
        "loss of active material": "stress-driven", # "stress-driven",
        "calculate discharge energy": "true",  # for compatibility with older PyBaMM versions,
        "thermal": "lumped" # temp stuff
    }
)
param = pybamm.ParameterValues("OKane2022")

var_pts = {
    "x_n": 5,  # negative electrode
    "x_s": 5,  # separator
    "x_p": 5,  # positive electrode
    "r_n": 30,  # negative particle
    "r_p": 30,  # positive particle
}

experiment_2 = pybamm.Experiment(
    [
        (
            "Charge at 1C until 4.2V",
            "Hold at 4.2V until C/50",
            "Discharge at 1C until 3V",
            "Rest for 1 hour",
        )
    ] * 1
)


# print(param)
sim = pybamm.Simulation(model, experiment=experiment_2, parameter_values=param, var_pts=var_pts)  # 0.001 s
sol = sim.solve() # >6 s

Q = param['Nominal cell capacity [A.h]']
SoC_init = 1
discharge_cap = sol['Discharge capacity [A.h]'].entries[-1] # last entry
SoC = SoC_init - discharge_cap/Q  # seems linear?
# print(SoC)

# print(sol['Discharge capacity [A.h]'].entries)
# sim.plot(["X-averaged negative particle surface concentration", "Average negative particle concentration"])

max_x_av = max(sol["X-averaged negative particle surface concentration"].entries) # can compare entry vs max to SOC!
max_av = max(sol["Average negative particle concentration"].entries)


# print(len(sol['Discharge capacity [A.h]'].entries))
# print(len(sol["X-averaged negative particle surface concentration"].entries))
# print(len(sol["Average negative particle concentration"].entries))

x = []
soc_dis = []
soc_av_list = []
soc_x_list = []

for i in range(len(sol['Discharge capacity [A.h]'].entries)):
    discharge_cap = sol['Discharge capacity [A.h]'].entries[i] # last entry
    SoC = SoC_init - discharge_cap/Q  # seems linear?

    soc_x_av = sol["X-averaged negative particle surface concentration"].entries[i]/max_x_av
    soc_av = sol["Average negative particle concentration"].entries[i]/max_av

    a = np.array([SoC, soc_x_av, soc_av])
    # print(np.std(a), a)

    x.append(i)
    soc_dis.append(SoC)
    soc_av_list.append(soc_av)
    soc_x_list.append(soc_x_av)

    print(sol['Discharge energy [W.h]'].entries[i])  # could use the energy argument
    print(sol[ 'Throughput energy [W.h]'].entries[i])



# plt.plot(x, soc_dis, label='Discharge cap', marker='o')
# plt.plot(x, soc_av_list, label='avg neg particle', marker='s')
# plt.plot(x, soc_x_list, label='avg x particle', marker='^')

# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('SOC differences')
# plt.legend()

# plt.grid(True)
# plt.show()

'''
new soc = prev soc - energy expend (we calculate by step)

or

use discharge cap, x particle etc. (using pybamm) - try saving solution and retesting (sasha's code)

save LAST state only - .last state
ALSO save last discharge cap value
don't forget that nominal cell capacity decreases with degradation!
'''
