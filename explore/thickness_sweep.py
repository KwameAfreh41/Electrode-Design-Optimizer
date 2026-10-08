import pybamm
import matplotlib.pyplot as plt

model = pybamm.lithium_ion.SPMe()  # faster, simpler model

for t in [60e-6, 75.6e-6, 90e-6]:
    param = pybamm.ParameterValues("Chen2020")
    param["Positive electrode thickness [m]"] = t
    sim = pybamm.Simulation(model, parameter_values=param)
    sol = sim.solve([0, 5000])
    plt.plot(sol["Discharge capacity [A.h]"].entries,
             sol["Voltage [V]"].entries,
             label=f"{t*1e6:.0f} µm cathode")

plt.xlabel("Discharge capacity (Ah)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.savefig("explore/thickness_sweep.png", dpi=200)
plt.show()