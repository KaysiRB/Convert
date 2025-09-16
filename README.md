# Outfits Converter

This project converts GTA V outfit codes between BBFAS and Cherax JSON. It provides a menu-driven Python tool, conversion modules.

---

## Table of Contents

- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [File Descriptions](#file-descriptions)
  - [Main Files](#main-files)
  - [Modules](#modules)
  - [Output Folders](#output-folders)
- [Troubleshooting](#troubleshooting)

---

## Project Structure

```
├── output/
│   └── .gitkeep
│   └── BBFAS
│       └── .gitkeep
│   └── CHERAX
│       └── .gitkeep
├── src/
│   ├── Modules/
│   │   ├── BBFAS-JSON.py
│   │   ├── CHERAX-BBFAS.py
│   │   ├── JSON-CHERAX.py
│   │   └── __init__.py
│   ├── debug_main.py
│   └── main.py
├── .gitignore
├── README.md
└── run.bat
```

---

## How to Use

### 1. **Run the Converter**

- **Windows:** Double-click `run.bat` or run in terminal:
  ```sh
  run.bat
  ```
- **Any OS:** Run the main Python script:
  ```sh
  python main.py
  ```

### 2. **Menu Options**

- **1:** BBFAS CODE → JSON BBFAS
- **2:** JSON BBFAS → JSON CHERAX
- **3:** JSON CHERAX → BBFAS CODE
- **4:** BBFAS CODE → JSON CHERAX (direct)
- **5:** JSON CHERAX → BBFAS CODE (direct)
- **0:** Exit

Generated files are saved in the `output/` folder.

---

## File Descriptions

### Main Files

- **[main.py](src/main.py):**  
  The main menu-driven script. Handles user input and calls conversion functions from modules.

- **[run.bat](run.bat):**  
  Windows batch launcher for `main.py`. Checks for Python and project structure.

- **[debug_main.py](src/debug_main.py):**  
  Diagnostic tool to inspect modules, list functions, and check for misplaced conversion functions.

### Modules

All modules are in [src/modules/](src/modules):

- **[BBFAS-JSON.py](src/modules/BBFAS-JSON.py):**  
  Converts BBFAS base64 codes to structured JSON.  
  - Main function: [`convert_bbfas_to_json`](src/modules/BBFAS-JSON.py)

- **[JSON-CHERAX.py](src/Modules/JSON-CHERAX.py):**  
  Converts BBFAS JSON to Cherax JSON format.  
  - Main function: [`convert_json_to_cherax`](Modules/JSON-CHERAX.py)

- **[CHERAX-BBFAS.py](src/Modules/CHERAX-BBFAS.py):**  
  Converts Cherax JSON back to BBFAS base64 code.  
  - Main function: [`convert_cherax_to_bbfas`](Modules/CHERAX-BBFAS.py)

- **[__init__.py](src/Modules/__init__.py):**  
  Empty file to mark the folder as a Python package.
  
### Output Folders

- **[output/BBFAS/](output/BBFAS):**  
  Stores generated BBFAS JSON and code files.

- **[output/CHERAX/](output/CHERAX):**  
  Stores generated Cherax JSON files.

---

## Troubleshooting

- If you see import errors, check that all files are in the correct structure.
- Use [`debug_main.py`](src/debug_main.py) to inspect modules and verify function locations.
- For Windows, ensure Python is installed and in your PATH.

---

## Credits

[BBFAS](https://www.bbfas.com/) and [Cherax](https://cherax.menu/).
