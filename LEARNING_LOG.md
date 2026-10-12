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