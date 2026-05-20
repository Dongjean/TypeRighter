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
```bash
deactivate
```

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

## Git Feature Branch Workflow

1. **Pull latest changes from GitHub**
    ```bash
    git checkout main
    git pull origin main
    ```

2. **Create new feature branch locally**
    ```bash
    git checkout -b feature/name-of-feature
    ```

3. **Make the first changes and commit**
    ```bash
    git add .
    git commit -m "commit name"
    ```

4. **Push changes to GitHub and set upstream with -u**
    ```bash
    git push -u origin feature/name-of-feature
    ```

5. **Open a Pull Request on GitHub and resolve any Merge Conflicts**

6. **Delete the feature branch on GitHub (after merging)**

7. **Delete the feature branch on the local repository**
    ```bash
    git checkout main
    git pull origin main
    git branch -d feature/name-of-feature
    ```

## Usage
Coming soon