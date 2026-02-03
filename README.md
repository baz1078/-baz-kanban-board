# Assure Home Inspections - Kanban Board

A simple project management Kanban board for Assure Home Inspections, Naperville, IL.

## Features

- Three-column Kanban board (To Do, In Progress, Done)
- Add new tasks with priority levels (High, Medium, Low)
- Move tasks between columns with arrow buttons
- Delete tasks
- Persistent storage (JSON file)
- Task statistics in sidebar
- Color-coded priorities

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

## Usage

1. **Add Tasks**: Use the sidebar form to add new tasks with title, priority, and target column
2. **Move Tasks**: Use ⬅️ and ➡️ buttons to move tasks between columns
3. **Delete Tasks**: Use 🗑️ button to remove tasks
4. **Reset**: Use the "Reset to Default" button to restore original backlog

## Data Storage

Tasks are saved to `kanban_data.json` in the same directory.