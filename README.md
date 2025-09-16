# Outfits Converter

This project converts GTA V outfit codes between BBFAS and Cherax JSON. It provides a menu-driven Python tool, conversion modules.

---

## Table of Contents

- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [File Descriptions](#file-descriptions)
  - [Main Files](#main-files)
  - [Modules](#modules)
  - [Templates & Examples](#templates--examples)
  - [Temporary Scripts](#temporary-scripts)
  - [Output Folders](#output-folders)
- [Troubleshooting](#troubleshooting)

---

## Project Structure

```
debug_main.py
main.py
run.bat
README.md
.TEMP/
  Base64ToJson.py
  JsonToBase.py
  Template/
    BBFAS/
      a.json
    Cherax/
      Cherax.txt
Modules/
  __init__.py
  BBFAS-JSON.py
  CHERAX-BBFAS.py
  JSON-CHERAX.py
output/
  BBFAS/
  CHERAX/
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

- **[main.py](main.py):**  
  The main menu-driven script. Handles user input and calls conversion functions from modules.

- **[run.bat](run.bat):**  
  Windows batch launcher for `main.py`. Checks for Python and project structure.

- **[debug_main.py](debug_main.py):**  
  Diagnostic tool to inspect modules, list functions, and check for misplaced conversion functions.

### Modules

All modules are in [Modules/](Modules):

- **[BBFAS-JSON.py](Modules/BBFAS-JSON.py):**  
  Converts BBFAS base64 codes to structured JSON.  
  - Main function: [`convert_bbfas_to_json`](Modules/BBFAS-JSON.py)

- **[JSON-CHERAX.py](Modules/JSON-CHERAX.py):**  
  Converts BBFAS JSON to Cherax JSON format.  
  - Main function: [`convert_json_to_cherax`](Modules/JSON-CHERAX.py)

- **[CHERAX-BBFAS.py](Modules/CHERAX-BBFAS.py):**  
  Converts Cherax JSON back to BBFAS base64 code.  
  - Main function: [`convert_cherax_to_bbfas`](Modules/CHERAX-BBFAS.py)

- **[__init__.py](Modules/__init__.py):**  
  Empty file to mark the folder as a Python package.

### Templates & Examples

- **[.TEMP/Template/BBFAS/a.json](.TEMP/Template/BBFAS/a.json):**  
  Example BBFAS JSON file (decoded from base64).

- **[.TEMP/Template/Cherax/Cherax.txt](.TEMP/Template/Cherax/Cherax.txt):**  
  Example Cherax JSON file.

### Temporary Scripts

- **[.TEMP/Base64ToJson.py](.TEMP/Base64ToJson.py):**  
  Standalone script to decode a BBFAS base64 code and generate a labeled JSON file.

- **[.TEMP/JsonToBase.py](.TEMP/JsonToBase.py):**  
  (Empty) Placeholder for future JSON-to-base64 conversion script.

### Output Folders

- **[output/BBFAS/](output/BBFAS):**  
  Stores generated BBFAS JSON and code files.

- **[output/CHERAX/](output/CHERAX):**  
  Stores generated Cherax JSON files.

---

## Troubleshooting

- If you see import errors, check that all files are in the correct structure.
- Use [`debug_main.py`](debug_main.py) to inspect modules and verify function locations.
- For Windows, ensure Python is installed and in your PATH.

---

## Credits

[BBFAS](https://www.bbfas.com/) and [Cherax](https://cherax.menu/).