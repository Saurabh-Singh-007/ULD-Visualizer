# ULD Packing Visualization 

This Streamlit application allows users to visualize the packing of packages in ULDs (Unit Load Devices) and perform analysis on their arrangement. It reads data from a file, displays 3D visualizations of ULDs with their packages, and provides insights into any overlaps or unassigned packages.


# How to Run  
- Requirements 
```bash
pip install streamlit matplotlib numpy 
```
- Clone this repository to your local machine. 
- Save you data in the format deescribed below as as `.txt` file. 
- Run the streamlit app .
```bash 
streamlit run app.py
```
- Open the app and upload the `.txt` file.


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
- Total cost (an integer value)
- Total number of packages packed in all ULDs
- Number of ULDs with Priority Packages
  
### 4. Package Data:
Next line contains the number of packages .

The subsequent lines contain data about each package in the following format:

```txt
<Package ID>,<ULD ID>,<X0>,<Y0>,<Z0>,<X1>,<Y1>,<Z1>,<Priority> (All separated by commas and NO SPACES)
```

Where:
- **Package ID**: A unique identifier for the package (e.g., `PKG1`).
- **ULD ID**: The ID of the ULD that the package is assigned to (e.g., `ULD1`, `NONE` if the package is not assigned to any ULD).
- **Coordinates (X0, Y0, Z0, X1, Y1, Z1)**: The 3D coordinates defining the package's box. `(X0, Y0, Z0)` is the lower-left-front corner and `(X1, Y1, Z1)` is the upper-right-back corner.
- **Priority**: The priority of the package. It can be:
  - `P` for **priority** packages (highlighted in the visualization).
  - `E` for **economy** packages.
 
# Sample Packing Data File

Here is a sample `sample_input.txt` file structure that can be uploaded for analysis:

```txt
3
120,100,100
150,150,150
100,100,100
1500,10,2
27
PKG1,ULD1,0,0,0,30,30,30,P
PKG2,ULD1,35,0,0,65,30,30,E
PKG3,ULD1,70,0,0,100,30,30,P
PKG4,ULD1,0,35,0,30,65,30,E
PKG5,ULD1,35,35,30,65,65,60,P
PKG6,ULD1,70,35,30,100,65,60,E
PKG7,ULD1,0,70,0,30,100,30,P
PKG8,ULD1,35,70,30,65,100,60,E
PKG9,ULD1,70,70,30,100,100,60,P
PKG10,ULD2,0,0,0,40,40,40,P
PKG11,ULD2,45,0,0,85,40,40,E
PKG12,ULD2,90,0,0,130,40,40,P
PKG13,ULD2,0,45,0,40,85,40,E
PKG14,ULD2,45,45,40,85,85,80,P
PKG15,ULD2,90,45,40,130,85,80,E
PKG16,ULD2,0,90,0,40,130,40,P
PKG17,ULD2,45,90,40,85,130,80,E
PKG18,ULD3,0,0,0,25,25,25,P
PKG19,ULD3,30,0,0,55,25,25,E
PKG20,ULD3,60,0,0,85,25,25,P
PKG21,ULD3,0,30,0,25,55,25,E
PKG22,ULD3,30,30,25,55,55,50,P
PKG23,ULD3,60,30,25,85,55,50,E
PKG24,ULD3,0,60,0,25,85,25,P
PKG25,ULD3,30,60,25,55,85,50,E
PKG26,NONE,0,0,0,40,40,40,E
PKG27,NONE,40,0,40,80,40,80,E
```
### Notes:
- **Priority Package (P)**: Packages marked with a priority (`P`) will be visually highlighted in the app.
- **Unassigned Package (NONE)**: Packages that are not assigned to any ULD are marked with `NONE`. These are considered unassigned and are not displayed in the 3D visualization, but they will be listed as unassigned economy packages.
- **Package Dimensions**: The dimensions of a package are automatically derived from the coordinates provided in the package data. The dimensions represent the size of the package's box in 3D space.


## Interacting with the App

### 3D Visualization
- Click and drag to rotate the view of the ULD and packages.

### Package Information
- Hover over each package to see its ID.

### Warnings
- Any overlap between packages will be displayed as a warning.
- Unassigned economy packages will be listed separately.

### Output
Upon successful execution, the app will display:
- A 3D visualization of the ULDs and packages.
- Details on the number of packages, ULD dimensions, total volume, and any overlap warnings.
- A list of unassigned economy packages if applicable.

## Troubleshooting

### File Format Issues
- Ensure that the file follows the correct structure, with each section properly formatted.

### Missing Dependencies
- If you encounter errors related to missing packages, make sure to install the required dependencies: 
    - `streamlit`
    - `matplotlib`
    - `numpy`

## Package Overlap
- The application will notify you if there are any overlapping packages within a ULD.
