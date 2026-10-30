#!/usr/bin/env python3
"""Clean Energy Automobiles — wind-harvest model (proof of concept).

Implements the validated physics model behind Chapter 4 of
*Inventions and Innovations* ("What an Agent Can Do With a Decade-Old Idea"):
ducted turbines on a moving car harvest energy from the air flowing around
it, but the extra aerodynamic drag they create is charged back through the
drivetrain at 90% motor efficiency.

THE HONEST HEADLINE: at highway cruise in calm air the drag bill is LARGER
than the harvest (net -780 W at 90 km/h). The idea only pays when the air
moves on its own — a strong headwind, a descent, braking, or a parked car
in a storm.

CALIBRATION NOTE
----------------
The constants below are calibrated so this reference implementation
reproduces the validated outputs of the published interactive model:

  * 90 km/h cruise, calm air ... harvest 1.27 kW, drag penalty 2.05 kW,
                                 net -780 W  (~122 Wh/km total consumption
                                 in the book's accounting)
  * break-even headwind ........ 73 km/h at 90 km/h cruise
  * parked in a storm .......... 301 W harvest, 0 W penalty

They are calibration constants fitted to those anchor points, not
first-principles predictions for any specific vehicle.

MODEL SHAPE
-----------
Relative air speed  v_rel = vehicle speed + headwind (tailwind negative).

Harvest:  P_h = K_H * A_scale * eta_scale * v_rel ** 2.807
    The exponent is sub-cubic (not the textbook 3.0) because duct losses
    and generator efficiency roll off as inflow rises; 2.807 is the
    effective exponent that fits the validated model's anchors.

Drag penalty: the turbines add a drag area CdA. The extra drag force is
    F = 0.5 * rho * CdA * v_rel ** 2
    the mechanical power to overcome it at road speed v is F * v, and the
    electrical penalty charged to the battery divides by the motor /
    drivetrain efficiency (0.90):
        P_penalty = F * v / 0.90
    A parked car (v = 0) therefore pays no drag penalty at all — which is
    exactly why the parked-in-a-storm case is genuinely free energy.

Python 3, standard library only.
"""

# --- Calibrated constants (see CALIBRATION NOTE above) --------------------

RHO = 1.225               # air density, kg/m^3 (sea level, standard)
MOTOR_EFFICIENCY = 0.90   # drivetrain efficiency the drag bill is charged through

REFERENCE_SPEED = 25.0    # m/s (= 90 km/h), the calibration reference point
HARVEST_AT_REFERENCE = 1270.0   # W at the reference point, calm air
HARVEST_EXPONENT = 2.807        # effective (sub-cubic) harvest exponent, calibrated
HARVEST_COEFF = HARVEST_AT_REFERENCE / REFERENCE_SPEED ** HARVEST_EXPONENT

# Extra drag area (Cd * A, m^2) of the turbine installation, sized so the
# electrical drag penalty at the reference point is 2.05 kW:
#   penalty = (0.5 * RHO * CdA * v_rel^2) * v / MOTOR_EFFICIENCY
DRAG_AREA = 0.1928        # m^2, calibrated

DEFAULT_TURBINE_AREA = 0.60    # m^2 swept area of the ducted turbine set
DEFAULT_TURBINE_EFFICIENCY = 0.28  # nominal turbine+generator efficiency label

# Preset: parked car, storm wind. Wind speed chosen (calibrated) so the
# harvest matches the validated model's 301 W.
STORM_WIND_KMH = 53.89


def _ms(kmh):
    return kmh / 3.6


def harvest_power(vehicle_kmh, headwind_kmh,
                  turbine_area=DEFAULT_TURBINE_AREA,
                  turbine_efficiency=DEFAULT_TURBINE_EFFICIENCY):
    """Electrical power harvested, in watts.

    vehicle_kmh:        road speed of the car
    headwind_kmh:       opposing wind (positive = headwind, negative = tailwind)
    turbine_area:       swept area, m^2 (scales harvest linearly)
    turbine_efficiency: turbine/generator efficiency (scales harvest linearly)
    """
    v_rel = _ms(vehicle_kmh) + _ms(headwind_kmh)
    if v_rel <= 0:
        return 0.0
    area_scale = turbine_area / DEFAULT_TURBINE_AREA
    eff_scale = turbine_efficiency / DEFAULT_TURBINE_EFFICIENCY
    return HARVEST_COEFF * area_scale * eff_scale * v_rel ** HARVEST_EXPONENT


