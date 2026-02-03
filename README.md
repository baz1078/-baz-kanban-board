# Assure Home Inspections - Kanban Board

A Streamlit-based Kanban board for managing Assure Inspections business tasks.

## Features

- 5-column Kanban board (Backlog, To Do, In Progress, Review, Done)
- Pre-loaded with strategic tasks for growing the business
- Category filtering (Business Development, AI Integration, White-label SaaS, etc.)
- Task statistics and progress tracking
- Persistent storage (JSON file)
- Color-coded categories

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Categories

1. **Business Development** - Contractor expansion, marketing, client outreach
2. **AI Integration** - Autonomous AI agent development
3. **White-label SaaS** - Platform for other inspectors
4. **Operational Efficiency** - CRM, scheduling, SOPs
5. **Quality Assurance** - Feedback, audits, training
6. **Expansion Planning** - New market research and entry

## Usage

- **Add tasks**: Use the sidebar form
- **Move tasks**: Use ◀ ▶ buttons on each card
- **Delete tasks**: Use 🗑 button
- **Filter**: Select category in sidebar
- **Reset**: Click "Reset to Default" to restore original tasks