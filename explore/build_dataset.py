import os
import time
import numpy as np
import pandas as pd
import pybamm
from scipy.stats import qmc

N_SAMPLES = 50              # small test run; we'll scale up later
NOMINAL_CAPACITY = 5.0      # Ah (LG M50)

# Design variables: thickness [m], porosity [-], particle radius [m], C-rate
lower = [50e-6, 0.25, 3e-6, 0.5]
upper = [100e-6, 0.45, 8e-6, 2.5]

# Spread the samples evenly across all four ranges (Latin hypercube sampling)
sampler = qmc.LatinHypercube(d=4, seed=42)
samples = qmc.scale(sampler.random(n=N_SAMPLES), lower, upper)

model = pybamm.lithium_ion.DFN()
rows = []
start_all = time.perf_counter()

for i, (thickness, porosity, radius, c_rate) in enumerate(samples):
    param = pybamm.ParameterValues("Chen2020")
    param["Positive electrode thickness [m]"] = thickness
    param["Positive electrode porosity"] = porosity
    # TODO 1: the electrode is solid particles + pores, and the two fractions add up to 1.
    #         Set the solid (active material) fraction using porosity.
    param["Positive electrode active material volume fraction"] = 1 - porosity
    param["Positive particle radius [m]"] = radius
    # TODO 2: set the discharge current in amps from the C-rate.
    param["Current function [A]"] = c_rate * NOMINAL_CAPACITY

    t_end = 3600 / c_rate * 1.3
    try:
        sim = pybamm.Simulation(model, parameter_values=param)
        sol = sim.solve(np.linspace(0, t_end, 500))
        t = sol["Time [s]"].entries
        v = sol["Voltage [V]"].entries
        current = sol["Current [A]"].entries
        capacity = sol["Discharge capacity [A.h]"].entries[-1]
        energy = np.trapezoid(v * current, t) / 3600     # Wh
        reached_cutoff = bool(v[-1] <= 2.51)
        status = "ok"
    except Exception as e:
        capacity, energy, reached_cutoff, status = np.nan, np.nan, False, f"failed: {e}"

    rows.append({
        "thickness_um": thickness * 1e6,
        "porosity": porosity,
        "particle_radius_um": radius * 1e6,
        "c_rate": c_rate,
        "capacity_Ah": capacity,
        "energy_Wh": energy,
        "reached_cutoff": reached_cutoff,
        "status": status,
    })
    print(f"[{i+1}/{N_SAMPLES}] {thickness*1e6:.0f} µm, por {porosity:.2f}, "
          f"r {radius*1e6:.1f} µm, {c_rate:.2f}C -> {capacity:.2f} Ah ({status})")

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv("data/dataset_test.csv", index=False)
print(f"Done: {len(df)} runs in {time.perf_counter() - start_all:.1f} s")
print(df.describe())