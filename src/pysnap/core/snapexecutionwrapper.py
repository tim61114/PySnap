from enum import Enum, auto
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from pysnap.core.snap import Snap


class SnapExecutionState(Enum):
    """
    Represents the execution state of a SnapExecutionWrapper.

    State Progression:
    CREATED → Initial state when wrapper is instantiated
    PARTIAL → Some inputs have been received, but not all required inputs are present
    READY → All required inputs have been collected and wrapper is ready for execution
    EXECUTED → Snap has completed its processing
    """
    CREATED = auto()
    PARTIAL = auto()
    READY = auto()
    EXECUTED = auto()


@dataclass
class SnapExecutionWrapper:
    """
    A wrapper class to manage the execution of a Snap module.

    This wrapper handles the lifecycle of a Snap's execution, managing inputs,
    tracking execution state, and providing a clean interface for pipeline processing.

    Core Responsibilities:
    1. Collect and manage input views
    2. Trigger Snap execution when all inputs are ready
    3. Provide execution metadata and state management
    """

    # The Snap to be executed
    snap: Snap

    # Collected inputs for the Snap
    inputs: Dict[str, Any] = field(default_factory=dict)

    # Execution metadata
    execution_time: Optional[float] = None
    execution_timestamp: Optional[datetime] = None

    # Execution state
    state: SnapExecutionState = SnapExecutionState.CREATED
    outputs: Optional[Dict[str, Any]] = None

    def add_input(self, view_name: str, data: Any) -> bool:
        """
        Add an input to the wrapper's input collection and update state.

        Args:
            view_name: Name of the input view
            data: Data to be added for the input view

        Returns:
            Boolean indicating whether the input was successfully added
        """
        # Validate the input against the Snap's input views
        if not self._validate_input(view_name, data):
            return False

        # Add the input
        self.inputs[view_name] = data

        # Update state based on input collection
        self._update_state()

        return True

    def _validate_input(self, view_name: str, data: Any) -> bool:
        """
        Validate a single input against the Snap's input view requirements.

        Args:
            view_name: Name of the input view
            data: Data to be validated

        Returns:
            Boolean indicating whether the input is valid
        """
        # Find the corresponding input view
        matching_views = [view for view in self.snap.input_views if view.name == view_name]

        if not matching_views:
            return False

        input_view = matching_views[0]
        return input_view.validate(data)

    def is_ready_for_execution(self) -> bool:
        """
        Determine if the wrapper has all required inputs for Snap execution.

        Returns:
            Boolean indicating whether all required inputs are present
        """
        # Check if all required input views are filled
        required_view_names = {view.name for view in self.snap.input_views if view.required}
        self._update_state()
        return required_view_names.issubset(self.inputs.keys())

    def _update_state(self):
        """
        Update the wrapper's state based on input collection.
        """
        # Determine required input view names
        required_view_names = {view.name for view in self.snap.input_views if view.required}

        # Track collected input view names
        collected_view_names = set(self.inputs.keys())

        # State transition logic
        if required_view_names.issubset(collected_view_names):
            self.state = SnapExecutionState.READY
        elif collected_view_names:
            self.state = SnapExecutionState.PARTIAL
        else:
            self.state = SnapExecutionState.CREATED


    def execute(self) -> Dict[str, Any]:
        """
        Execute the Snap with collected inputs.

        Raises:
            RuntimeError: If not in READY state

        Returns:
            Dictionary of output view results
        """
        # Ensure wrapper is in READY state before execution
        if self.state != SnapExecutionState.READY:
            raise RuntimeError(f"Cannot execute Snap. Current state: {self.state}")

        # Track execution start time
        start_time = datetime.now()

        try:
            # Execute the Snap's process method
            self.outputs = self.snap.process(self.inputs)

            # Update state and execution metadata
            self.state = SnapExecutionState.EXECUTED
            self.execution_time = (datetime.now() - start_time).total_seconds()
            self.execution_timestamp = start_time

            return self.outputs

        except Exception as e:
            # Optionally, you could add more sophisticated error handling
            raise