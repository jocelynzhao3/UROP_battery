import pybamm   # https://github.com/pybamm-team/PyBaMM/tree/main
import numpy as np
import matplotlib.pyplot as plt

### compare models ###
model = pybamm.lithium_ion.DFN() # load a model
# create simulation

models = [
    pybamm.lithium_ion.SPM(),
    pybamm.lithium_ion.SPMe(),
    pybamm.lithium_ion.DFN(),
]

sims = []
for model in models:
    sim = pybamm.Simulation(model)
    sim.solve([0, 3600]) # solve for time window [0, 3600] aka 1 hour in seconds
    sims.append(sim)

pybamm.dynamic_plot(sims)

### plotting ###
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600])

model.variable_names() # A LOT
model.variables.search("electrolyte") # easier to search

output_variables = ["Electrolyte concentration [mol.m-3]", "Voltage [V]"] # what to plot
sim.plot(output_variables=output_variables)

# output_variables = ["Voltage [V]"] # plotting one thing needs a list
# sim.plot(output_variables=output_variables)

# sim.plot(  # plotting Electrode data on the same graph
#     [
#         ["Electrode current density [A.m-2]", "Electrolyte current density [A.m-2]"],
#         "Voltage [V]",
#     ]
# )

# sim.plot_voltage_components() # voltage stuff, pass solution as arg?
# sim.plot_voltage_components(split_by_electrode=True)

### setting params ###

parameter_values = pybamm.ParameterValues("Chen2020") # many parameter sets
parameter_values # A LOT
parameter_values["Electrode height [m]"] # access via dictionary syntax
parameter_values.search("electrolyte") # find params via keyword

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, parameter_values=parameter_values) # add specific parameter values
sim.solve([0, 3600])
sim.plot()

model.print_parameter_info() # see param type to make individual changes
parameter_values["Current function [A]"] = 10

sim = pybamm.Simulation(model, parameter_values=parameter_values) # same as above
sim.solve([0, 3600])
sim.plot()

def my_current(t): # make time dependent current
    return pybamm.sin(2 * np.pi * t / 60)
parameter_values["Current function [A]"] = my_current

sim = pybamm.Simulation(model, parameter_values=parameter_values) # simulate again
t_eval = np.arange(0, 121, 1)
sim.solve(t_eval=t_eval) # array of points to evaluate solution to solver
sim.plot(["Current [A]", "Voltage [V]"])

def cube(t):
    return t**3

parameter_values = pybamm.ParameterValues( # make new
    {
        "Negative electrode thickness [m]": 1e-4,
        "Positive electrode thickness [m]": 1.2e-4,
        "Current function [A]": cube,
    }
)

### run experiments ###

experiment = pybamm.Experiment( # instructions on how to cycle the battery
    [
        (
            "Discharge at C/10 for 10 hours or until 3.3 V",
            "Rest for 1 hour",
            "Charge at 1 A until 4.1 V",
            "Hold at 4.1 V until 50 mA",
            "Rest for 1 hour",
        )
    ]
    * 3
    + [
        "Discharge at 1C until 3.3 V",
    ]
) # note that steps (list) can be skipped but cycles (tuples) cannot

# more long experiments: https://github.com/pybamm-team/PyBaMM/blob/a553fe6b980abfdb560263be78d72ad534d25419/docs/source/examples/notebooks/simulations_and_experiments/simulating-long-experiments.ipynb

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model, experiment=experiment)
sim.solution.cycles[0].plot() # sol.cycles is a list, the indexing starts at 0.

# pybamm.step.string(  # add conditions to a string-defined step
#     "Discharge at 1C for 1 hour", period="1 minute", temperature="25oC", tags=["tag1"]
# )

'''
pybamm.step.current(1, duration="1 hour", termination="2.5 V") is equivalent to
pybamm.step.string("Discharge at 1A for 1 hour or until 2.5V")

available methods are current, c_rate, voltage, power, and resistance

define drive cycle:
t = np.linspace(0, 1, 60)
sin_t = 0.5 * np.sin(2 * np.pi * t)
drive_cycle_power = np.column_stack([t, sin_t])
experiment = pybamm.Experiment([pybamm.step.power(drive_cycle_power)])
sim = pybamm.Simulation(model, experiment=experiment)
sim.solve()
sim.plot()
'''

