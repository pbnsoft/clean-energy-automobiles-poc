# Run Guide — `src/wind_model.py`

## Requirements

Python 3. Nothing else — the model uses only the standard library.

## Run it

From the repository root:

```bash
python3 src/wind_model.py
```

## What it prints

1. **The default case** — 90 km/h cruise in calm air: harvest **1270 W (1.27 kW)**, drag penalty **2050 W (2.05 kW)**, **net −780 W**. This is the validated anchor condition, and the net is negative on purpose: the model charges the turbines' drag through the 90%-efficient drivetrain, and at cruise the bill exceeds the harvest.
2. **A headwind sweep** at 90 km/h cruise, headwind 0–100 km/h in 10 km/h steps, showing harvest, penalty and net at each step.
3. **The break-even point** — the headwind at which the net crosses zero at 90 km/h cruise: **≈73 km/h**.
4. **The parked-in-a-storm case** — vehicle speed 0, storm wind ≈54 km/h: harvest **301 W**, penalty **0 W** (a parked car pays no drag bill), net **+301 W**.

If your run reproduces 1.27 kW / 2.05 kW / −780 W / 73 km/h / 301 W, the calibration is intact.

## Use it as a library

```python
import sys
sys.path.insert(0, "src")
from wind_model import harvest_power, drag_penalty, net_power, break_even_headwind

harvest_power(90, 0)        # 1270 W — cruise, calm
drag_penalty(90, 0)         # 2050 W
net_power(90, 0)            # -780 W
net_power(90, 80)           # positive: a storm-grade headwind pays
net_power(0, 53.89)         # +301 W — parked in the storm preset
break_even_headwind(90)     # ~73 km/h
break_even_headwind(110)    # break-even headwind at a faster cruise
```

### Parameters

All power functions take:

- `vehicle_kmh` — road speed.
- `headwind_kmh` — opposing wind; use a negative value for a tailwind.
- `turbine_area` (default 0.60 m²) — swept area of the turbine set; scales harvest and drag area linearly.
- `turbine_efficiency` (default 0.28) — scales harvest linearly (`harvest_power` and `net_power` only; the drag penalty does not depend on how good the generator is — a worse generator harvests less but drags exactly the same, which is precisely the trap this model exists to show).

## Calibration note

The constants in the module (effective harvest exponent 2.807, drag area 0.1928 m², motor efficiency 0.90) are **calibrated to the validated outputs of the published interactive model**, as documented in the module docstring and in [how-it-works.md](how-it-works.md). Treat them as the fitted constants of this proof of concept, not as predictions for a specific production vehicle.
