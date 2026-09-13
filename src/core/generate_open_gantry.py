#!/usr/bin/env python3
import os
from solid import scad_render, cylinder, cube, union, difference, translate

class OpenGantryRigGenerator:
    """
    Procedurally compiles the open test gantry configuration for the 12.5m 
    Vortex Resonance Cylinder and non-obstructive radial E-Field electrode rings.
    """
    def __init__(self):
        self.cylinder_diameter_mm = 12500.0  # 12.5m open bore matching BB-67 spec
        self.cylinder_radius_mm = self.cylinder_diameter_mm / 2.0
        self.output_dir = "gantry_templates"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def compile_open_gantry_mesh(self) -> str:
        """Assembles the open cylinder core supported by external skeleton mounts."""
        # 1. Bare Open-Ended Resonance Cylinder
        open_core = cylinder(r=self.cylinder_radius_mm + 100, h=6000, center=True, segments=120)
        inner_gas_channel = cylinder(r=self.cylinder_radius_mm, h=6004, center=True, segments=120)
        
        # 2. Non-Obstructive Solid-State E-Field Deflection Rings (Thrust Vectoring Array)
        e_field_ring_upper = cylinder(r=self.cylinder_radius_mm + 400, h=300, center=True, segments=60)
        e_field_ring_inner_cut = cylinder(r=self.cylinder_radius_mm + 200, h=304, center=True, segments=60)
        
        vector_anode_ring = difference()(e_field_ring_upper, e_field_ring_inner_cut)
        
        # 3. Open Laboratory Skeleton Structural Mounting Truss
        support_strut_left = translate([-(self.cylinder_radius_mm + 800), 0, 0])(cube([400, 400, 7000], center=True))
        support_strut_right = translate([(self.cylinder_radius_mm + 800), 0, 0])(cube([400, 400, 7000], center=True))

        # Build complete uninsulated open configuration footprint
        open_gantry_rig = difference()(
            union()(
                open_core, 
                translate([0, 0, 3100])(vector_anode_ring),
                support_strut_left,
                support_strut_right
            ),
            inner_gas_channel
        )
        
        output_file_path = os.path.join(self.output_dir, "open_propulsion_gantry_rig.scad")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write("// --- UNIVAC IX OPEN EXPERIMENTAL RIG Blueprints ---\n")
            f.write(scad_render(open_gantry_rig))
            
        return output_file_path

if __name__ == "__main__":
    generator = OpenGantryRigGenerator()
    generator.compile_open_gantry_mesh()
