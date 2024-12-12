from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .views import InputView, OutputView


class Snap(ABC):
    """
    Abstract base class defining the contract for Snap modules.
    
    Defines the interface for processing data through input and output views.
    """

    @property
    @abstractmethod
    def input_views(self) -> List[InputView]:
        """
        Define the input views for this Snap.
        
        Returns:
            List of InputView objects defining the input contract
        """
        pass

    @property
    @abstractmethod
    def output_views(self) -> List[OutputView]:
        """
        Define the output views for this Snap.
        
        Returns:
            List of OutputView objects defining the output contract
        """
        pass

    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and produce output.
        
        Args:
            inputs: Dictionary of input data keyed by input view names
        
        Returns:
            Dictionary of output data keyed by output view names
        """
        pass

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """
        Validate inputs against the defined input views.
        
        Args:
            inputs: Dictionary of input data to validate
        
        Returns:
            Boolean indicating whether all inputs meet the Snap's requirements
        """
        # Check that all required inputs are present and valid
        for input_view in self.input_views:
            if input_view.required and input_view.name not in inputs:
                return False

            if input_view.name in inputs:
                if not input_view.validate(inputs[input_view.name]):
                    return False

        return True
