import streamlit as st
import json
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Assure Inspections - Kanban Board", layout="wide")

# Data file
DATA_FILE = "kanban_data.json"

# Default columns
DEFAULT_COLUMNS = ["Backlog", "To Do", "In Progress", "Review", "Done"]

# Default tasks for backlog
DEFAULT_TASKS = {
    "Backlog": [
        {"id": 1, "title": "Identify and reach out to potential contractors in Chicago", "category": "Business Growth", "created": "2024-01-01"},
        {"id": 2, "title": "Develop a referral program for existing clients", "category": "Business Growth", "created": "2024-01-01"},
        {"id": 3, "title": "Create targeted online ads to attract new clients", "category": "Business Growth", "created": "2024-01-01"},
        {"id": 4, "title": "Research AI platforms and tools suitable for task automation", "category": "AI Agent Development", "created": "2024-01-01"},
        {"id": 5, "title": "Define key tasks for the AI agent to execute autonomously", "category": "AI Agent Development", "created": "2024-01-01"},
        {"id": 6, "title": "Plan and implement user training for the AI agent", "category": "AI Agent Development", "created": "2024-01-01"},
        {"id": 7, "title": "Identify features and functionalities required for the platform", "category": "White-Label SaaS", "created": "2024-01-01"},
        {"id": 8, "title": "Develop a prototype or MVP of the white-label SaaS", "category": "White-Label SaaS", "created": "2024-01-01"},
        {"id": 9, "title": "Gather feedback from potential users and iterate on the design", "category": "White-Label SaaS", "created": "2024-01-01"},
        {"id": 10, "title": "Map out current business processes that can be automated", "category": "AI Integration", "created": "2024-01-01"},
        {"id": 11, "title": "Plan and implement AI integration into these processes", "category": "AI Integration", "created": "2024-01-01"},
        {"id": 12, "title": "Monitor and optimize AI performance in daily operations", "category": "AI Integration", "created": "2024-01-01"},
    ],
    "To Do": [],
    "In Progress": [],
    "Review": [],
    "Done": []
}

# Category colors
CATEGORY_COLORS = {
    "Business Growth": "#4CAF50",
    "AI Agent Development": "#2196F3",
    "White-Label SaaS": "#9C27B0",
    "AI Integration": "#FF9800"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_TASKS.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_id(data):
    max_id = 0
    for column in data.values():
        for task in column:
            if task["id"] > max_id:
                max_id = task["id"]
    return max_id + 1

# Initialize session state
if "kanban_data" not in st.session_state:
    st.session_state.kanban_data = load_data()

if "show_add_task" not in st.session_state:
    st.session_state.show_add_task = False

# Custom CSS
st.markdown("""
<style>
    .kanban-column {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 10px;
        min-height: 500px;
    }
    .kanban-header {
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        color: white;
    }
    .task-card {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid;
    }
    .task-title {
        font-size: 14px;
        margin-bottom: 8px;
    }
    .task-category {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        color: white;
        display: inline-block;
    }
    .column-count {
        font-size: 12px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏠 Assure Home Inspections - Kanban Board")
st.markdown("*Growing to 30-50 contractors in Chicago | AI-Powered Operations*")
st.divider()

# Add task button
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    if st.button("➕ Add New Task", type="primary"):
        st.session_state.show_add_task = not st.session_state.show_add_task

with col2:
    if st.button("🔄 Reset Board"):
        st.session_state.kanban_data = DEFAULT_TASKS.copy()
        save_data(st.session_state.kanban_data)
        st.rerun()

# Add task form
if st.session_state.show_add_task:
    with st.expander("Add New Task", expanded=True):
        with st.form("add_task_form"):
            task_title = st.text_input("Task Title")
            task_category = st.selectbox("Category", list(CATEGORY_COLORS.keys()))
            task_column = st.selectbox("Add to Column", DEFAULT_COLUMNS)
            
            if st.form_submit_button("Add Task"):
                if task_title:
                    new_task = {
                        "id": get_next_id(st.session_state.kanban_data),
                        "title": task_title,
                        "category": task_category,
                        "created": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.kanban_data[task_column].append(new_task)
                    save_data(st.session_state.kanban_data)
                    st.session_state.show_add_task = False
                    st.rerun()
                else:
                    st.error("Please enter a task title")

st.divider()

# Column header colors
COLUMN_COLORS = {
    "Backlog": "#607D8B",
    "To Do": "#2196F3",
    "In Progress": "#FF9800",
    "Review": "#9C27B0",
    "Done": "#4CAF50"
}

# Kanban board
columns = st.columns(5)

for idx, col_name in enumerate(DEFAULT_COLUMNS):
    with columns[idx]:
        # Column header
        task_count = len(st.session_state.kanban_data[col_name])
        st.markdown(f"""
        <div class="kanban-header" style="background-color: {COLUMN_COLORS[col_name]};">
            {col_name} <span class="column-count">({task_count})</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Tasks container
        st.markdown('<div class="kanban-column">', unsafe_allow_html=True)
        
        for task in st.session_state.kanban_data[col_name]:
            category_color = CATEGORY_COLORS.get(task["category"], "#666")
            
            st.markdown(f"""
            <div class="task-card" style="border-left-color: {category_color};">
                <div class="task-title">{task["title"]}</div>
                <span class="task-category" style="background-color: {category_color};">{task["category"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Move buttons
            move_cols = st.columns(4)
            
            if idx > 0:
                with move_cols[0]:
                    if st.button("◀", key=f"left_{task['id']}", help="Move left"):
                        st.session_state.kanban_data[col_name].remove(task)
                        st.session_state.kanban_data[DEFAULT_COLUMNS[idx-1]].append(task)
                        save_data(st.session_state.kanban_data)
                        st.rerun()
            
            if idx < 4:
                with move_cols[1]:
                    if st.button("▶", key=f"right_{task['id']}", help="Move right"):
                        st.session_state.kanban_data[col_name].remove(task)
                        st.session_state.kanban_data[DEFAULT_COLUMNS[idx+1]].append(task)
                        save_data(st.session_state.kanban_data)
                        st.rerun()
            
            with move_cols[3]:
                if st.button("🗑", key=f"del_{task['id']}", help="Delete"):
                    st.session_state.kanban_data[col_name].remove(task)
                    save_data(st.session_state.kanban_data)
                    st.rerun()
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Sidebar stats
with st.sidebar:
    st.header("📊 Board Statistics")
    
    total_tasks = sum(len(tasks) for tasks in st.session_state.kanban_data.values())
    completed_tasks = len(st.session_state.kanban_data["Done"])
    
    st.metric("Total Tasks", total_tasks)
    st.metric("Completed", completed_tasks)
    
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.caption(f"{progress*100:.1f}% Complete")
    
    st.divider()
    st.header("📁 Tasks by Category")
    
    category_counts = {}
    for column in st.session_state.kanban_data.values():
        for task in column:
            cat = task["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for cat, count in category_counts.items():
        color = CATEGORY_COLORS.get(cat, "#666")
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 12px; height: 12px; background-color: {color}; border-radius: 50%; margin-right: 8px;"></div>
            <span>{cat}: {count}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.header("🎯 Goals")
    st.markdown("""
    - 📈 Grow to 30-50 contractors
    - 🤖 Build autonomous AI agent
    - 💼 Create white-label SaaS
    - ⚡ Integrate AI with operations
    """)