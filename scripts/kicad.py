import sys
import os
import math

# Add the scripts directory to Python path for exec() context
script_dir = os.path.join(os.getcwd(), 'scripts')
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from truth import truth
import pcbnew

def switch_placement():
    params = truth()
    board = pcbnew.GetBoard()
    
    # Clean up previously auto-generated borders
    for drawing in list(board.GetDrawings()):
        if drawing.GetComment() == "AUTO_GENERATED_BORDER":
            board.Remove(drawing)
    
    # Get parameters
    frame_border = params['FrameBorder'].val
    switch_spacing = params['SwitchSpacing'].val
    diode_offset = 8.0  # mm below switch center
    
    # Column offsets
    col_offsets = [
        params['Col0Offset'].val,
        params['Col1Offset'].val,
        params['Col2Offset'].val,
        params['Col3Offset'].val,
        params['Col4Offset'].val,
        params['Col5Offset'].val,
    ]
    
    # Offset to center design within KiCAD page frame
    kicad_offset_x = 40  # mm
    kicad_offset_y = 120  # mm
    
    # Place main grid switches (SW1-SW18: 3 rows x 6 columns)
    num_cols = 6
    num_rows = 3
    switch_num = 1
    
    for col in range(num_cols):
        for row in range(num_rows):
            # Calculate position in FreeCAD coordinate system
            x = frame_border + col * switch_spacing + kicad_offset_x
            y = frame_border + row * switch_spacing + col_offsets[col]
            
            # Find switch footprint
            sw_ref = f'SW{switch_num}'
            sw = board.FindFootprintByReference(sw_ref)
            
            if sw:
                # Set position (convert mm to KiCAD internal units)
                # Negate y to convert from y-up (FreeCAD) to y-down (KiCAD)
                sw.SetPosition(pcbnew.VECTOR2I(
                    pcbnew.FromMM(x),
                    pcbnew.FromMM(-y + kicad_offset_y)
                ))
                print(f'{sw_ref} placed at ({x:.2f}, {y:.2f}) mm (FreeCAD coords)')
                
                # Place diode directly underneath switch
                d_ref = f'D{switch_num}'
                diode = board.FindFootprintByReference(d_ref)
                if diode:
                    diode.SetPosition(pcbnew.VECTOR2I(
                        pcbnew.FromMM(x),
                        pcbnew.FromMM(-y + kicad_offset_y + diode_offset)
                    ))
                    print(f'{d_ref} placed at ({x:.2f}, {y - diode_offset:.2f}) mm (FreeCAD coords)')
                else:
                    print(f'{d_ref} not found on board')
            else:
                print(f'{sw_ref} not found on board')
            
            switch_num += 1
    
    # Place thumb keys
    # SW20: directly beneath SW16 (bottom of col5 at row 0)
    # "Beneath" means lower y value in FreeCAD coords
    sw20_x = frame_border + 5 * switch_spacing + kicad_offset_x
    sw20_y = frame_border - switch_spacing + col_offsets[5]
    
    sw20 = board.FindFootprintByReference('SW20')
    if sw20:
        sw20.SetPosition(pcbnew.VECTOR2I(
            pcbnew.FromMM(sw20_x),
            pcbnew.FromMM(-sw20_y + kicad_offset_y)
        ))
        print(f'SW20 placed at ({sw20_x:.2f}, {sw20_y:.2f}) mm (FreeCAD coords)')
        
        # Place D20 underneath SW20
        d20 = board.FindFootprintByReference('D20')
        if d20:
            d20.SetPosition(pcbnew.VECTOR2I(
                pcbnew.FromMM(sw20_x),
                pcbnew.FromMM(-sw20_y + kicad_offset_y + pcbnew.ToMM(diode_offset))
            ))
            print(f'D20 placed at ({sw20_x:.2f}, {sw20_y - diode_offset:.2f}) mm (FreeCAD coords)')
        else:
            print('D20 not found on board')
    else:
        print('SW20 not found on board')
    
    # SW19: to the left of SW20
    sw19_x = frame_border + 4 * switch_spacing + kicad_offset_x
    sw19_y = sw20_y
    
    sw19 = board.FindFootprintByReference('SW19')
    if sw19:
        sw19.SetPosition(pcbnew.VECTOR2I(
            pcbnew.FromMM(sw19_x),
            pcbnew.FromMM(-sw19_y + kicad_offset_y)
        ))
        print(f'SW19 placed at ({sw19_x:.2f}, {sw19_y:.2f}) mm (FreeCAD coords)')
        
        # Place D19 underneath SW19
        d19 = board.FindFootprintByReference('D19')
        if d19:
            d19.SetPosition(pcbnew.VECTOR2I(
                pcbnew.FromMM(sw19_x),
                pcbnew.FromMM(-sw19_y + kicad_offset_y + pcbnew.ToMM(diode_offset))
            ))
            print(f'D19 placed at ({sw19_x:.2f}, {sw19_y - diode_offset:.2f}) mm (FreeCAD coords)')
        else:
            print('D19 not found on board')
    else:
        print('SW19 not found on board')
    
    # Place SW21 and SW22 on circle centered below SW20
    thumb_radius = params['ThumbRadius'].val
    thumb_angle = params['ThumbRotationAngle'].val
    
    # Circle center is ThumbRadius below SW20
    circle_center_x = sw20_x
    circle_center_y = sw20_y - thumb_radius
    
    # SW20 is at the top of the circle (90 degrees)
    # SW21 is at 90 + thumb_angle degrees
    # SW22 is at 90 + 2*thumb_angle degrees
    
    for i, sw_num in enumerate([21, 22]):
        angle_deg = 90 + (i + 1) * thumb_angle
        angle_rad = math.radians(angle_deg)
        
        x = circle_center_x + thumb_radius * math.cos(angle_rad)
        y = circle_center_y + thumb_radius * math.sin(angle_rad)
        
        sw = board.FindFootprintByReference(f'SW{sw_num}')
        if sw:
            sw.SetPosition(pcbnew.VECTOR2I(
                pcbnew.FromMM(x),
                pcbnew.FromMM(-y + kicad_offset_y)
            ))
            # Rotate the switch to match its angle on the circle
            # KiCAD angles are in tenths of a degree (decidegrees)
            sw.SetOrientation(pcbnew.EDA_ANGLE(angle_deg, pcbnew.DEGREES_T))
            print(f'SW{sw_num} placed at ({x:.2f}, {y:.2f}) mm (FreeCAD coords) - angle: {angle_deg:.1f}°')
            
            # Place diode underneath rotated switch
            # For rotated switches, offset diode radially outward from circle center
            d_ref = f'D{sw_num}'
            diode = board.FindFootprintByReference(d_ref)
            if diode:
                # Calculate diode position: move along the radial direction (away from center)
                diode_x = x + diode_offset * math.cos(angle_rad)
                diode_y = y + diode_offset * math.sin(angle_rad)
                diode.SetPosition(pcbnew.VECTOR2I(
                    pcbnew.FromMM(diode_x),
                    pcbnew.FromMM(-diode_y + kicad_offset_y)
                ))
                diode.SetOrientation(pcbnew.EDA_ANGLE(angle_deg, pcbnew.DEGREES_T))
                print(f'{d_ref} placed at ({diode_x:.2f}, {diode_y:.2f}) mm (FreeCAD coords) - angle: {angle_deg:.1f}°')
            else:
                print(f'{d_ref} not found on board')
        else:
            print(f'SW{sw_num} not found on board')
    
    # Create border outline
    # Calculate board dimensions
    board_width = 2 * frame_border + 5 * switch_spacing
    board_height = 2 * frame_border + 2 * switch_spacing + abs(circle_center_y - frame_border)
    
    # Apply KiCAD offset
    border_x0 = kicad_offset_x
    border_y0 = kicad_offset_y
    border_x1 = board_width + kicad_offset_x
    border_y1 = kicad_offset_y - board_height
    
    # Create rectangular border (4 line segments)
    border_lines = [
        ((border_x0, border_y0), (border_x1, border_y0)),  # Top
        ((border_x1, border_y0), (border_x1, border_y1)),  # Right
        ((border_x1, border_y1), (border_x0, border_y1)),  # Bottom
        ((border_x0, border_y1), (border_x0, border_y0)),  # Left
    ]
    
    for (x1, y1), (x2, y2) in border_lines:
        line = pcbnew.PCB_SHAPE()
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        line.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(pcbnew.FromMM(0.15))
        line.SetComment("AUTO_GENERATED_BORDER")
        board.Add(line)
    
    print(f'Border created: {board_width:.2f} x {board_height:.2f} mm')
    
    pcbnew.Refresh()

switch_placement()
