from calculations import calculate_flow


velocity, reynolds, friction, pressure_drop, regime = calculate_flow(
    1000, 0.001, 50, 100, 2
)

assert round(velocity, 4) == 1.0186
assert round(reynolds, 4) == 50929.5818
assert round(friction, 4) == 0.0211
assert round(pressure_drop, 4) == 21852.1493
assert regime == "Turbulent"

print("All calculation checks passed.")
