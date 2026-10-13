import time
import numpy as np
import pybamm
import matplotlib.pyplot as plt

models = {
    "SPMe": pybamm.lithium_ion.SPMe(),
    "DFN": pybamm.lithium_ion.DFN(),
}
c_rates = [1, 2, 3]
nominal_capacity = 5.0   # Ah (LG M50)

fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)

for ax, c in zip(axes, c_rates):
    t_end = 3600 / c * 1.2
    for name, model in models.items():
        param = pybamm.ParameterValues("Chen2020")
        param["Current function [A]"] = c * nominal_capacity
        sim = pybamm.Simulation(model, parameter_values=param)

        start = time.perf_counter()
        sol = sim.solve(np.linspace(0, t_end, 500))
        elapsed = time.perf_counter() - start

        cap = sol["Discharge capacity [A.h]"].entries
        ax.plot(cap, sol["Voltage [V]"].entries, label=name)
        print(f"{c}C {name}: {cap[-1]:.2f} Ah in {elapsed:.2f} s")
    ax.set_title(f"{c}C ({c * nominal_capacity:.0f} A)")
    ax.set_xlabel("Discharge capacity (Ah)")

axes[0].set_ylabel("Voltage (V)")
axes[0].legend()
plt.tight_layout()
plt.savefig("explore/model_comparison.png", dpi=200)
print("Saved plot to explore/model_comparison.png")