# How It Works — the Wind-Harvest Model

## The question

A moving car sits in a powerful airflow of its own making. Ducted turbines in that airflow will unquestionably generate electricity — the engineering question is never *whether* they generate, but *what the generation costs*. Every watt a turbine extracts from the airstream is paid for in aerodynamic drag, and the motor has to repay that drag from the same battery the turbine is charging. This model keeps both sides of that ledger, in the open, at all times.

## The model

Let **v** be the car's road speed and **h** the headwind (tailwind counts negative). The turbines see the relative air speed **v_rel = v + h**.

**Harvest.** Electrical output grows with the relative airflow — steeply, but not with the textbook cube: duct losses and generator efficiency roll off as inflow rises, so the validated model uses an effective sub-cubic exponent (2.807). Turbine area and turbine/generator efficiency scale the harvest linearly.

**Drag penalty.** The turbine installation adds a drag area (CdA). The extra drag force is the standard ½·ρ·CdA·v_rel²; the mechanical power to overcome it at road speed is force × v; and the electrical penalty charged to the battery divides that by the **motor/drivetrain efficiency of 90%**. The drag bill is therefore always paid at a markup — one of the two reasons cruise never breaks even. The other is simpler: at cruise in calm air, v_rel is wind the car paid to create in the first place.

**The parked case falls out of the same equations.** With v = 0 the drag penalty is force × 0 = 0. A parked car's turbines harvest weather, not self-made wind, and keep all of it.

## The validated anchor figures

The constants in `src/wind_model.py` are calibration constants fitted so this implementation reproduces the published interactive model's independently validated outputs:

| Condition | Harvest | Drag penalty | Net |
|---|---|---|---|
| 90 km/h cruise, calm air | 1.27 kW | 2.05 kW | **−780 W** |
| 90 km/h cruise, break-even headwind 73 km/h | — | — | 0 W |
| Parked, storm wind (≈54 km/h) | 301 W | 0 W | **+301 W** |

The cruise row deserves emphasis because it is the row most versions of this idea omit: **at cruise, the concept loses 780 W**. The book prints that number in the chapter, and this repository leads with it.

## Where the idea does pay

- **Headwinds.** Once the opposing wind is strong enough (73 km/h at a 90 km/h cruise), the airflow carries energy the car did not pay for, and the net turns positive.
- **Descents and braking.** Air the car would shed anyway can be harvested on the way down or while slowing.
- **Parked in a storm.** 301 W of genuinely free harvest — a car sitting in bad weather trickle-charging itself.

The author's chosen embodiment follows from that verdict: flight-style turbines **hidden inside the bodywork**, invisible from outside and shown only in an X-ray view — deployed and useful in the conditions above, without styling the car around machinery that is a passenger the rest of the time. Both films in [`../media/`](../media/) show this design.

## The published evidence — read honestly

This idea has been studied, and the record is the reason the chapter's claims are as narrow as they are:

- **El et al., *Thermal Science* (2022)** — a CFD simulation of a turbine embedded in a car's front duct at 97 km/h produced **1.40 kW**, yet recovered only **5.13% of the base car's total losses**, while the drag coefficient rose **+4.05%**. The authors claim a small net positive — **in simulation only**.
- **Yıldız & Dandil, *Scientia Iranica* (2025)** — a simulation study in the same research lineage found ≈**6.51% of aerodynamic losses recovered**, with Cd up only +0.38%. Again simulation, and the same school of authors — one line of evidence, not two independent ones.
- **Akgün & Gürbüz (2025)** — the rare **road test** (a Toyota Corolla): generation worked at every speed and was **better driving into a headwind** than with it, matching this model's shape. But the test **never metered the drag cost**, so it cannot speak to the net.
- **Lightyear (economics, not aerodynamics).** The solar-car maker harvested genuinely external energy with no drag bill at all — and still failed on economics: production began December 2022 at roughly one car a week at €250,000, halted in January 2023, and its production company was bankrupt within weeks. Even free energy loses to manufacturing cost at the wrong price point.

The sentence the evidence supports, and the one this repository stands on: **no instrumented road test anywhere has yet netted a car turbine's electrical output against its full drivetrain drag cost.** The simulations disagree about the margin; none of them overturns the cruise verdict in the model above, and the honest deployment envelope — headwind, descent, braking, storm parking — is what remains standing after the evidence is read whole.
