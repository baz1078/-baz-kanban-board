# Assure Home Inspections - Kanban Board

A Streamlit-based Kanban board for tracking business growth and AI development tasks.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Features

- 5 columns: Backlog, To Do, In Progress, Review, Done
- 4 task categories with color coding:
  - Business Growth (Green)
  - AI Agent Development (Blue)
  - White-Label SaaS (Purple)
  - AI Integration (Orange)
- Add, move, and delete tasks
- Progress tracking
- Persistent storage (JSON file)
- Reset board to defaults

## Usage

- Click **➕ Add New Task** to create new tasks
- Use **◀ ▶** buttons to move tasks between columns
- Use **🗑** to delete tasks
- Click **🔄 Reset Board** to restore default tasks