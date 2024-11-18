import streamlit as st
import plotly.graph_objects as go
import numpy as np

def read_packing_data_v2(file_content):
    lines = file_content.splitlines()
    
    # Read ULD count and dimensions
    uld_count = int(lines[0].strip())
    uld_dimensions = []
    for i in range(1, 1 + uld_count):
        uld_dimensions.append(list(map(int, lines[i].strip().split(','))))
    
    # Read cost, total packages, and priority ULDs
    total_cost, total_packages, priority_ulds = map(int, lines[1 + uld_count].strip().split(','))
    
    # Read package data
    package_count = int(lines[2 + uld_count].strip())
    packages = []
    for i in range(3 + uld_count, 3 + uld_count + package_count):
        data = lines[i].strip().split(',')
        package_id, uld_id, *coords, priority = data
        coords = list(map(float, coords))
        packages.append({
            'package_id': package_id,
            'uld_id': uld_id,
            'coords': coords,
            'priority': priority
        })
        
        # Check if a priority package is unassigned
        if priority == 'P' and uld_id == 'NONE':
            raise ValueError(f"Priority package {package_id} is not assigned to a ULD.")
    
    return packages, uld_dimensions

def check_overlap(packages):
    overlap_warnings = []
    for i in range(len(packages)):
        for j in range(i + 1, len(packages)):
            p1 = packages[i]
            p2 = packages[j]

            # Extract coordinates for both packages
            x0_1, y0_1, z0_1, x1_1, y1_1, z1_1 = p1['coords']
            x0_2, y0_2, z0_2, x1_2, y1_2, z1_2 = p2['coords']

            # Check for overlap in all three dimensions
            if not (x1_1 <= x0_2 or x1_2 <= x0_1 or  # No overlap in X
                    y1_1 <= y0_2 or y1_2 <= y0_1 or  # No overlap in Y
                    z1_1 <= z0_2 or z1_2 <= z0_1):  # No overlap in Z
                overlap_warnings.append(f"Overlap detected between {p1['package_id']} and {p2['package_id']}.")
    
    return overlap_warnings
import plotly.colors as pc  # For color palettes