### output management ###

model = pybamm.lithium_ion.SPMe()
sim = pybamm.Simulation(model)

solution = sim.solve([0, 3600]) # solution object

t = solution["Time [s]"] # define vars, find more options in model.variable_names()
V = solution["Voltage [V]"]

V.entries # V([200, 400, 780, 1236]) for specific times in seconds
t.entries

sim.save("SPMe.pkl") # save long simulation data
sim2 = pybamm.load("SPMe.pkl") # reload and plot saved data
sim2.plot()

# Alternative:
sol = sim.solution
sol.save("SPMe_sol.pkl")
sol2 = pybamm.load("SPMe_sol.pkl")
sol2.plot()

sol.save_data("sol_data.pkl", ["Current [A]", "Voltage [V]"]) # save specific vars

sol.save_data("sol_data.csv", ["Current [A]", "Voltage [V]"], to_format="csv") # save as csv

# sol.save_data( # matlab needs names without spaces
#     "sol_data.mat",
#     ["Current [A]", "Voltage [V]"],
#     to_format="matlab",
#     short_names={"Current [A]": "I", "Voltage [V]": "V"},
# )

# csv and mat only work for 0D variables (variables the do not depend on space, only on time)

# import os   # remvove files
# os.remove("SPMe.pkl")
# os.remove("SPMe_sol.pkl")
# os.remove("sol_data.pkl")
# os.remove("sol_data.csv")
# os.remove("sol_data.mat")

### model options ###

options = {"thermal": "lumped"}
model = pybamm.lithium_ion.SPMe(options=options)  # loading in options
sim = pybamm.Simulation(model)
sim.solve([0, 3600])
sim.plot(["Cell temperature [K]", "Total heating [W.m-3]", "Current [A]", "Voltage [V]"])

# many model options avaliable - will require more research

### solver options ###

model = pybamm.lithium_ion.DFN()
param = model.default_parameter_values
param["Lower voltage cut-off [V]"] = 3.6

safe_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="safe")
fast_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="fast")


safe_sim = pybamm.Simulation(model, parameter_values=param, solver=safe_solver) # create simulations
fast_sim = pybamm.Simulation(model, parameter_values=param, solver=fast_solver)

safe_sim.solve([0, 3600])
print(f"Safe mode solve time: {safe_sim.solution.solve_time}")
fast_sim.solve([0, 3600])
print(f"Fast mode solve time: {fast_sim.solution.solve_time}")
pybamm.dynamic_plot([safe_sim, fast_sim])

# I don't really understand this feature

### changing the mesh ###

model = pybamm.lithium_ion.SPMe()
model.default_var_pts  # number of points used in models

var_pts = {   # create our dictionary
    "x_n": 10,  # negative electrode
    "x_s": 10,  # separator
    "x_p": 10,  # positive electrode
    "r_n": 10,  # negative particle
    "r_p": 10,  # positive particle
}

sim = pybamm.Simulation(model, var_pts=var_pts)
sim.solve([0, 3600])
sim.plot()

npts = [4, 8, 16, 32, 64]  # increased precision ('resolution')
model = pybamm.lithium_ion.DFN()
parameter_values = pybamm.ParameterValues("Ecker2015")
solver = pybamm.CasadiSolver(mode="fast")
solutions = []
for N in npts:
    var_pts = {
        "x_n": N,  # negative electrode
        "x_s": N,  # separator
        "x_p": N,  # positive electrode
        "r_n": N,  # negative particle
        "r_p": N,  # positive particle
    }
    sim = pybamm.Simulation(
        model, solver=solver, parameter_values=parameter_values, var_pts=var_pts
    )
    sim.solve([0, 3600])
    solutions.append(sim.solution)

pybamm.dynamic_plot(solutions, ["Voltage [V]"], labels=npts)
