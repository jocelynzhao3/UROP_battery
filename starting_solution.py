import pybamm
import pickle
import matplotlib.pyplot as plt


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

param["Negative electrode Paris' law constant b"] = 1.12*15
cycle_number = 10
experiment_1 = pybamm.Experiment([
            (
                "Discharge at 1C until 2.5 V",  # ageing cycles
                "Charge at 0.3C until 4.2 V (5 minute period)",
                "Hold at 4.2 V until C/100 (5 minute period)",
            )
        ]  * cycle_number)

# sim = pybamm.Simulation(model, experiment=experiment_1, parameter_values=param, var_pts=var_pts)
# sol_1 = sim.solve()

experiment_2 = pybamm.Experiment(
    [
        (
            "Charge at 1C until 4.2V",
            "Hold at 4.2V until C/50",
            "Discharge at 1C until 3V",
            "Rest for 1 hour",
        ),
    ]*2
)

sim = pybamm.Simulation(model, experiment=experiment_2, parameter_values=param, var_pts=var_pts)
# sol_2 = sim.solve(starting_solution=sol_1)  # start from aged battery
# sol_2.plot()
# sol_2.cycles[-1].plot()

sol_3 = sim.solve()
print(sol_3['Discharge capacity [A.h]'].entries[-1])

# sol_3.plot()
# sol_3.cycles[-1].plot()

sol_3.last_state.save("last_state.pkl")  # how to save solution aka pybamm object
print('done')

final_state = sol_3.cycles[-1] # just taking the last entry
sol_3.cycles[-1].save('alt_last_state.pkl')  # saves entire thing

print(final_state["Voltage [V]"].entries)
print(final_state['Discharge capacity [A.h]'].entries[-1])  # when you save final state it seems discharge cap goes back to 0
# print(final_state.summary_variables['Capacity [A.h]'])


# with open('saved_solution.pkl', 'rb') as f:
#     saved_sol = pickle.load(f)

# for x in saved_sol.summary_variables:
#     print(x)

# print(sol_3['Discharge capacity [A.h]'].entries)

print(sol_3.summary_variables['Capacity [A.h]'][-1])
# print(final_state.summary_variables['Capacity [A.h]'])  # will not work :(
# sol.summary_variables["Capacity [A.h]"]
