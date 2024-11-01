# Beam-Analysis-Tool
This project is a Python tool for analyzing beam design under various load conditions. It calculates key structural properties like shear force, bending moment, and deflection for a given beam, and visualizes the results. The results are also saved to a downloadable file for further review.

**Features**

Beam Properties Calculation: Calculates section modulus, moment of inertia, cross-sectional area, and shear area based on input dimensions.
Load Analysis: Handles multiple load types (point loads, uniformly distributed loads, and uniformly varying loads).
Safety Checks: Computes design bending and shear strengths using partial safety factors and material properties.
Deflection Calculation: Computes slope and deflection at various points along the beam.
Visualization: Plots shear force, bending moment, and deflection along the beam length.
File Output: Saves key results, such as span, maximum moment, maximum shear, section modulus, and moment of inertia to a text file.

**Requirements**

Python 3.6+
sympy for symbolic mathematics
numpy for numerical operations
matplotlib for plotting graphs
math for mathematical functions
google.colab for file handling (for download in Colab)

**Installation**
**Copy code**

git clone https://github.com/shubarya2912/beam-analysis-tool.git
cd beam-analysis-tool

**Usage**
Run the script:
python beam_analysis.py

**Enter beam properties:**
Provide beam length, width, depth, and web thickness as prompted.

**Specify load cases:**
You can add uniformly distributed loads, point loads, and uniformly varying loads.
Enter the required details for each load type.

**View and download results:**
The program displays shear, moment, and deflection values at various intervals.
The results are saved in beam_design_input.txt, which can be downloaded if using Google Colab.
Plot graphs:
Graphs of shear force, bending moment, and deflection are displayed after calculations.

**Example Output**
Sample output for each interval:
Copy code
At x = 0.0 m: Shear Force = 2000 N, Bending Moment = 1500 Nm, Deflection = 0.01 m
...

**Files**
beam_design_input.txt: Contains beam properties, maximum shear, maximum moment, yield strength, section modulus, and moment of inertia.

**License**
None

**Acknowledgments**
Developed with sympy, numpy, and matplotlib.
