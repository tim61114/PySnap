from typing import List, Dict, Any, Tuple
from .snap import Snap

class Pipeline:
    """
    Manages the execution of a sequence of Snaps.
    
    Allows adding Snaps, connecting their input and output views,
    and executing the entire pipeline.
    """
    
    def __init__(self):
        self.snaps: List[Snap] = []
        self.connections: List[Tuple[Snap, str, Snap, str]] = []
    
    def add_snap(self, snap: Snap):
        """
        Add a Snap to the pipeline.
        
        Args:
            snap: Snap to be added to the pipeline
        """
        self.snaps.append(snap)
    
    def connect(self, 
                source_snap: Snap, 
                source_output: str, 
                destination_snap: Snap, 
                destination_input: str):
        """
        Establish a connection between Snaps.
        
        Args:
            source_snap: Snap producing the output
            source_output: Name of the output view to connect
            destination_snap: Snap consuming the input
            destination_input: Name of the input view to connect
        """
        # Future: Add more sophisticated connection validation
        self.connections.append((source_snap, source_output, destination_snap, destination_input))
    
    def execute(self, initial_inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the pipeline by processing data through connected Snaps.
        
        Args:
            initial_inputs: Optional initial input data for the first Snap
        
        Returns:
            Final output of the pipeline
        """
        current_data = initial_inputs or {}
        
        for snap in self.snaps:
            # Validate inputs before processing
            if not snap.validate_inputs(current_data):
                raise ValueError(f"Invalid inputs for Snap: {snap}")
            
            # Process the Snap
            current_data = snap.process(current_data)
        
        return current_data
