# Project Overview

This project is a Python GUI application built with Tkinter. Its purpose is to generate a festive, animated HTML page. The application, `automate.py`, allows the user to input custom ASCII art, select a color for the text, and define an animation delay. It then generates an HTML file (named `winter_led.html` by default) that displays the ASCII art as a glowing, blinking "LED" sign over a continuously scrolling, animated winter landscape background created with HTML5 Canvas and JavaScript.

# Building and Running

The project is a single Python script and does not have a formal build process. It can be run directly.

**Dependencies:**

The script uses the standard Python libraries `tkinter`, `webbrowser`, `os`, and `json`. These are typically included with Python. The project also contains a `.venv` directory, suggesting a virtual environment is used.

**Running the application:**

```bash
# Make sure you are in the project's virtual environment
# On Windows:
.venv\Scripts\activate

# Run the python script
python automate.py
```

# Development Conventions

*   The project consists of a single Python script (`automate.py`).
*   The script generates a self-contained HTML file with embedded CSS and JavaScript.
*   The user-facing application is built using the Tkinter library.
*   The animation is handled entirely by JavaScript within the generated HTML file.
