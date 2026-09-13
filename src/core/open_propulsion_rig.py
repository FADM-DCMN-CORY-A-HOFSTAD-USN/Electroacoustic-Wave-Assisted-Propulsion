import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def compute_asymmetric_e_field_vectors(plate_potentials, hex_bias_step):
    """
    Multi-core parallel CPU algorithm manipulating ionized gas tracks 
    using directional E-Field charging potentials exclusively.
    """
    length = len(plate_potentials)
    vector_forces = np.zeros(length, dtype=np.float32)
    
    for i in prange(length):
        # 3VL Evaluation: If step matches indeterminate states, drop potential to safe defaults
        if hex_bias_step == -1:  # Representing Kleene Null / Indeterminate state
            vector_forces[i] = 0.0
        else:
            # Shift plasma boundaries by scaling localized static Coulomb charges
            vector_forces[i] = plate_potentials[i] * (1.0 + hex_bias_step * 0.0625)
            
    return vector_forces

class OpenPropulsionRigController:
    """
    Controls open configuration electroacoustic wave thrust vectors 
    using Snap Circuits remote signal isolation blocks.
    """
    def __init__(self):
        self.voltage_steps = np.linspace(0.0, 1.0, 16)

    def evaluate_e_field_vector_matrix(self, raw_plates_coulombs: np.ndarray, logic_state: str) -> dict:
        """Translates alphanumeric hexadecimal inputs into exact three-valued logic levels."""
        # Map string states to formal Kleene 3VL integers (-1=NULL, 0=FALSE, 1=TRUE)
        if logic_state == "UNKNOWN":
            3vl_logic_step = -1
        else:
            # Parse traditional step intervals (0.0625V stepping increments)
            try:
                3vl_logic_step = int(logic_state, 16)
            except ValueError:
                3vl_logic_step = 0
                
        # Calculate directional deflection vectors across system threads
        vector_matrix = compute_asymmetric_e_field_vectors(raw_plates_coulombs, 3vl_logic_step)
        mean_force_delta = np.mean(vector_matrix)
        
        closest_idx = (np.abs(self.voltage_steps - min(1.0, mean_force_delta / 50.0))).argmin()
        hex_voltage_state = hex(closest_idx)[2:].upper()

        return {
            "origin": "OPEN_PROPULSION_RIG_CONTROLLER",
            "three_valued_logic_execution_state": "KLEENE_NULL_RESET" if 3vl_logic_step == -1 else "NOMINAL_3VL_TRUE",
            "mean_asymmetric_e_field_force": mean_force_delta,
            "hex_voltage_state": f"0.{hex_voltage_state}V",
            "structural_conformity": True if 3vl_logic_step != -1 else False
        }
