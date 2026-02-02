import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Assure Inspections - Kanban Board",
    page_icon="🏠",
    layout="wide"
)

# Data file
DATA_FILE = "kanban_data.json"

# Default columns
DEFAULT_COLUMNS = ["Backlog", "To Do", "In Progress", "Review", "Done"]

# Default tasks from the plan
DEFAULT_TASKS = {
    "Backlog": [
        {"id": 1, "title": "Market Research", "description": "Identify potential contractors in Chicago area.\nAnalyze competitors and their offerings.", "priority": "high", "created": "2025-01-10"},
        {"id": 2, "title": "Business Development", "description": "Develop partnership proposals for local real estate agencies.\nCreate marketing materials (brochures, digital ads).", "priority": "high", "created": "2025-01-10"},
        {"id": 3, "title": "AI Integration", "description": "Research AI tools for task automation.\nPlan integration of AI with existing business operations.", "priority": "high", "created": "2025-01-10"},
        {"id": 4, "title": "White-Label SaaS Development", "description": "Define features and requirements.\nDevelop MVP (Minimum Viable Product).", "priority": "high", "created": "2025-01-10"},
        {"id": 5, "title": "Training & Onboarding", "description": "Create training materials for new contractors.\nDevelop onboarding process for new hires.", "priority": "medium", "created": "2025-01-10"},
        {"id": 6, "title": "Customer Feedback System", "description": "Implement a system to collect customer feedback.\nAnalyze feedback to improve services.", "priority": "medium", "created": "2025-01-10"},
        {"id": 7, "title": "Website Optimization", "description": "Redesign website for better user experience.\nImprove SEO for higher search engine rankings.", "priority": "medium", "created": "2025-01-10"},
        {"id": 8, "title": "Expand Service Offerings", "description": "Research and develop new inspection services.\nUpdate service listings on the website.", "priority": "low", "created": "2025-01-10"},
        {"id": 9, "title": "Build Local Network", "description": "Attend local business events and networking meetings.\nCollaborate with other local businesses.", "priority": "medium", "created": "2025-01-10"},
        {"id": 10, "title": "Legal & Compliance", "description": "Ensure all contracts are up-to-date and compliant.\nReview insurance policies for adequate coverage.", "priority": "high", "created": "2025-01-10"},
    ],
    "To Do": [],
    "In Progress": [],
    "Review": [],
    "Done": []
}

def load_data():
    """Load kanban data from file"""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"columns": DEFAULT_COLUMNS, "tasks": DEFAULT_TASKS, "next_id": 11}

def save_data(data):
    """Save kanban data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_priority_color(priority):
    """Get color based on priority"""
    colors = {
        "high": "#ff4b4b",
        "medium": "#ffa500",
        "low": "#00cc00"
    }
    return colors.get(priority, "#gray")

def render_task_card(task, column, data):
    """Render a single task card"""
    priority_color = get_priority_color(task.get("priority", "medium"))
    
    with st.container():
        st.markdown(f"""
        <div style="
            background: #1e1e1e;
            border-left: 4px solid {priority_color};
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        ">
            <strong style="color: white;">{task['title']}</strong>
            <p style="color: #aaa; font-size: 12px; margin: 5px 0;">{task.get('description', '')[:100]}...</p>
            <span style="
                background: {priority_color};
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 10px;
            ">{task.get('priority', 'medium').upper()}</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Move buttons
        col_idx = data["columns"].index(column)
        
        with col1:
            if col_idx > 0:
                if st.button("◀", key=f"left_{task['id']}_{column}", help="Move left"):
                    move_task(data, task['id'], column, data["columns"][col_idx - 1])
                    st.rerun()
        
        with col2:
            if st.button("🗑️", key=f"del_{task['id']}_{column}", help="Delete"):
                delete_task(data, task['id'], column)
                st.rerun()
        
        with col3:
            if col_idx < len(data["columns"]) - 1:
                if st.button("▶", key=f"right_{task['id']}_{column}", help="Move right"):
                    move_task(data, task['id'], column, data["columns"][col_idx + 1])
                    st.rerun()

def move_task(data, task_id, from_col, to_col):
    """Move task between columns"""
    task = None
    for t in data["tasks"][from_col]:
        if t["id"] == task_id:
            task = t
            break
    
    if task:
        data["tasks"][from_col].remove(task)
        data["tasks"][to_col].append(task)
        save_data(data)

def delete_task(data, task_id, column):
    """Delete a task"""
    data["tasks"][column] = [t for t in data["tasks"][column] if t["id"] != task_id]
    save_data(data)

def add_task(data, column, title, description, priority):
    """Add a new task"""
    task = {
        "id": data["next_id"],
        "title": title,
        "description": description,
        "priority": priority,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    data["tasks"][column].append(task)
    data["next_id"] += 1
    save_data(data)

# Main app
st.title("🏠 Assure Home Inspections - Kanban Board")
st.markdown("*Growing to 30-50 contractors in Chicago*")
st.divider()

# Load data
data = load_data()

# Add new task section
with st.expander("➕ Add New Task", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        new_title = st.text_input("Task Title")
        new_column = st.selectbox("Add to Column", data["columns"])
    with col2:
        new_priority = st.selectbox("Priority", ["high", "medium", "low"])
        new_description = st.text_area("Description", height=100)
    
    if st.button("Add Task", type="primary"):
        if new_title:
            add_task(data, new_column, new_title, new_description, new_priority)
            st.success(f"Added '{new_title}' to {new_column}")
            st.rerun()
        else:
            st.error("Please enter a task title")

st.divider()

# Kanban board
cols = st.columns(len(data["columns"]))

for idx, column in enumerate(data["columns"]):
    with cols[idx]:
        task_count = len(data["tasks"].get(column, []))
        st.markdown(f"""
        <div style="
            background: #262730;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 15px;
        ">
            <h3 style="margin: 0; color: white;">{column}</h3>
            <span style="color: #888;">{task_count} tasks</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Render tasks
        for task in data["tasks"].get(column, []):
            render_task_card(task, column, data)

# Stats section
st.divider()
st.subheader("📊 Board Statistics")

stat_cols = st.columns(5)
for idx, column in enumerate(data["columns"]):
    with stat_cols[idx]:
        count = len(data["tasks"].get(column, []))
        st.metric(column, count)

# Progress bar
total_tasks = sum(len(data["tasks"].get(col, [])) for col in data["columns"])
done_tasks = len(data["tasks"].get("Done", []))
if total_tasks > 0:
    progress = done_tasks / total_tasks
    st.progress(progress, text=f"Overall Progress: {done_tasks}/{total_tasks} tasks completed ({progress*100:.0f}%)")

# Reset button
st.divider()
if st.button("🔄 Reset to Default", type="secondary"):
    save_data({"columns": DEFAULT_COLUMNS, "tasks": DEFAULT_TASKS, "next_id": 11})
    st.success("Board reset to default!")
    st.rerun()