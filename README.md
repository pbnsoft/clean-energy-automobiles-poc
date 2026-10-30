# Clean Energy Automobiles — Proof of Concept

**The idea:** fit a car with ducted wind turbines that harvest energy from the air moving around it as it drives. The physics verdict, after the idea was rebuilt as an interactive model and validated: at highway cruise the turbines' extra drag costs more energy than they harvest — the "wind" at cruise is mostly wind the car itself created. The harvest only pays when the air moves on its own: driving into a strong headwind, descending, braking, or parked in a storm. The author's chosen design hides flight-style turbines inside the bodywork, invisible from outside and revealed only in an X-ray view — the styling never advertises the machinery.

*Chapter 4 of* **Inventions and Innovations** *by Balasubramanian Natarajan — "What an Agent Can Do With a Decade-Old Idea" (the 2017 article "Clean Energy for Automobiles," revisited in 2026).*

## The honest numbers first

At the reference cruise condition — 90 km/h, calm air — the validated model gives:

| | |
|---|---|
| Harvest | 1.27 kW |
| Drag penalty (charged through 90% motor efficiency) | 2.05 kW |
| **Net** | **−780 W** |

The idea does **not** produce a net gain at cruise, and this repository does not pretend otherwise. Break-even arrives only at a **73 km/h headwind** at 90 km/h cruise. Parked in a storm, the same turbines return **301 W at zero drag cost** — that is where the concept earns its keep.

## What's inside

- **`src/wind_model.py`** — the calibrated reference model (Python 3, standard library only): harvest vs. drag penalty as parameterized functions of vehicle speed, headwind, turbine area and efficiency, with a break-even solver. Its constants are calibrated to reproduce the published interactive model's validated anchor figures exactly (see the module docstring).
- **`docs/`** — the documentation folder: [index](docs/README.md), [how it works](docs/how-it-works.md) (the model and the published evidence), and the [run guide](docs/run-guide.md).
- **`media/`** — the concept films:
  - [`media/clean-energy-concept-film.mp4`](media/clean-energy-concept-film.mp4) — the concept film: the car, the airflow, and the author's chosen design, hidden flight-style turbines inside the body shown via the X-ray view.
  - [`media/clean-energy-improvements-film.mp4`](media/clean-energy-improvements-film.mp4) — the improvements animation: how the design evolved toward the hidden-turbine layout.

## Quick start

```bash
python3 src/wind_model.py
```

No dependencies — Python 3 standard library only. The script prints the default cruise case (harvest 1.27 kW, penalty 2.05 kW, net −780 W), a headwind sweep at 90 km/h, the break-even headwind (≈73 km/h), and the parked-in-a-storm case (301 W harvest, 0 W penalty). To explore other conditions, import the functions:

```python
from src.wind_model import harvest_power, drag_penalty, net_power, break_even_headwind
net_power(90, 40)          # net watts at 90 km/h into a 40 km/h headwind
break_even_headwind(110)   # headwind needed to break even at 110 km/h
```

See [docs/run-guide.md](docs/run-guide.md) for parameter details.
