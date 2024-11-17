# ULD Packing Visualization and Analysis

This Streamlit application allows users to visualize the packing of packages in ULDs (Unit Load Devices) and perform analysis on their arrangement. It reads data from a file, displays 3D visualizations of ULDs with their packages, and provides insights into any overlaps or unassigned packages.

## Features

- **3D Visualization**: Displays ULDs and their packed packages in a 3D space.
- **Package Priority Highlighting**: Priority packages (marked with 'P') are highlighted in red.
- **Overlap Detection**: Identifies and warns if any packages overlap within a ULD.
- **Unassigned Economy Packages**: Marks economy packages not assigned to any ULD.
- **Package Information**: Provides details such as package size, ULD assignment, and priority.

## How It Works

The application parses a text file with specific format requirements and visualizes the packing of the packages inside ULDs. The file contains:
- ULD count and their dimensions.
- Information on the number of packages, their dimensions, priority, and ULD assignments.
- A 3D visualization of each ULD and the packages inside it.

## ULD Packing Data File Format

This document describes the structure and contents of the packing data file used in the ULD packing visualization and analysis app.

### File Structure Overview:
The file consists of several sections, each containing specific data about ULDs and packages. The format is plain text, and each line in the file represents a distinct piece of information.

### 1. Number of ULDs:
The first line contains an integer that specifies the number of ULDs.

### 2. ULD Dimensions:
The next N lines (where N is the number of ULDs) contain the dimensions of each ULD. Each line should list the length, width, and height of the ULD, separated by commas.

### 3. Total Number of Packages, ULDs, and Priority ULDs:
The line after the ULD dimensions contains three integers:
- Total number of packages in the system.
- Total number of ULDs.
- Number of priority ULDs (used for validation).

### 4. Package Data:
The subsequent lines contain data about each package in the following format:

`
<Package ID>,<ULD ID>,<X0>,<Y0>,<Z0>,<X1>,<Y1>,<Z1>,<Priority>
`

Where:
- **Package ID**: A unique identifier for the package (e.g., `PKG1`).
- **ULD ID**: The ID of the ULD that the package is assigned to (e.g., `ULD1`, `NONE` if the package is not assigned to any ULD).
- **Coordinates (X0, Y0, Z0, X1, Y1, Z1)**: The 3D coordinates defining the package's box. `(X0, Y0, Z0)` is the lower-left-front corner and `(X1, Y1, Z1)` is the upper-right-back corner.
- **Priority**: The priority of the package. It can be:
  - `P` for **priority** packages (highlighted in the visualization).
  - `E` for **economy** packages.
### Notes:
- **Priority Package (P)**: Packages marked with a priority (`P`) will be visually highlighted in the app.
- **Unassigned Package (NONE)**: Packages that are not assigned to any ULD are marked with `NONE`. These are considered unassigned and are not displayed in the 3D visualization, but they will be listed as unassigned economy packages.
- **Package Dimensions**: The dimensions of a package are automatically derived from the coordinates provided in the package data. The dimensions represent the size of the package's box in 3D space.

# How to Run  
- Requirements 
```bash
pip install streamlit matplotlib numpy 
```
- Clone this repository to your local machine. 
- Save you data in the format deescribed above as as `.txt` file. 
- Run the streamlit app .
```bash 
streamlit run app.py
```
- Open the app and upload the `.txt` file.

# Interacting with the App

## 3D Visualization
- Click and drag to rotate the view of the ULD and packages.

## Package Information
- Hover over each package to see its ID.

## Warnings
- Any overlap between packages will be displayed as a warning.
- Unassigned economy packages will be listed separately.

# Example Output
Upon successful execution, the app will display:
- A 3D visualization of the ULDs and packages.
- Details on the number of packages, ULD dimensions, total volume, and any overlap warnings.
- A list of unassigned economy packages if applicable.

# Troubleshooting

## File Format Issues
- Ensure that the file follows the correct structure, with each section properly formatted.

## Missing Dependencies
- If you encounter errors related to missing packages, make sure to install the required dependencies: 
    - `streamlit`
    - `matplotlib`
    - `numpy`

## Package Overlap
- The application will notify you if there are any overlapping packages within a ULD.
