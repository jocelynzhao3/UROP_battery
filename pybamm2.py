## basic simulation code, problem is getting the data off the graphs

import pybamm
import time

# print(pybamm.parameter_sets.get_docstring("Sulzer2019"))

# a = time.time()
# model = pybamm.lithium_ion.SPM()  # Doyle-Fuller-Newman model
# sim = pybamm.Simulation(model)
# sim.solve([0, 3600])  # solve for 1 hour
# b = time.time()
# sim.plot()


# print(f'run time: {b-a} seconds')


# #################################################

# # experiment = pybamm.Experiment(
# #     [
# #         (
# #             "Discharge at C/10 for 10 hours or until 3.3 V",
# #             "Rest for 1 hour",
# #             "Charge at 1 A until 4.1 V",
# #             "Hold at 4.1 V until 50 mA",
# #             "Rest for 1 hour",
# #         )
# #     ]
# #     * 3,
# # )
# # model = pybamm.lithium_ion.DFN()
# # sim = pybamm.Simulation(model, experiment=experiment, solver=pybamm.CasadiSolver())
# # sim.solve()
# # sim.plot()

# ################################################

# model = pybamm.lithium_ion.SPMe()
# sim = pybamm.Simulation(model)

# solution = sim.solve([0, 3600]) # solution object

# t = solution["Time [s]"] # define vars, find more options in model.variable_names()
# V = solution["Voltage [V]"]

# print(V.entries) # V([200, 400, 780, 1236]) for specific times in seconds


models = [
    pybamm.lithium_ion.SPM(),
    pybamm.lithium_ion.SPMe(),
    pybamm.lithium_ion.DFN(),
]

sims = []
for model in models:
    sim = pybamm.Simulation(model)
    sol = sim.solve([0, 3600]) # solve for time window [0, 3600] aka 1 hour in seconds
    sims.append(sim)

    print(sol.summary_variables)

# pybamm.dynamic_plot(sims)

# for item in list(pybamm.parameter_sets):
#     print(item)
