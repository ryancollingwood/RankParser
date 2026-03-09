# Web UI Proposal for RankParser

## Introduction

This document outlines a proposal to implement a Web User Interface (Web UI) for RankParser, enabling users to interact with the application via a browser in addition to the existing Command Line Interface (CLI).

## Refactoring and Extraction Requirements

To support both CLI and Web UI effectively, the following refactoring and extraction tasks are needed:

1. **Decouple Logic from Presentation:**
   - **Interactive Session Separation:** The `Session` class in `interactive/session.py` contains both core application logic (e.g., managing projects, history, invoking parser/solver) and presentation logic (CLI I/O like `print`, `input()`, `PromptSession`).
   - *Action:* Extract the business logic from `Session` into a core `RankParserCore` or `ProjectManager` class. This class should manage the `RankingProblem`, history, project files, and return data structures instead of printing them. The CLI `Session` and the new Web UI backend will both consume this core class.
2. **Standardize Outputs:**
   - The CLI relies heavily on `colorama` and print statements (e.g., in `solve_challenge()`, `main.py`, `interactive/session.py`).
   - *Action:* Ensure that all core operations (parsing, solving, suggesting pairs, generating graphs) return standard data formats (e.g., lists of strings, dictionaries, paths to generated files, error objects) that can be easily serialized to JSON for a web API, while the CLI handles formatting these objects for the terminal.
3. **Error Handling:**
   - Errors like `IncompleteResultsError` and `UnsolvableModelError` currently print directly to the console in some places.
   - *Action:* Propagate these exceptions up to the interface layer (CLI or Web API) so they can be formatted as appropriate HTTP error responses or CLI error messages.

## Functionality Replacements for Web UI

When transitioning from the CLI to a Web UI, certain functionalities must be replaced or adapted:

1. **Command Input:**
   - **CLI:** Uses `prompt_toolkit` with auto-suggestion and history.
   - **Web UI:** Will need a text input field for submitting commands, a history panel to view past commands, and possibly visual buttons to represent common actions (Solve, Undo, Suggest Pair) instead of typing them out.
2. **Syntax Highlighting:**
   - **CLI:** Uses `interactive/highlight.py` and `STYLE_MAP` which relies on ANSI escape codes (`colorama`).
   - **Web UI:** Needs to be replaced with HTML/CSS based syntax highlighting. The `HighLighter` could be adapted to return HTML span tags with specific classes based on token types, or the frontend could handle the highlighting logic.
3. **Graph Generation (Graphviz):**
   - **CLI:** Generates `.dot` files and expects the user to manually render them or relies on local graphviz installations.
   - **Web UI:** Can use frontend libraries (like `vis.js`, `D3.js`, or `d3-graphviz`) to dynamically render the network/graph directly in the browser based on the solver's JSON output or a provided `.dot` string.
4. **Project and File Management:**
   - **CLI:** Creates local directories, reads/writes text and CSV files directly to the filesystem.
   - **Web UI:** Needs an API to handle project isolation (e.g., via session IDs or user accounts). File exports (CSV, dot) should be provided as downloadable links rather than written to the local disk of the user.

## Suggestions for Implementing Web UI with Minimal Frontend Skills

For a developer with minimal frontend experience, building a full Single Page Application (SPA) might be daunting. Here are accessible approaches:

1. **Use Streamlit or Gradio (Highly Recommended)**
   - These are Python libraries designed exactly for this use case: turning Python scripts into interactive web apps with almost zero HTML/CSS/JS knowledge.
   - You write pure Python, and the library handles the UI components (text inputs, buttons, data tables, rendering markdown/HTML).
   - This aligns perfectly with RankParser as it’s already Python-based.

2. **Flask or FastAPI with Server-Side Rendering (Jinja2)**
   - Create a simple web server using Flask or FastAPI.
   - Use Jinja2 templates for the frontend. You can use a lightweight CSS framework like **Bootstrap**, **Bulma**, or **Tailwind CSS** to make the UI look professional without needing to write custom CSS.
   - Forms can be submitted via standard HTML POST requests, reducing the need for complex JavaScript AJAX calls.

3. **HTMX**
   - If you want a more dynamic, SPA-like feel without writing JavaScript, you can use HTMX alongside Flask/FastAPI. HTMX allows you to access AJAX, CSS Transitions, WebSockets, and Server Sent Events directly in HTML, using attributes.

### Proposed Architecture using Minimal Frontend Approach (Streamlit/Flask)

- **Backend:** Expose `RankParserCore` logic.
- **Frontend (Streamlit):**
  - A sidebar for project selection/creation.
  - A main chat-like interface or text area for entering commands.
  - An output pane that displays results as tables (for rankings) or renders Graphviz outputs using Streamlit's built-in `st.graphviz_chart`.

By focusing on Python-based web frameworks or lightweight templating, the Web UI can be achieved quickly and maintainably.