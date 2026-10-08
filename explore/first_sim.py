import pybamm

model = pybamm.lithium_ion.DFN()
param = pybamm.ParameterValues("Chen2020")
sim = pybamm.Simulation(model, parameter_values=param)
sim.solve([0, 3600])
sim.plot()