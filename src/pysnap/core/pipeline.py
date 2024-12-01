from typing import List, Dict, Any, Tuple
from .snap import Snap
from collections import defaultdict, deque

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
        Execute the pipeline by processing data through connected Snaps in a DAG order.
        
        Args:
            initial_inputs: Optional initial input data for the first Snap
        
        Returns:
            Final output of the pipeline
        """
        current_data = initial_inputs or {}
        
        # Build the graph and in-degree count
        graph = defaultdict(list)
        in_degree = {snap: 0 for snap in self.snaps}
        
        for source_snap, source_output, destination_snap, destination_input in self.connections:
            graph[source_snap].append((destination_snap, source_output, destination_input))
            in_degree[destination_snap] += 1
        
        # Perform topological sort
        queue = deque([snap for snap in self.snaps if in_degree[snap] == 0])
        sorted_snaps = []
        
        while queue:
            snap = queue.popleft()
            sorted_snaps.append(snap)
            
            for destination_snap, source_output, destination_input in graph[snap]:
                in_degree[destination_snap] -= 1
                if in_degree[destination_snap] == 0:
                    queue.append(destination_snap)
        
        # Execute snaps in topologically sorted order
        for snap in sorted_snaps:
            if not snap.validate_inputs(current_data):
                raise ValueError(f"Invalid inputs for Snap: {snap}")
            
            output_data = snap.process(current_data)
            
            for destination_snap, source_output, destination_input in graph[snap]:
                if source_output in output_data:
                    current_data[destination_input] = output_data[source_output]
                else:
                    raise ValueError(f"Output {source_output} not found in Snap: {snap}")
        
        return current_data
