# Mercor Challenge

## Language & Setup
**Language:** Python 3.10+  
**Runtime Requirements:** Python 3.x and `pip` package manager.  

### Installation
Clone the repository and install dependencies:
```bash
git clone <your-private-repo-url>
cd mercor-challenge
pip install -r requirements.txt
```
## Running tests

We use pytest for testing

Run the entire test suit
```bash
pytest
```

If you encounter import errors, run:

```bash
PYTHONPATH=. pytest
```

Run a specific test file

example:

```bash
pytest tests/test_simulation.py
```
Run a specific test function

example:

```bash
pytest -k "test_simulate_basic_growth"
```



