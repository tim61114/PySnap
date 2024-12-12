from typing import List, Dict, Any, Tuple
from .snap import Snap
from collections import defaultdict, deque

from .snapexecutionwrapper import SnapExecutionWrapper


class Pipeline:
    """
    Manages the execution of a sequence of Snaps.
    
    Allows adding Snaps, connecting their input and output views,
    and executing the entire pipeline.
    """
    
    def __init__(self):
        self.snaps: List[Snap] = []
        self.connections: List[Tuple[Snap, str, Snap, str]] = []
        self.snap_execution_instance: Dict[Snap, SnapExecutionWrapper] = {}
    
    def add_snap(self, snap: Snap):
        """
        Add a Snap to the pipeline.
        
        Args:
            snap: Snap to be added to the pipeline
        """
        self.snaps.append(snap)
        self.snap_execution_instance[snap] = SnapExecutionWrapper(snap)
    
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
    
    def execute(self, initial_inputs: Dict[str, Any] = None) -> bool:
        """
        Execute the pipeline by processing data through connected Snaps in a DAG order.
        
        Args:
            initial_inputs: Optional initial input data for the first Snap
        
        Returns:
            True if the pipeline executed successfully
        """
        # Build the graph and in-degree count
        graph = defaultdict(list)
        in_degree = {snap: 0 for snap in self.snaps}
        
        for source_snap, source_output, destination_snap, destination_input in self.connections:
            graph[source_snap].append((destination_snap, source_output, destination_input))
            in_degree[destination_snap] += 1


        # Find all snaps with 0 in-degree and 1 input view
        starting_snaps = [snap for snap in self.snaps if in_degree[snap] == 0 and len(snap.input_views) == 1]
        ready_snaps = [snap for snap in self.snaps if in_degree[snap] == 0]

        if len(starting_snaps) > 1:
            raise ValueError("Invalid pipeline configuration: Multiple open input views detected")

        if len(starting_snaps) == 1:
            target_snap = starting_snaps[0]
            self.snap_execution_instance[target_snap].add_input(target_snap.input_views[0].name, initial_inputs[starting_snaps[0].input_views[0].name])

        # Prepare snaps with 0 in-degree for execution
        for snap in ready_snaps:
            self.snap_execution_instance[snap].is_ready_for_execution()

        job_queue = [snap for snap in ready_snaps]

        while job_queue:
            cur_snap_instance = self.snap_execution_instance[job_queue.pop(0)]
            output = cur_snap_instance.execute()
            for destination_snap, source_output, destination_input in graph[cur_snap_instance.snap]:
                if source_output not in output.keys():
                    continue
                self.snap_execution_instance[destination_snap].add_input(destination_input, output[source_output])
                if self.snap_execution_instance[destination_snap].is_ready_for_execution():
                    job_queue.append(destination_snap)


        return True

    def get_output(self):
        #find all snaps with out-degree 0
        output_snaps = [snap for snap in self.snaps if not any([snap == connection[0] for connection in self.connections])]
        for snap in output_snaps:
            print(self.snap_execution_instance[snap].outputs if self.snap_execution_instance[snap].outputs else "no output from this snap")



