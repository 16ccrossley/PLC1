import streamlit as st
import math

# Define material properties
materials = {
    "ABS": {"eta0": 3000, "b": 0.02, "T_ref": 230},
    "PP": {"eta0": 1000, "b": 0.018, "T_ref": 190},
    "PE": {"eta0": 800, "b": 0.015, "T_ref": 160},
}

# Function to calculate viscosity at a given temperature
def calc_viscosity(material, T_melt):
    eta0 = materials[material]["eta0"]
    b = materials[material]["b"]
    T_ref = materials[material]["T_ref"]
    eta = eta0 * math.exp(-b * (T_melt - T_ref))
    return eta

# Function to calculate pressure loss using Hagen–Poiseuille's equation
def calc_pressure_loss(viscosity, length, diameter, flow_rate):
    radius = diameter / 2
    pressure_loss = (8 * viscosity * length * flow_rate) / (math.pi * radius**4)
    return pressure_loss

# Function to calculate flow rate
def calc_flow_rate(injection_speed, diameter):
    area = math.pi * (diameter / 2)**2
    flow_rate = area * injection_speed
    return flow_rate

# Streamlit app layout
st.title("Hot Runner Pressure Loss Calculator")

# User input for the parameters
material = st.selectbox("Select Material", ["ABS", "PP", "PE"])
T_melt = st.slider("Melt Temperature (°C)", 150, 300, 240)
nozzle_diameter = st.number_input("Nozzle Flow Bore Diameter (mm)", min_value=1.0, max_value=10.0, value=5.0)
injection_speed = st.number_input("Injection Speed (mm/s)", min_value=1.0, max_value=500.0, value=100.0)
shot_weight = st.number_input("Shot Weight (grams)", min_value=1.0, value=50.0)
gate_diameter = st.number_input("Gate Diameter (mm)", min_value=0.1, max_value=10.0, value=2.0)
nozzle_length = st.number_input("Nozzle Length (mm)", min_value=1.0, max_value=500.0, value=50.0)
mold_temperature = st.slider("Mold Temperature (°C)", 50, 200, 180)
cycle_time = st.number_input("Cycle Time (seconds)", min_value=1.0, value=30.0)

# Convert mm to meters for calculations
nozzle_diameter_m = nozzle_diameter / 1000
gate_diameter_m = gate_diameter / 1000
nozzle_length_m = nozzle_length / 1000

# Step 1: Calculate viscosity
viscosity = calc_viscosity(material, T_melt)

# Step 2: Calculate flow rate
flow_rate = calc_flow_rate(injection_speed, nozzle_diameter_m)

# Step 3: Calculate pressure loss for the nozzle
pressure_loss_nozzle = calc_pressure_loss(viscosity, nozzle_length_m, nozzle_diameter_m, flow_rate)

# Step 4: Calculate pressure loss for the gate
pressure_loss_gate = calc_pressure_loss(viscosity, nozzle_length_m, gate_diameter_m, flow_rate)

# Step 5: Calculate total pressure loss
total_pressure_loss = pressure_loss_nozzle + pressure_loss_gate

# Display the results
st.subheader("Results")
st.write(f"Viscosity at Melt Temperature: {viscosity:.2f} Pa·s")
st.write(f"Flow Rate: {flow_rate:.6f} m³/s")
st.write(f"Pressure Loss in Nozzle: {pressure_loss_nozzle:.2f} Pa")
st.write(f"Pressure Loss in Gate: {pressure_loss_gate:.2f} Pa")
st.write(f"Total Pressure Loss: {total_pressure_loss:.2f} Pa")
