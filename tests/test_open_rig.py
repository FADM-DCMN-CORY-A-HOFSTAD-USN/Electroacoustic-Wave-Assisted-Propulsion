import pytest
import os
import numpy as np
from src.core.generate_open_gantry import OpenGantryRigGenerator
from src.core.open_propulsion_rig import OpenPropulsionRigController

def test_procedural_open_gantry_scad_io(tmpdir):
    generator = OpenGantryRigGenerator()
    generator.output_dir = str(tmpdir)
    
    scad_output_path = generator.compile_open_gantry_mesh()
    assert os.path.exists(scad_output_path)
    with open(scad_output_path, "r") as f:
        content = f.read()
    assert "cylinder" in content
    assert "cube" in content

def test_three_valued_logic_indeterminate_trap():
    controller = OpenPropulsionRigController()
    mock_anode_charge_array = np.array([25.0, 30.0, 25.0], dtype=np.float32)
    
    # Evaluate under a standard nominal Hex validation state 'A'
    nominal_run = controller.evaluate_e_field_vector_matrix(mock_anode_charge_array, logic_state="A")
    assert nominal_run["three_valued_logic_execution_state"] == "NOMINAL_3VL_TRUE"
    assert nominal_run["structural_conformity"] is True
    
    # Evaluate under a Kleene 3VL Indeterminate configuration exception signal
    trapped_run = controller.evaluate_e_field_vector_matrix(mock_anode_charge_array, logic_state="UNKNOWN")
    assert trapped_run["three_valued_logic_execution_state"] == "KLEENE_NULL_RESET"
    assert trapped_run["mean_asymmetric_e_field_force"] == 0.0  # Safe grounding fallback loop
    assert trapped_run["structural_conformity"] is False
