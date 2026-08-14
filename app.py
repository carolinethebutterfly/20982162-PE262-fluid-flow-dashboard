"""
AI DOCUMENTATION
AI tool used: ChatGPT

Key prompts used:
1. Build a simple Streamlit fluid-flow calculator with sidebar inputs for
   density, viscosity, pipe diameter, pipe length and flow rate.
2. Add Darcy-Weisbach calculations, a Pandas results table and a Plotly chart
   showing pressure drop against flow rate.
3. Add input validation so zero or negative values show a warning instead of
   making the app crash.

Most important manual check/fix:
I checked all unit conversions. Pipe diameter is converted from mm to m and
flow rate is converted from L/s to m3/s before the calculations are done.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from calculations import calculate_flow


st.set_page_config(page_title="Fluid Flow Dashboard", page_icon="💧", layout="wide")


st.title("Fluid Flow Engineering Dashboard")
st.subheader("Darcy-Weisbach Pipe Flow Calculator")
st.write(
    "Use the controls in the sidebar to enter the fluid and pipe data. "
    "The app calculates the velocity, Reynolds number, friction factor and pressure drop."
)

with st.sidebar:
    st.header("Input Data")
    density = st.number_input("Fluid density (kg/m³)", value=1000.0, step=10.0)
    viscosity = st.number_input("Dynamic viscosity (Pa·s)", value=0.001, format="%.4f")
    diameter_mm = st.slider("Pipe diameter (mm)", 10, 200, 50)
    length = st.number_input("Pipe length (m)", value=100.0, step=10.0)
    flow_lps = st.slider("Flow rate (L/s)", 0.1, 20.0, 2.0, 0.1)
    chart_points = st.selectbox("Number of chart points", [10, 15, 20, 25], index=1)

inputs = [density, viscosity, diameter_mm, length, flow_lps]

if any(value <= 0 for value in inputs):
    st.warning("All input values must be greater than zero. Please check the sidebar entries.")
else:
    velocity, reynolds, friction, pressure_drop, regime = calculate_flow(
        density, viscosity, diameter_mm, length, flow_lps
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocity", f"{velocity:.3f} m/s")
    col2.metric("Reynolds number", f"{reynolds:,.0f}")
    col3.metric("Friction factor", f"{friction:.4f}")
    col4.metric("Pressure drop", f"{pressure_drop:,.2f} Pa")

    st.write(f"**Flow regime:** {regime}")

    result_table = pd.DataFrame(
        {
            "Parameter": ["Velocity", "Reynolds number", "Friction factor", "Pressure drop"],
            "Value": [velocity, reynolds, friction, pressure_drop],
            "Unit": ["m/s", "-", "-", "Pa"],
        }
    )
    st.subheader("Calculated Results")
    st.dataframe(result_table.style.format({"Value": "{:.4f}"}), use_container_width=True)

    flow_values = [0.1 + i * (20.0 - 0.1) / (chart_points - 1) for i in range(chart_points)]
    chart_rows = []
    for test_flow in flow_values:
        _, test_reynolds, _, test_drop, _ = calculate_flow(
            density, viscosity, diameter_mm, length, test_flow
        )
        chart_rows.append(
            {"Flow rate (L/s)": test_flow, "Pressure drop (Pa)": test_drop,
             "Reynolds number": test_reynolds}
        )

    chart_data = pd.DataFrame(chart_rows)
    figure = px.line(
        chart_data,
        x="Flow rate (L/s)",
        y="Pressure drop (Pa)",
        markers=True,
        title="Pressure Drop Against Flow Rate",
    )
    figure.update_layout(template="plotly_white")
    st.plotly_chart(figure, use_container_width=True)

    with st.expander("Calculation equations"):
        st.latex(r"V = \frac{Q}{A}")
        st.latex(r"Re = \frac{\rho VD}{\mu}")
        st.latex(r"\Delta P = f\frac{L}{D}\frac{\rho V^2}{2}")

st.caption("PE 262 Project 8 | Student ID: 20982162")
