import math


def calculate_flow(density, viscosity, diameter_mm, length, flow_lps):
    """Calculate velocity, Reynolds number, friction factor and pressure drop."""
    diameter = diameter_mm / 1000
    flow_rate = flow_lps / 1000
    area = math.pi * diameter**2 / 4
    velocity = flow_rate / area
    reynolds = density * velocity * diameter / viscosity

    if reynolds < 2300:
        friction_factor = 64 / reynolds
        flow_regime = "Laminar"
    else:
        friction_factor = 0.3164 / reynolds**0.25
        flow_regime = "Turbulent"

    pressure_drop = friction_factor * (length / diameter) * (density * velocity**2 / 2)
    return velocity, reynolds, friction_factor, pressure_drop, flow_regime
