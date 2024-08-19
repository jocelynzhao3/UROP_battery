import pybamm
import matplotlib.pyplot as plt
import time
import numpy as np
import csv

# https://github.com/pybamm-team/PyBaMM/blob/d5ca92be199ee31d31238a882cb79f6ae7cddccd/docs/source/examples/notebooks/models/coupled-degradation.ipynb

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
        # "thermal": "lumped" # temp stuff
    }
)

param = pybamm.ParameterValues("OKane2022")
# for i, v in param.items():
#     print(i, v)

var_pts = {
    "x_n": 5,  # negative electrode
    "x_s": 5,  # separator
    "x_p": 5,  # positive electrode
    "r_n": 30,  # negative particle
    "r_p": 30,  # positive particle
}

# for i, v in param.items():
#     print(i, v)
# param['Negative electrode reaction-driven LAM factor [m3.mol-1]'] = 0.001  # multiplier?
# print(param["Positive electrode Paris' law constant b"]) # only negative electrode cracks rn
# print(param["Positive electrode Paris' law constant m"]) # Paris law alters cracking rate

# print(param["Negative electrode Paris' law constant b"]) # 1.12, multipler?
# print(param["Negative electrode Paris' law constant m"]) # 2.2, exponential?

with open('mini_dataset/master.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    # Write header if needed
    writer.writerow(['Iteration', 'Discharge Cap', 'Capacity'])

a = time.time()

for i in range(0, 51):

    crack_multipler = 12 + (i-25)/5

    param["Negative electrode Paris' law constant b"] = 1.12*crack_multipler # scale by 30?

    # var_pts = { # slight graph difference
    #     "x_n": 20,  # negative electrode
    #     "x_s": 20,  # separator
    #     "x_p": 20,  # positive electrode
    #     "r_n": 30,  # negative particle
    #     "r_p": 30,  # positive particle
    # }

    cycle_number = 100  # original used 1000 cycles - run these longer one overnight
    exp = pybamm.Experiment(
        [
            ("Hold at 4.2 V until C/100 (5 minute period)",
            "Rest for 4 hours (5 minute period)",
            "Discharge at 0.1C until 2.5 V (5 minute period)",  # initial capacity check
            "Charge at 0.3C until 4.2 V (5 minute period)",
            "Hold at 4.2 V until C/100 (5 minute period)",)
        ]
        + [
            (
                "Discharge at 1C until 2.5 V",  # ageing cycles
                "Charge at 0.3C until 4.2 V (5 minute period)",
                "Hold at 4.2 V until C/100 (5 minute period)",
            )
        ]
        * cycle_number
        + [("Discharge at 0.1C until 2.5 V (5 minute period)")],  # final capacity check
    )
    sim = pybamm.Simulation(model, parameter_values=param, experiment=exp, var_pts=var_pts)
    sol = sim.solve()

    SoC_init = 1

    discharge_cap = sol['Discharge capacity [A.h]'].entries[-1] # last entry
    capacity = sol.summary_variables["Capacity [A.h]"][-1]
    # SoC = SoC_init - discharge_cap/capacity  # seems linear?

    # sim.solution.cycles[0].plot(['Terminal voltage [V]'])
    # sim.solution.cycles[50].plot(['Terminal voltage [V]'])
    # sim.solution.cycles[-1].plot(['Terminal voltage [V]'])

    # print("nominal capacity: " + str(param['Nominal cell capacity [A.h]'])) = 5

    # y = sim.solution.cycles[0]['Terminal voltage [V]'].entries  # gets more detailed params per cycle
    # x = sim.solution.cycles[0]['Time [s]'].entries
    # for i, item in enumerate(x):
    #     print(item, y[i])

    # Qt = sol["Throughput capacity [A.h]"].entries
    # Q_SEI = [5-item for item in sol["Loss of capacity to negative SEI [A.h]"].entries]
    # Q_SEI_cr = [5-item for item in sol["Loss of capacity to negative SEI on cracks [A.h]"].entries]
    # Q_plating = [5-item for item in sol["Loss of capacity to negative lithium plating [A.h]"].entries]
    # Q_side = [5-item for item in sol["Total capacity lost to side reactions [A.h]"].entries]
    # Q_LLI = [5-item for item in (
    #     sol["Total lithium lost [mol]"].entries * 96485.3 / 3600
    # )]  # convert from mol to A.h
    # plt.figure()
    # plt.plot(Qt, Q_SEI, label="SEI", linestyle="dashed")
    # plt.plot(Qt, Q_SEI_cr, label="SEI on cracks", linestyle="dashdot")
    # plt.plot(Qt, Q_plating, label="Li plating", linestyle="dotted")
    # plt.plot(Qt, Q_side, label="All side reactions", linestyle=(0, (6, 1)))
    # plt.plot(Qt, Q_LLI, label="All LLI")
    # plt.xlabel("Throughput capacity [A.h]")
    # plt.ylabel("Capacity left [A.h]")
    # plt.legend()
    # plt.show()

    # Qt = sol["Throughput capacity [A.h]"].entries # not sure what to do with this yet
    # LLI = sol["Loss of lithium inventory [%]"].entries
    # LAM_neg = sol["Loss of active material in negative electrode [%]"].entries
    # LAM_pos = sol["Loss of active material in positive electrode [%]"].entries
    # plt.figure()
    # plt.plot(Qt, LLI, label="LLI")
    # plt.plot(Qt, LAM_neg, label="LAM (negative)")
    # plt.plot(Qt, LAM_pos, label="LAM (positive)")
    # plt.xlabel("Throughput capacity [A.h]")
    # plt.ylabel("Degradation modes [%]")
    # plt.legend()
    # plt.show()

    # eps_neg_avg = sol["X-averaged negative electrode porosity"].entries  # not important for current application
    # eps_neg_sep = sol["Negative electrode porosity"].entries[-1, :]
    # eps_neg_CC = sol["Negative electrode porosity"].entries[0, :]
    # plt.figure()
    # plt.plot(Qt, eps_neg_avg, label="Average")
    # plt.plot(Qt, eps_neg_sep, label="Separator", linestyle="dotted")
    # plt.plot(Qt, eps_neg_CC, label="Current collector", linestyle="dashed")
    # plt.xlabel("Throughput capacity [A.h]")
    # plt.ylabel("Negative electrode porosity")
    # plt.legend()
    # plt.show()

    # vars_to_track = [ "Time [s]", "Current [A]", "Voltage [V]", 'Local ECM resistance [Ohm]', 'Ambient temperature [K]','Total capacity lost to side reactions [A.h]']
    # sol.save_data(f"capacity_tester.csv", vars_to_track, to_format="csv") # save as csv

    sol.last_state.save(f"mini_dataset/last_state_{i}.pkl")  # how to save solution aka pybamm object
    with open('mini_dataset/master.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        # Write rows one by one
        writer.writerow([i, discharge_cap, capacity])


    print(f"saved iteration: {i}")
    # break # only take one cycle

# vars_to_track = [ "Time [s]", "Current [A]", "Voltage [V]"]
# sol.save_data("data.csv", vars_to_track, to_format="csv") # save as csv

# print(sol.summary_variables['Capacity [A.h]'])

# for i in sol.summary_variables.keys():
#     print(i)

# x = np.arange(len(sol.summary_variables["Capacity [A.h]"]))
# y = sol.summary_variables["Capacity [A.h]"]


b = time.time()
print(f'total sim time: {b-a} seconds')

with open('mini_dataset/master.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    # Write header if needed
    writer.writerow(['Time:', f'{b-a} seconds', ''])


# plt.plot(x, y, label='Discharge cap', marker='o')
# plt.xlabel('Index')
# plt.ylabel('Capacity')   # WORKS AS A MAX CAPACITY VALUE, is a summary variable though..
# plt.title('SOC differences')
# plt.legend()
# plt.grid(True)
# plt.show()

# print(x)
# print(y)
# print(param['Nominal cell capacity [A.h]'])

'''
Dataset vs. starting params

1. original: 100 cycles
2.
3.

'''
