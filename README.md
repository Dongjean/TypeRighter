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

### Setting Environment Variables
In the root directory, make a file names ```.env```, and add the following key-values:
```ini
FB_API_KEY="your_value"
FB_AUTH_DOMAIN="your_value"
FB_PROJECT_ID="your_value"
FB_STORAGE_BUCKET="your_value"
FB_MESSAGING_SENDER_ID="your_value"
FB_APP_ID="your_value"
FB_MEASUREMENT_ID="your_value"
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

8. **Delete the remote branch on the local repository**
    ```bash
    git fetch --prune
    ```
    * This removes local remote branches that no longer exist on github

## Usage

There are 3 'Modes' to the app:
1. background-mode (**bg-mode**)
2. overlay-mode (**overlay-mode**)
3. control panel-mode (**cp-mode**)

In the root directory, run the script with:
```bash
python main.py
```

**bg-mode**
* Pressing ```CTRL + LEFT_ALT + SPACE``` enters **overlay-mode**
    * Pressing it again exits **overlay-mode**
* Otherwise, normal typing is permitted

**overlay-mode**
* Green overlay indicates **overlay-mode**
* Typing ```\``` is blocked
* Press and hold ```\``` to insert a new command, and a preview can be seen in a popup on the screen:
    * ```a``` - Exit **overlay-mode**, into **bg-mode**
    * ```s``` - Exit **overlay-mode**, into **cp-mode**
    * ``` ` ``` - Exit the app entirely
    * Any other single character inserts its preset shortcut unicode
    * If there is no preset shortcut unicode, insert its preset unicode phrase
    * Otherwise, if the typed character matches a unicode character name, insert it

_All of the above shortcuts, including ```\```, ```a```, ```s``` and ``` ` ```, can be changed via Preferences Settings in **cp-mode**_

**cp-mode**
1. LaTeX editor:
    * Enter LaTeX code in the text editor
    * Press enter or click the compile button to have the LaTeX output displayed
    * Press the download button to save the LaTeX output

2. Login page:
    * User Authentication with Firebase
    * Can Login or Signup through this page

3. Unicode Menu: 
    * Search Unicode using unicode codepoint or name
    * Bind keys to unicode by press the bind button
    * While overlay is active, press shortcut key followed by Ctrl + V to insert symbol 

4. Settings:
    * Preferences Setting
        * Select the template you wish to edit
        * Rebind or Unbind the Shortcuts from that template
        * Rebind or Unbind the Phrase Shortcuts from that template
        * Add new or Unbind LaTeX Shortcuts from that template
    * Control Panel Setting (not implemented)
        * Edit the size and popup location of the control panel

_All of the above in **cp-mode** are accessible via the right Navigation Bar_