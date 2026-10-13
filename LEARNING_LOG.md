# Learning Log

## Oct 6, 2026
- Set up Python 3.13, VS Code, Git, and PyBaMM 26.9 on my M4 Mac
- Fixed a broken Anaconda startup block in .zshrc (and a file ownership issue with sudo chown)
- Learned: what a virtual environment is and why each project gets its own
## Oct 7, 2026
- Next: run my first PyBaMM simulation
## Oct 11, 2026 — C-rate sweep (1C, 2C, 3C)
- Prediction: at 3C, the 90 um cathode will deliver the most capacity, because the cathode has more active materials for the arriving ions
- Result: the 90 µm cathode delivered the most capacity at every C-rate
  (1C: 4.96 Ah, 2C: 4.80 Ah, 3C: 0.26 Ah). [My prediction was right]
- Why thick still won: current was fixed in amps, so the thin 60 µm cathode
  ran at a harsher C-rate relative to its own capacity. Its particle surfaces
  saturated faster (solid-state diffusion limitation), and the voltage crashed
  early (3.82 Ah at 2C).
- Why 3C collapsed (~0.25 Ah for all): electrolyte depletion. The cathode
  consumes Li+ at a rate set by Faraday's law (current / F), 3x faster at 3C.
  The electrolyte can't deliver ions that fast, salt near the cathode drops
  toward zero, and the reaction stalls.
- Key idea: high current doesn't slow ions down; it demands more transport
  than the electrolyte can supply (limiting current).
- Caveat: SPMe is less trustworthy at high current; the staircase at 3C is the
  solver struggling. LG M50 is an energy cell, not built for 15 A.
- Next: rerun 3C with DFN and compare against SPMe (model validation).
- DFN treats each electrode as many particles at different depths, and tracks where along the electrode thickness the reaction is happening. At high current, most of the reaction crowds toward the separator side, where ions are easiest to reach. DFN captures that.
- SPMe assumes every particle in an electrode behaves the same, so one "average particle" stands in for all of them. It adds a simplified correction for the electrolyte that only works when concentration differences are small.
## Oct 12, 2026 — SPMe vs DFN (model validation)

### Results (75.6 µm cathode, LG M50 / Chen2020)
| C-rate | SPMe    | DFN     | Verdict          |
|--------|---------|---------|------------------|
| 1C     | 4.94 Ah | 4.94 Ah | Identical        |
| 2C     | 4.76 Ah | 4.73 Ah | ~0.6% apart, OK  |
| 3C     | 0.25 Ah | 2.30 Ah | SPMe fails       |

Speed: SPMe ~0.1 s, DFN ~0.4 s per run (only ~4x slower on my M4).

### What I learned
- DFN tracks particles at every depth of the electrode, so it captures
  where the reaction happens. At high current, the reaction crowds toward
  the separator side.
- SPMe uses one "average particle" per electrode plus a simplified
  electrolyte correction. That only works when gradients are small.
- At 3C, SPMe's assumptions break, and its collapse (0.25 Ah) was a model
  failure, not the battery. My Oct 11 conclusion was partly wrong: the
  real 3C capacity (DFN) is ~2.30 Ah.
- The real loss at 3C (2.30 vs 4.94 Ah) still comes from transport limits:
  electrolyte gradients and solid diffusion.
- Lesson: always validate a fast model against a trusted one before
  relying on it.

### Decision
- Use DFN to generate the ML training data: accurate at all C-rates and
  fast enough (~2,000 runs in ~15 min).
- The ML surrogate is still needed: Monte Carlo × many designs × instant
  web app answers = millions of evaluations.

### Code I learned
- `time.perf_counter()` before and after a step = how long it took
  (computer time, not battery time).
- A dictionary `{"SPMe": ..., "DFN": ...}` lets one loop run several models.
- Dropped `plt.show()`; `savefig` saves the plot and the terminal stays free.

### Next
- Build the dataset: run DFN over many combinations of design variables.