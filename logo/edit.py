"""
SVG Circle Generator
Generate SVG files with circles based on input specifications.
"""

def generate_corner_circles(circles, grid_size, radius_factor=1.5):
    """
    Generate smaller circles at the corners around each input circle.
    
    For each circle, creates 4 smaller circles (1/3 radius) positioned at the corners:
    - Top-left: (cx - grid_size/2, cy - grid_size/2)
    - Top-right: (cx + grid_size/2, cy - grid_size/2)
    - Bottom-left: (cx - grid_size/2, cy + grid_size/2)
    - Bottom-right: (cx + grid_size/2, cy + grid_size/2)
    
    If multiple circles overlap at the same position, keeps only the largest one.
    
    Args:
        circles: List of dictionaries with 'cx', 'cy', 'r' keys
        grid_size: Distance between circle centers
        
    Returns:
        List of new circles (dictionaries with 'cx', 'cy', 'r' keys)
    
    Example:
        original = [
            {'cx': 0, 'cy': 0, 'r': 60},
            {'cx': 10, 'cy': 0, 'r': 60}
        ]
        new_circles = generate_corner_circles(original, grid_size=10)
    """
    new_circles = {}  # Use dict with (cx, cy) as key to handle overlaps
    offset = grid_size / 2
    
    # Define the four corner offsets
    corners = [
        (-offset, -offset),  # Top-left
        (offset, -offset),   # Top-right
        (-offset, offset),   # Bottom-left
        (offset, offset)     # Bottom-right
    ]
    
    for circle in circles:
        cx = circle['cx']
        cy = circle['cy']
        r = circle['r']
        new_r = r / radius_factor
        
        # Create circles at each corner
        for dx, dy in corners:
            new_cx = cx + dx
            new_cy = cy + dy
            position = (new_cx, new_cy)
            
            # Preserve any additional properties from the original circle
            new_circle = {
                'cx': new_cx,
                'cy': new_cy,
                'r': new_r
            }
            
            # Copy optional properties if they exist
            if 'fill' in circle:
                new_circle['fill'] = circle['fill']
            if 'stroke' in circle:
                new_circle['stroke'] = circle['stroke']
            if 'stroke_width' in circle:
                new_circle['stroke_width'] = circle['stroke_width']
            
            # If position already exists, keep the larger circle
            if position in new_circles:
                if new_r > new_circles[position]['r']:
                    new_circles[position] = new_circle
            else:
                new_circles[position] = new_circle
    
    return list(new_circles.values())


def generate_svg_circles(circles, width=800, height=600, output_file="circles.svg"):
    """
    Generate an SVG file with circles.
    
    Args:
        circles: List of dictionaries with keys 'cx', 'cy', 'r', and optionally 'fill', 'stroke', 'stroke_width'
        width: SVG canvas width
        height: SVG canvas height
        output_file: Output SVG file path
    
    Example:
        circles = [
            {'cx': 100, 'cy': 100, 'r': 50, 'fill': 'red'},
            {'cx': 200, 'cy': 150, 'r': 30, 'fill': 'blue', 'stroke': 'black', 'stroke_width': 2}
        ]
        generate_svg_circles(circles, output_file="my_circles.svg")
    """
    # Remove duplicates - keep the largest circle at each position
    unique_circles = {}
    for circle in circles:
        position = (circle['cx'], circle['cy'])
        if position in unique_circles:
            # Keep the larger circle
            if circle['r'] > unique_circles[position]['r']:
                unique_circles[position] = circle
        else:
            unique_circles[position] = circle
    
    circles = list(unique_circles.values())
    svg_parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    ]
    
    for circle in circles:
        cx = circle['cx']
        cy = circle['cy']
        r = circle['r']
        fill = circle.get('fill', 'black')
        stroke = circle.get('stroke', 'none')
        stroke_width = circle.get('stroke_width', 1)
        
        circle_tag = f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'
        svg_parts.append(circle_tag)
    
    svg_parts.append('</svg>')
    
    svg_content = '\n'.join(svg_parts)
    
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"SVG file generated: {output_file}")


if __name__ == "__main__":
    # Example usage
    circles = [
        # T top
        {'cx': 30, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 40, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 50, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 60, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 70, 'cy': 30, 'r': 4, 'fill': 'black'},
        
        # T vertical bar
        {'cx': 50, 'cy': 40, 'r': 4, 'fill': 'black'},
        {'cx': 50, 'cy': 50, 'r': 4, 'fill': 'black'},
        {'cx': 50, 'cy': 60, 'r': 4, 'fill': 'black'},
        {'cx': 50, 'cy': 70, 'r': 4, 'fill': 'black'},
        {'cx': 50, 'cy': 80, 'r': 4, 'fill': 'black'},
        
        # D vertical bar
        {'cx': 90, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 90, 'cy': 40, 'r': 4, 'fill': 'black'},
        {'cx': 90, 'cy': 50, 'r': 4, 'fill': 'black'},
        {'cx': 90, 'cy': 60, 'r': 4, 'fill': 'black'},
        {'cx': 90, 'cy': 70, 'r': 4, 'fill': 'black'},
        {'cx': 90, 'cy': 80, 'r': 4, 'fill': 'black'},
        
        # D round
        {'cx': 100, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 110, 'cy': 30, 'r': 4, 'fill': 'black'},
        {'cx': 120, 'cy': 40, 'r': 4, 'fill': 'black'},
        {'cx': 120, 'cy': 50, 'r': 4, 'fill': 'black'},
        {'cx': 120, 'cy': 60, 'r': 4, 'fill': 'black'},
        {'cx': 120, 'cy': 70, 'r': 4, 'fill': 'black'},
        {'cx': 110, 'cy': 80, 'r': 4, 'fill': 'black'},
        {'cx': 100, 'cy': 80, 'r': 4, 'fill': 'black'},
    ]

    # generate_svg_circles(example_circles, width=800, height=600, output_file="circles.svg")
    
    # Generate corner circles with grid size of 100
    corner_circles = generate_corner_circles(circles, grid_size=10, radius_factor = 1.4)
    more_corners = generate_corner_circles(corner_circles, grid_size=10, radius_factor = 1.3)
    more_more = generate_corner_circles(more_corners, grid_size=10, radius_factor=1.7)
    # print(f"Generated {len(corner_circles)} corner circles (duplicates removed)")

    generate_svg_circles(circles + corner_circles + more_corners + more_more, width=200, height=100, output_file="circles.svg")
    
