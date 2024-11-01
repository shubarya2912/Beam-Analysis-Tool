# -*- coding: utf-8 -*-
"""Beam_analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y9R941VcYfqKe_uAyxlSBt4ImvI88L34

**Program for Finding Bending Moment , Shear force and Deflection Along with BMD and SFD **
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import math
from google.colab import files

# Define constants and position variable
x = sp.Symbol('x', real=True)
E = 200 * 10**9  # Modulus of Elasticity for steel in Pa (200 GPa)
yield_stress = 250 * 10**6  # Yield strength in Pa (example: 250 MPa for steel)
gamma_m0 = 1.5  # Partial safety factor for bending and shear
beta_b = 1.0  # Bending capacity reduction factor (example)

# Beam properties input
def get_beam_properties():
    L = float(input("Enter the total length of the beam (m): "))
    b = float(input("Enter the width of the beam (m): "))
    d = float(input("Enter the depth of the beam (m): "))
    tw = float(input("Enter the thickness of the web (m): "))
    return L, b, d, tw

# Section properties
def calculate_section_properties(b, d, tw):
    Z = (b * d**2) / 6  # Elastic section modulus (m^3)
    Av = b * tw  # Shear area of web (m^2)
    I = (b * d**3) / 12  # Moment of inertia (m^4)
    A = b * d  # Cross-sectional area (m^2)
    return Z, Av, I, A

# Calculate design strength (not used for checks)
def calculate_design_strength(Z, Av):
    M_d = beta_b * Z * yield_stress / gamma_m0  # Design bending strength
    V_d = (Av * yield_stress) / (math.sqrt(3) * gamma_m0)  # Design shear strength
    return M_d, V_d

# Calculate deflection
def calculate_deflection(M, E, I, x_val, L):
    slope = sp.integrate(M / (E * I), x)
    deflection = sp.integrate(slope, x)
    C1 = -deflection.subs(x, L) / L
    deflection = deflection + C1 * x
    return deflection.subs(x, x_val)

# Load case input
def get_load_cases():
    point_loads = []
    udls = []
    uvls = []

    while True:
        print("\nSelect the load case:")
        print("1. Add Uniformly Distributed Load (UDL)")
        print("2. Add Point Load")
        print("3. Add Uniformly Varying Load (UVL)")
        print("4. Done with Loadings")
        load_case = int(input("Enter the load case number (1-3 for load types, 4 to finish): "))

        if load_case == 1:
            w = float(input("Enter UDL intensity (N/m): "))
            a = float(input("Enter start position of UDL (m): "))
            b = float(input("Enter end position of UDL (m): "))
            udls.append((w, a, b))
        elif load_case == 2:
            P = float(input("Enter point load value (N): "))
            x_pos = float(input("Enter position of point load from left support (m): "))
            point_loads.append((P, x_pos))
        elif load_case == 3:
            q = float(input("Enter maximum intensity of UVL (N/m): "))
            m = float(input("Position of maximum intensity (m): "))
            n = float(input("Position of minimum intensity (0) (m): "))
            uvls.append((q, m, n))
        elif load_case == 4:
            print("Load entry complete.")
            break
        else:
            print("Invalid input. Please enter a valid load case number.")

    return point_loads, udls, uvls

# Calculate results for each case based on loads entered
def calculate_case_values(x_val, point_loads, udls, uvls, L, E, I):
    RL, RR, V, M = 0, 0, 0, 0

    for w, a, b in udls:
        RL += w * (b - a) / 2
        RR += w * (b - a) / 2
        V += RL - w * sp.Max(0, x - a)
        M += RL * x - w * sp.Max(0, x - a)**2 / 2

    if point_loads:
        total_moment = sum(P * xi for P, xi in point_loads)
        RL += total_moment / L
        RR += sum(P for P, _ in point_loads) - RL
        V += RL
        M += RL * x
        for P, xi in point_loads:
            V -= P * sp.Max(0, x - xi)
            M -= P * sp.Max(0, x - xi)

    for q, m, n in uvls:
        RL += 0.5 * (n - m) * q
        RR += RL
        V += RL - 0.5 * q * (sp.Max(0, x - m)**2 / (n - m))
        M += RL * x - (q * (sp.Max(0, x - m)**3) / (6 * (n - m)))

    deflection = calculate_deflection(M, E, I, x_val, L)
    return V.subs(x, x_val), M.subs(x, x_val), deflection

# Writing to file
def write_to_file(filename, L, max_shear, max_moment, yield_stress, section_properties):
    Z, I, A = section_properties

    with open(filename, 'w') as file:
        file.write(f"Span: {L} m\n")
        file.write(f"Moment: {max_moment / 1000} kNm\n")  # Convert Nm to kNm
        file.write(f"Shear Force: {max_shear / 1000} kN\n")  # Convert N to kN
        file.write(f"Yield Strength: {yield_stress / 10**6} MPa\n")  # Convert Pa to MPa
        file.write(f"Section Modulus (Z): {Z * 10**9} mm^3\n")  # Convert m^3 to mm^3
        file.write(f"Moment of Inertia (I): {I * 10**12} mm^4\n")  # Convert m^4 to mm^4
        file.write(f"Cross-sectional Area (A): {A * 10**6} mm^2\n")  # Convert m^2 to mm^2

    print(f"Results saved to {filename}")

# Main function
def main():
    L, b, d, tw = get_beam_properties()
    Z, Av, I, A = calculate_section_properties(b, d, tw)
    M_d, V_d = calculate_design_strength(Z, Av)

    point_loads, udls, uvls = get_load_cases()
    intervals = np.arange(0, L + 0.5, 0.5)
    shear_values, moment_values, deflection_values = [], [], []

    print("\nResults at each interval:")
    for x_val in intervals:
        V, M, deflection = calculate_case_values(x_val, point_loads, udls, uvls, L, E, I)
        shear_values.append(float(V))
        moment_values.append(float(M))
        deflection_values.append(float(deflection))
        print(f"At x = {x_val} m: Shear Force = {float(V)} N, Bending Moment = {float(M)} Nm, Deflection = {float(deflection)} m")

    max_shear = max(shear_values)
    max_moment = max(moment_values)

    # Write results to a specified file
    output_filename = "beam_design_input.txt"
    write_to_file(output_filename, L, max_shear, max_moment, yield_stress, (Z, I, A))

    # Download the file
    files.download(output_filename)

    # Plotting results
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(intervals, shear_values, label="Shear Force (V)", color='blue')
    plt.xlabel("Length (m)")
    plt.ylabel("Shear Force (N)")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(intervals, moment_values, label="Bending Moment (M)", color='green')
    plt.xlabel("Length (m)")
    plt.ylabel("Bending Moment (Nm)")
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(intervals, deflection_values, label="Deflection (v)", color='red')
    plt.xlabel("Length (m)")
    plt.ylabel("Deflection (m)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