def drag_penalty(vehicle_kmh, headwind_kmh,
                 turbine_area=DEFAULT_TURBINE_AREA):
    """Electrical drag penalty, in watts, charged through the 90%-efficient
    drivetrain. Zero when the car is parked, whatever the wind."""
    v = _ms(vehicle_kmh)
    if v <= 0:
        return 0.0
    v_rel = v + _ms(headwind_kmh)
    if v_rel <= 0:
        return 0.0
    area_scale = turbine_area / DEFAULT_TURBINE_AREA
    drag_force = 0.5 * RHO * (DRAG_AREA * area_scale) * v_rel ** 2
    return drag_force * v / MOTOR_EFFICIENCY


def net_power(vehicle_kmh, headwind_kmh, **kwargs):
    """Harvest minus drag penalty, in watts. Negative means the turbines
    cost the car more than they return."""
    return (harvest_power(vehicle_kmh, headwind_kmh, **kwargs)
            - drag_penalty(vehicle_kmh, headwind_kmh,
                           turbine_area=kwargs.get("turbine_area",
                                                    DEFAULT_TURBINE_AREA)))


def break_even_headwind(vehicle_kmh, lo=0.0, hi=250.0, tol=0.05):
    """Headwind (km/h) at which net power crosses zero for a given road
    speed, found by bisection. Returns None if the car is parked (no
    penalty to break even against) or no crossing exists in range."""
    if vehicle_kmh <= 0:
        return None
    if net_power(vehicle_kmh, lo) >= 0:
        return lo
    if net_power(vehicle_kmh, hi) < 0:
        return None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if net_power(vehicle_kmh, mid) >= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def _case(vehicle_kmh, headwind_kmh, label):
    h = harvest_power(vehicle_kmh, headwind_kmh)
    p = drag_penalty(vehicle_kmh, headwind_kmh)
    print(f"{label}")
    print(f"  vehicle {vehicle_kmh:6.1f} km/h | headwind {headwind_kmh:6.1f} km/h")
    print(f"  harvest       {h:8.0f} W  ({h/1000:.2f} kW)")
    print(f"  drag penalty  {p:8.0f} W  ({p/1000:.2f} kW)")
    print(f"  NET           {h-p:+8.0f} W")
    return h, p, h - p


def main():
    print("=" * 64)
    print("CLEAN ENERGY AUTOMOBILES — WIND-HARVEST MODEL (calibrated POC)")
    print("=" * 64)
    print()
    print("--- Default case: highway cruise, calm air ---")
    _case(90, 0, "90 km/h cruise, no wind:")
    print("  -> The drag bill exceeds the harvest. At cruise in calm air")
    print("     the turbines are a net cost — the 'wind' they harvest is")
    print("     mostly wind the car itself created.")
    print()
    print("--- Headwind sweep at 90 km/h cruise ---")
    print(f"  {'headwind':>10} {'harvest':>10} {'penalty':>10} {'net':>10}")
    print(f"  {'(km/h)':>10} {'(W)':>10} {'(W)':>10} {'(W)':>10}")
    for hw in range(0, 101, 10):
        h = harvest_power(90, hw)
        p = drag_penalty(90, hw)
        print(f"  {hw:>10} {h:>10.0f} {p:>10.0f} {h-p:>+10.0f}")
    print()
    be = break_even_headwind(90)
    print(f"--- Break-even at 90 km/h cruise: headwind ≈ {be:.0f} km/h ---")
    print("  Only when the opposing wind reaches that strength does the")
    print("  harvest finally pay its own drag bill.")
    print()
    print("--- Parked in a storm ---")
    _case(0, STORM_WIND_KMH, "Parked, storm wind:")
    print("  -> No road speed, no drag bill: this harvest is genuinely free.")
    print("     Headwind, descents, braking and storm parking are where")
    print("     this idea earns its keep.")


if __name__ == "__main__":
    main()
