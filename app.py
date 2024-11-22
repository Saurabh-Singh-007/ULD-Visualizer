import streamlit as st
import plotly.graph_objects as go
import numpy as np

def read_packing_data_v2(file_content):
    lines = file_content.splitlines()
    
    uld_count = int(lines[0].strip())
    uld_dimensions = []
    for i in range(1, 1 + uld_count):
        uld_dimensions.append(list(map(int, lines[i].strip().split(','))))
    
    total_cost, total_packages, priority_ulds = map(int, lines[1 + uld_count].strip().split(','))
    
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
import plotly.colors as pc  



def analyze_packing(packages, uld_dimensions):
    st.write("### Packing Analysis")
    uld_ids = sorted(set(package['uld_id'] for package in packages if package['uld_id'] != 'NONE'))
    
    for uld_id in uld_ids:
        uld_packages = [p for p in packages if p['uld_id'] == uld_id]
        uld_index = int(uld_id[3:]) - 1  
        uld_dim = uld_dimensions[uld_index]  
        
        st.write(f"#### {uld_id}")
        st.write(f"- Number of packages: {len(uld_packages)}")
        st.write(f"- ULD Dimensions: {uld_dim}")
        st.write(f"- Total volume: {np.prod(uld_dim):.2f} cubic units")
        
        overlaps = check_overlap(uld_packages)
        if overlaps:
            st.warning(f"Overlaps detected in {uld_id}:")
            for warning in overlaps:
                st.write(f"- {warning}")
        else:
            st.success(f"No overlaps detected in {uld_id}.")
        
        st.write("- **Packages:**")
        for package in uld_packages:
            coords = package['coords']
            size = [coords[3] - coords[0], coords[4] - coords[1], coords[5] - coords[2]]
            priority = package['priority']
            priority_label = " (Priority)" if priority == 'P' else ""
            st.write(f"  - {package['package_id']}: Size {size}{priority_label}")

            
def calculate_layers(packages):
    """
    Calculate the layer number for each package based on support.
    Layer 1: Packages directly on the ULD floor.
    Subsequent layers: Packages supported by the layer below.
    """
    layer_map = {}  # Maps package_id to its layer
    packages_sorted = sorted(packages, key=lambda p: p['coords'][2])  # Sort by z0 (bottom height)

    for package in packages_sorted:
        x0, y0, z0, x1, y1, z1 = package['coords']
        # Check for packages below this one to determine the layer
        supported_layer = 0
        for other in packages_sorted:
            ox0, oy0, oz0, ox1, oy1, oz1 = other['coords']
            # Check if 'other' is directly below 'package'
            if oz1 == z0 and not (ox1 <= x0 or ox0 >= x1 or oy1 <= y0 or oy0 >= y1):  # Overlapping base
                supported_layer = max(supported_layer, layer_map[other['package_id']])

        # Layer is the maximum supported layer + 1
        layer_map[package['package_id']] = supported_layer + 1

    return layer_map



def visualize_all_layers(packages, uld_dimensions, selected_uld=None, selected_layer=None, layer_map=None):
    """
    Visualize all packages for all ULDs or a specific ULD and optionally highlight a specific layer.
    """
    fig = go.Figure()

    if selected_uld:
        uld_packages = [p for p in packages if p['uld_id'] == selected_uld]
        uld_ids = [selected_uld]
    else:
        uld_packages = packages
        uld_ids = sorted(set(p['uld_id'] for p in packages if p['uld_id'] != 'NONE'))

    for uld_id in uld_ids:
        uld_index = int(uld_id[3:]) - 1  
        dimensions = uld_dimensions[uld_index]
        uld_color = "rgba(200,200,200,0.2)" 

        x0, y0, z0 = 0, 0, 0
        x1, y1, z1 = dimensions
        fig.add_trace(go.Mesh3d(
            x=[x0, x1, x1, x0, x0, x1, x1, x0],
            y=[y0, y0, y1, y1, y0, y0, y1, y1],
            z=[z0, z0, z0, z0, z1, z1, z1, z1],
            color=uld_color,
            opacity=0.2,
            hoverinfo='skip',
            name=f"{uld_id} Boundary"
        ))

    color_palette = pc.qualitative.Set3  
    for i, package in enumerate(uld_packages):
        coords = package['coords']
        package_id = package['package_id']
        priority = package['priority']
        layer = layer_map[package_id] if layer_map else None

        x0, y0, z0, x1, y1, z1 = coords
        vertices = np.array([
            [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],  
            [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]   
        ])
        faces = np.array([
            [0, 1, 2], [0, 2, 3],  
            [4, 5, 6], [4, 6, 7],  
            [0, 1, 5], [0, 5, 4], 
            [2, 3, 7], [2, 7, 6],  
            [1, 2, 6], [1, 6, 5],  
            [0, 3, 7], [0, 7, 4] 
        ])

        if selected_layer is not None and layer == selected_layer:
            box_color = pc.qualitative.Plotly[i % len(pc.qualitative.Plotly)]
            box_opacity = 1.0  # Fully opaque for highlighted packages
        elif selected_layer is None:
            box_color = pc.qualitative.Plotly[i % len(pc.qualitative.Plotly)]
            box_opacity = 0.7  # Uniform visibility for all packages
        else:
            box_color = "rgba(200,200,200,0.5)"  # Gray for non-highlighted packages
            box_opacity = 0.5  # Semi-transparent for non-highlighted packages

        fig.add_trace(go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            color=box_color,
            opacity=box_opacity,
            name=f"{package_id} (Layer {layer})" if layer_map else package_id,
            hovertext=f"Package ID: {package_id}<br>Priority: {'Yes' if priority == 'P' else 'No'}<br>Layer: {layer}" if layer_map else f"Package ID: {package_id}<br>Priority: {'Yes' if priority == 'P' else 'No'}",
            hoverinfo='text'
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z')
        ),
        title="ULD Visualization" if selected_uld is None else f"{selected_uld} Visualization",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    st.plotly_chart(fig)


st.title("ULD Packing Visualization and Analysis")

uploaded_file = st.file_uploader("Upload a Packing Data File", type="txt")

if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")
    packages, uld_dimensions = read_packing_data_v2(file_content)

    layer_map = calculate_layers(packages)

    uld_ids = sorted(set(p['uld_id'] for p in packages if p['uld_id'] != 'NONE'))
    selected_uld = st.selectbox("Select ULD", uld_ids)

    if selected_uld:
        available_layers = ["None Highlighted"] + sorted(set(layer_map[p['package_id']] for p in packages if p['uld_id'] == selected_uld))
    else:
        available_layers = ["None Highlighted"] + sorted(set(layer_map[p['package_id']] for p in packages))

    selected_layer = st.selectbox("Select Layer to Highlight", available_layers)

    if selected_layer == "None Highlighted":
        selected_layer = None
    else:
        selected_layer = int(selected_layer)

    visualize_all_layers(packages, uld_dimensions, selected_uld, selected_layer, layer_map)
else:
    st.write("Please upload a packing data file to analyze and visualize.")

