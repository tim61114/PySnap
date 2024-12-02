from dataclasses import dataclass
from typing import Optional, Type, Any

@dataclass
class InputView:
    """
    Represents an input connection point for a Snap.
    
    Attributes:
        name: Unique identifier for the input view
        type_hint: Optional type annotation for data validation
        required: Whether this input view must be connected
        description: Human-readable explanation of the input's purpose
    """
    name: str
    type_hint: Optional[Type[Any]] = None
    required: bool = False
    description: str = ""
    
    def validate(self, value: Any) -> bool:
        """
        Basic validation method that can be extended in the future.
        
        Args:
            value: The value to validate against the input view's specifications
        
        Returns:
            Boolean indicating whether the value meets the input view's requirements
        """
        # If type_hint is specified, check type compatibility
        if self.type_hint is not None and not isinstance(value, self.type_hint):
            return False
        
        # If required, ensure value is not None
        if self.required and value is None:
            return False
        
        return True

@dataclass
class OutputView:
    """
    Represents an output connection point for a Snap.
    
    Attributes:
        name: Unique identifier for the output view
        type_hint: Optional type annotation for data validation
        description: Human-readable explanation of the output's purpose
    """
    name: str
    type_hint: Optional[Type[Any]] = None
    description: str = ""
    
    def validate(self, value: Any) -> bool:
        """
        Basic validation method for output views.
        
        Args:
            value: The value to validate against the output view's specifications
        
        Returns:
            Boolean indicating whether the value meets the output view's requirements
        """
        # If type_hint is specified, check type compatibility
        if self.type_hint is not None and not isinstance(value, self.type_hint):
            return False
        
        return True
