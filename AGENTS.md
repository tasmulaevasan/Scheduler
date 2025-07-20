# Repository Guidelines

This project contains a PyQt-based application. Follow these instructions when making changes.

## Coding Style
- Write Python code using PEP8 conventions with 4 spaces per indent and a maximum line
  length of 100 characters.
- Provide a short docstring for every public function or class.
- Keep variable and function names in English.

## UI and Resources
- Do not edit `resource_rc.py` manually. After modifying `resource.qrc` or any images
  under `icon/`, regenerate the resource file with:
  ```bash
  pyrcc6 resource.qrc -o resource_rc.py
  ```
- `*.ui` files are edited with Qt Designer; avoid manual edits unless necessary.

## Commit Messages
- Use concise English summaries in the first line of each commit message.

## Database
- The application creates `teachers.db` at runtime. Do not commit this file.

## Running the Application
- Launch the UI with `python main.py`.
