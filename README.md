# PySnap 

## Overview

This project is an oversimplified version of the Java Snap API.

### Key Concepts

- **Snap**: A modular processing unit that can transform data
- **InputView**: Defines the input requirements for a Snap
- **OutputView**: Describes the output produced by a Snap
- **Pipeline**: Orchestrates the execution of multiple Snaps in sequence

## Project Structure
```
PySnap/
│
├── src/                                # Source code
│   └── py_snap/
│       └── core/                       # Core framework components
│           ├── views.py                # InputView and OutputView definitions
│           ├── snap.py                 # Abstract Snap base class
│           ├── pipeline.py             # Pipeline implementation
│           └── snapexecutionwrapper.py # Execution wrapper for holding input and output documents
│        
│       
│
├── examples/                           # Examples including pipelines and snaps
│   ├── snaps/                          # Sample snaps to play with
│   ├── simple_pipeline_example.py    
│   ├── router_pipeline_example.py
│   └── chat_completions_pipeline_example.py
├── pyproject.toml                      # Project configuration
└── README.md              
```

## Prerequisites

- Python 3.8+
- pip
- pyenv (recommended for virtual environment management)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tim61114/PySnap.git
cd PySnap
```
### 2. Set Up Virtual Environment
Using pyenv:
```python
# Install Python version (if not already installed)
pyenv install 3.10.13

# Create and activate virtual environment
pyenv virtualenv 3.10.13 pysnap-env
pyenv activate pysnap-env
```

### 3. Install the Package
```bash
# Install in editable mode
pip install -e .
```

## Basic Usage
### Creating a Snap
```python
from pysnap.core.snap import Snap
from pysnap.core.views import InputView, OutputView

class TextUppercaseSnap(Snap):
    @property
    def input_views(self):
        return [InputView(name="text", required=True, type_hint=str)]
    
    @property
    def output_views(self):
        return [OutputView(name="uppercase_text", type_hint=str)]
    
    def process(self, inputs):
        return {"uppercase_text": inputs["text"].upper()}
```

### Creating a Pipeline
```python
from pysnap.core.pipeline import Pipeline

# Create pipeline and add Snaps
pipeline = Pipeline()
pipeline.add_snap(TextUppercaseSnap())

# Execute pipeline
pipeline.execute({"text": "hello world"})
pipeline.get_output()

```

## Development
### Running Examples
```bash
# From project root
python examples/simple_pipeline_example.py
```

### Running Tests
Tests TBA

