import numpy as np
import pybamm
import matplotlib.pyplot as plt

model = pybamm.lithium_ion.SPMe()
thicknesses = [60e-6, 75.6e-6, 90e-6]   # cathode thickness in meters
c_rates = [1, 2, 3]
nominal_capacity = 5.0                   # Ah (LG M50)

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, c in zip(axes, c_rates):
    current = c * nominal_capacity       # amps
    t_end = 3600 / c * 1.2               # a bit longer than the discharge needs
    for t in thicknesses:
        param = pybamm.ParameterValues("Chen2020")
        param["Positive electrode thickness [m]"] = t
        param["Current function [A]"] = current
        sim = pybamm.Simulation(model, parameter_values=param)
        sol = sim.solve(np.linspace(0, t_end, 500))
        cap = sol["Discharge capacity [A.h]"].entries
        ax.plot(cap, sol["Voltage [V]"].entries, label=f"{t*1e6:.0f} µm")
        print(f"{c}C, {t*1e6:.0f} µm cathode: {cap[-1]:.2f} Ah")
    ax.set_title(f"{c}C ({current:.0f} A)")
    ax.set_xlabel("Discharge capacity (Ah)")

axes[0].set_ylabel("Voltage (V)")
axes[0].legend()
plt.tight_layout()
plt.savefig("explore/crate_sweep.png", dpi=200)
plt.show()