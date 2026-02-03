import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Data file path
DATA_FILE = "kanban_data.json"

# Default board structure
DEFAULT_DATA = {
    "columns": ["To Do (Backlog)", "In Progress", "Done"],
    "tasks": [
        {"id": 1, "title": "Develop marketing strategy to target Chicago area", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "High"},
        {"id": 2, "title": "Create website landing page for new clients", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "High"},
        {"id": 3, "title": "Implement customer feedback system", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "Medium"},
        {"id": 4, "title": "Research and select project management software", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "Medium"},
        {"id": 5, "title": "Plan expansion to 30-50 contractors in Chicago", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "High"},
        {"id": 6, "title": "Start development of autonomous AI agent", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "High"},
        {"id": 7, "title": "Investigate white-label SaaS options for other inspectors", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "Medium"},
        {"id": 8, "title": "Explore AI integration possibilities with business operations", "column": "To Do (Backlog)", "created": "2024-01-01", "priority": "Medium"},
    ]
}

def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

# Page config
st.set_page_config(
    page_title="Assure Home Inspections - Kanban Board",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .kanban-column {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        min-height: 400px;
    }
    .task-card {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .task-card-high {
        border-left-color: #e74c3c;
    }
    .task-card-medium {
        border-left-color: #f39c12;
    }
    .task-card-low {
        border-left-color: #27ae60;
    }
    .column-header {
        font-size: 1.2em;
        font-weight: bold;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .todo-header { background-color: #3498db; color: white; }
    .progress-header { background-color: #f39c12; color: white; }
    .done-header { background-color: #27ae60; color: white; }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = load_data()

# Header
st.title("🏠 Assure Home Inspections")
st.subheader("Project Kanban Board - Naperville, IL")
st.markdown("---")

# Sidebar for adding new tasks
with st.sidebar:
    st.header("➕ Add New Task")
    new_task_title = st.text_area("Task Description", height=100)
    new_task_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    new_task_column = st.selectbox("Add to Column", st.session_state.data["columns"])
    
    if st.button("Add Task", type="primary"):
        if new_task_title.strip():
            new_task = {
                "id": get_next_id(st.session_state.data["tasks"]),
                "title": new_task_title.strip(),
                "column": new_task_column,
                "created": datetime.now().strftime("%Y-%m-%d"),
                "priority": new_task_priority
            }
            st.session_state.data["tasks"].append(new_task)
            save_data(st.session_state.data)
            st.success("Task added!")
            st.rerun()
        else:
            st.error("Please enter a task description")
    
    st.markdown("---")
    st.header("📊 Statistics")
    for col in st.session_state.data["columns"]:
        count = len([t for t in st.session_state.data["tasks"] if t["column"] == col])
        st.metric(col, count)
    
    st.markdown("---")
    if st.button("🔄 Reset to Default"):
        st.session_state.data = DEFAULT_DATA.copy()
        save_data(st.session_state.data)
        st.rerun()

# Main Kanban Board
cols = st.columns(3)

column_styles = {
    "To Do (Backlog)": "todo-header",
    "In Progress": "progress-header",
    "Done": "done-header"
}

for idx, column_name in enumerate(st.session_state.data["columns"]):
    with cols[idx]:
        # Column header
        header_class = column_styles.get(column_name, "todo-header")
        st.markdown(f'<div class="column-header {header_class}">{column_name}</div>', unsafe_allow_html=True)
        
        # Get tasks for this column
        column_tasks = [t for t in st.session_state.data["tasks"] if t["column"] == column_name]
        
        # Display tasks
        for task in column_tasks:
            priority_class = f"task-card-{task['priority'].lower()}"
            
            with st.container():
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <strong>{task['title']}</strong><br>
                    <small>📅 {task['created']} | 🏷️ {task['priority']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Task actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Move left
                    current_idx = st.session_state.data["columns"].index(column_name)
                    if current_idx > 0:
                        if st.button("⬅️", key=f"left_{task['id']}"):
                            task["column"] = st.session_state.data["columns"][current_idx - 1]
                            save_data(st.session_state.data)
                            st.rerun()
                
                with col2:
                    # Delete
                    if st.button("🗑️", key=f"del_{task['id']}"):
                        st.session_state.data["tasks"] = [t for t in st.session_state.data["tasks"] if t["id"] != task["id"]]
                        save_data(st.session_state.data)
                        st.rerun()
                
                with col3:
                    # Move right
                    if current_idx < len(st.session_state.data["columns"]) - 1:
                        if st.button("➡️", key=f"right_{task['id']}"):
                            task["column"] = st.session_state.data["columns"][current_idx + 1]
                            save_data(st.session_state.data)
                            st.rerun()
                
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown("**🎯 Goals:** Grow to 30-50 contractors in Chicago | Build autonomous AI agent | Create white-label SaaS | Integrate AI with operations")