def visualize_packing(packages, uld_dimensions):
    uld_ids = sorted(set(package['uld_id'] for package in packages if package['uld_id'] != 'NONE'))
    color_palette = pc.qualitative.Set3  # A qualitative palette with diverse colors
    
    for uld_id in uld_ids:
        fig = go.Figure()
        
        # Filter packages for this ULD
        uld_packages = [p for p in packages if p['uld_id'] == uld_id]
        
        # Get dimensions of the ULD
        uld_index = int(uld_id[3:]) - 1  # Extract ULD index (e.g., ULD1 -> 0)
        dimensions = uld_dimensions[uld_index]
        uld_color = "rgba(200,200,200,0.2)"  # Light gray with transparency
        
        # Add ULD boundary as a transparent cuboid
        x0, y0, z0 = 0, 0, 0
        x1, y1, z1 = dimensions
        uld_vertices = np.array([
            [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],  # Bottom face
            [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]   # Top face
        ])
        uld_faces = np.array([
            [0, 1, 2], [0, 2, 3],  # Bottom face
            [4, 5, 6], [4, 6, 7],  # Top face
            [0, 1, 5], [0, 5, 4],  # Front face
            [2, 3, 7], [2, 7, 6],  # Back face
            [1, 2, 6], [1, 6, 5],  # Right face
            [0, 3, 7], [0, 7, 4]   # Left face
        ])
        fig.add_trace(go.Mesh3d(
            x=uld_vertices[:, 0],
            y=uld_vertices[:, 1],
            z=uld_vertices[:, 2],
            i=uld_faces[:, 0],
            j=uld_faces[:, 1],
            k=uld_faces[:, 2],
            color=uld_color,
            opacity=0.2,
            hoverinfo='skip',
            name=f"{uld_id} Boundary"
        ))
        
        # Add packages inside the ULD
        for i, package in enumerate(uld_packages):
            coords = package['coords']
            package_id = package['package_id']
            priority = package['priority']
            
            # Extract coordinates
            x0, y0, z0, x1, y1, z1 = coords
            vertices = np.array([
                [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],  # Bottom face
                [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]   # Top face
            ])
            
            # Define triangular faces for Mesh3d
            faces = np.array([
                [0, 1, 2], [0, 2, 3],  # Bottom face
                [4, 5, 6], [4, 6, 7],  # Top face
                [0, 1, 5], [0, 5, 4],  # Front face
                [2, 3, 7], [2, 7, 6],  # Back face
                [1, 2, 6], [1, 6, 5],  # Right face
                [0, 3, 7], [0, 7, 4]   # Left face
            ])
            
            # Assign a unique color for the package
            color_index = i % len(color_palette)
            box_color = color_palette[color_index]
            
            # Add the package as a solid block (Mesh3d trace)
            fig.add_trace(go.Mesh3d(
                x=vertices[:, 0],
                y=vertices[:, 1],
                z=vertices[:, 2],
                i=faces[:, 0],
                j=faces[:, 1],
                k=faces[:, 2],
                color=box_color,
                opacity=1.0,
                name=package_id,
                hovertext=f"Package ID: {package_id}<br>Priority: {'Yes' if priority == 'P' else 'No'}",
                hoverinfo='text'
            ))
        
        # Set axis limits and labels
        fig.update_layout(
            scene=dict(
                xaxis=dict(range=[0, dimensions[0]], title='X'),
                yaxis=dict(range=[0, dimensions[1]], title='Y'),
                zaxis=dict(range=[0, dimensions[2]], title='Z')
            ),
            title=f"{uld_id} Package Visualization",
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        # Display the figure
        st.plotly_chart(fig)



def analyze_packing(packages, uld_dimensions):
    st.write("### Packing Analysis")
    uld_ids = sorted(set(package['uld_id'] for package in packages if package['uld_id'] != 'NONE'))
    
    for uld_id in uld_ids:
        uld_packages = [p for p in packages if p['uld_id'] == uld_id]
        uld_index = int(uld_id[3:]) - 1  # Extract ULD index (e.g., ULD1 -> 0)
        uld_dim = uld_dimensions[uld_index]  # Get actual ULD dimensions
        
        st.write(f"#### {uld_id}")
        st.write(f"- Number of packages: {len(uld_packages)}")
        st.write(f"- ULD Dimensions: {uld_dim}")
        st.write(f"- Total volume: {np.prod(uld_dim):.2f} cubic units")
        
        # Check for overlaps
        overlaps = check_overlap(uld_packages)
        if overlaps:
            st.warning(f"Overlaps detected in {uld_id}:")
            for warning in overlaps:
                st.write(f"- {warning}")
        else:
            st.success(f"No overlaps detected in {uld_id}.")
        
        # Display package details and highlight priority packages
        st.write("- **Packages:**")
        for package in uld_packages:
            coords = package['coords']
            size = [coords[3] - coords[0], coords[4] - coords[1], coords[5] - coords[2]]
            priority = package['priority']
            priority_label = " (Priority)" if priority == 'P' else ""
            st.write(f"  - {package['package_id']}: Size {size}{priority_label}")


# Streamlit App
st.title("ULD Packing Visualization and Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload a Packing Data File", type="txt")

if uploaded_file is not None:
    # Read and parse the file
    file_content = uploaded_file.getvalue().decode("utf-8")
    packages, uld_dimensions = read_packing_data_v2(file_content)
    
    # Analyze the packing arrangement
    analyze_packing(packages, uld_dimensions)
    
    # Visualize the ULDs
    visualize_packing(packages, uld_dimensions)
else:
    st.write("Please upload a packing data file to analyze and visualize.")