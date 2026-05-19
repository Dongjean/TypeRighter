# TypeRighter
### Orbital 2026 (Dongjin & Andrew)

## Tech Stack
* **Language:** Python 3.11+
* **Testing Framework:** pytest 8.0.0
* **CI/CD Platform:** GitHub Actions

## Dependencies
* All dependencies are to be included in dependencies.txt with format: ```dependency==version```

## Using the Virtual Environment
### Activate
In the root directory, run:

Linux:
```bash
source .venv/source/activate
```

Windows (Command Prompt):
```bash
.venv/Scripts/activate.bat
```

Windows (Powershell):
```bash
.venv/Scripts/Activate.ps1
```

### Deactivate
From anywhere, run:
```deactivate```

## Setup
*NOTE: enter the Virtual Environment before any Setup steps*
### Setup the Virtual Environment
In the root directory, run:
```bash
python -m venv .venv
```

### Installing Dependencies
In the root directory, run:
```bash
pip install -r dependencies.txt
```

## Testing

### Test Locally

In the root directory, run:

```bash
pytest -v
```


### Test through Github Actions
Pushing changes to github automatically triggers the tests

## Usage
Coming soon