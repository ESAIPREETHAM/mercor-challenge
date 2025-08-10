# Mercor Challenge

## Language & Setup
**Language:** Python 3.10+  
**Runtime Requirements:** Python 3.x and `pip` package manager.  

### Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/ESAIPREETHAM/mercor-challenge
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

## Design choices

### Data structure
1) I used Python classes to model the network of referrers.
2) Lists are used for sequential simulation, and dictionaries are used for quick lookups of referral counts and capacities.
3) The approach balances simplicity and efficiency, making it easy to expand later if more complex referral rules are added.

### API Design
1) Simulation Class:
     i) simulate(p, days) → Runs simulation for a given adoption probability p and duration in days, returning cumulative hires per day.
     ii)days_to_target(p, target_total) → Calculates the minimum number of days needed to hit a target total hires.
2) Modularity: Referral logic and simulation logic are split into separate files (ReferralNetwork.py and Simulation.py) under source/.
3) Testability: All major logic paths are covered in tests/ using pytest.

### Dependancy management
I have listed all dependencies in requirements.txt
Install them with: 
```bash
pip install -r requirements.txt
```

## Approximate Time Taken

| File / Task                          | Time Spent |
|--------------------------------------|------------|
| ReferralNetwork.py (core logic)      | ~1 hr 30 min |
| Simulation.py (simulation engine)    | ~1 hr |
| test_simulation.py (test suite)      | ~45 min |
| README.md (documentation)            | ~20 min |
| requirements.txt (dependencies)      | ~5 min |
| Debugging & fixing imports           | ~15 min |
| **Total**                            | **~3 hr 55 min** |


## Acknowledgment of AI assistance

Parts of this codebase were developed with the help of AI tools (e.g., ChatGPT) for:
  1) I used it for only for boilerplate code generation
  2) for debugging import path issues
  3) And finally drafting initial README and project structure
This code is completely implemented by me (i.e, author: Saipreetham Eamani).
Thank you.


