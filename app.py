import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Data file path
DATA_FILE = "kanban_data.json"

# Default Kanban data
DEFAULT_DATA = {
    "columns": ["Backlog", "To Do", "In Progress", "Review", "Done"],
    "tasks": [
        {
            "id": 1,
            "title": "Expand Contractor Network",
            "description": "- Research potential contractors in the Chicago area.\n- Develop a contractor onboarding process.\n- Reach out to and sign up 5 new contractors.",
            "column": "Backlog",
            "priority": "High",
            "created": "2024-01-15"
        },
        {
            "id": 2,
            "title": "AI Agent Development",
            "description": "- Define AI agent's initial tasks and responsibilities.\n- Research suitable AI platforms and tools.\n- Create an outline for AI agent training and implementation.",
            "column": "Backlog",
            "priority": "High",
            "created": "2024-01-15"
        },
        {
            "id": 3,
            "title": "White-Label SaaS Creation",
            "description": "- Identify core features and functionalities required.\n- Develop a basic prototype of the platform.\n- Test the prototype with a small group of users.",
            "column": "Backlog",
            "priority": "Medium",
            "created": "2024-01-15"
        },
        {
            "id": 4,
            "title": "AI Integration with Business Operations",
            "description": "- Map out current business operations.\n- Identify areas where AI can be integrated for efficiency.\n- Develop an integration plan and timeline.",
            "column": "Backlog",
            "priority": "Medium",
            "created": "2024-01-15"
        },
        {
            "id": 5,
            "title": "Marketing Campaign for Expansion",
            "description": "- Define target audience for expansion.\n- Develop marketing materials (e.g., brochures, social media posts).\n- Plan and schedule a series of promotional activities.",
            "column": "Backlog",
            "priority": "Medium",
            "created": "2024-01-15"
        },
        {
            "id": 6,
            "title": "Customer Feedback System",
            "description": "- Design a customer feedback form or survey.\n- Implement the feedback system on the website and email communications.\n- Analyze initial feedback to identify areas for improvement.",
            "column": "Backlog",
            "priority": "Low",
            "created": "2024-01-15"
        }
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

def get_priority_color(priority):
    colors = {
        "High": "#ff4b4b",
        "Medium": "#ffa600",
        "Low": "#00cc66"
    }
    return colors.get(priority, "#808080")

def main():
    st.set_page_config(
        page_title="Assure Inspections - Kanban Board",
        page_icon="🏠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .kanban-card {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 4px solid;
    }
    .kanban-title {
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .kanban-desc {
        font-size: 12px;
        color: #888;
        margin-bottom: 8px;
    }
    .priority-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
    }
    .column-header {
        background: #2d2d2d;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 15px;
        font-weight: bold;
    }
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
    st.subheader("Strategic Kanban Board - Naperville, IL")
    st.markdown("---")
    
    # Sidebar for adding new tasks
    with st.sidebar:
        st.header("➕ Add New Task")
        
        new_title = st.text_input("Task Title")
        new_description = st.text_area("Description")
        new_column = st.selectbox("Column", st.session_state.data["columns"])
        new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        if st.button("Add Task", type="primary"):
            if new_title:
                new_id = max([t["id"] for t in st.session_state.data["tasks"]], default=0) + 1
                st.session_state.data["tasks"].append({
                    "id": new_id,
                    "title": new_title,
                    "description": new_description,
                    "column": new_column,
                    "priority": new_priority,
                    "created": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(st.session_state.data)
                st.success("Task added!")
                st.rerun()
            else:
                st.error("Please enter a title")
        
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
    columns = st.columns(len(st.session_state.data["columns"]))
    
    for idx, col_name in enumerate(st.session_state.data["columns"]):
        with columns[idx]:
            # Column header with count
            task_count = len([t for t in st.session_state.data["tasks"] if t["column"] == col_name])
            st.markdown(f'<div class="column-header">{col_name} ({task_count})</div>', unsafe_allow_html=True)
            
            # Tasks in this column
            col_tasks = [t for t in st.session_state.data["tasks"] if t["column"] == col_name]
            
            for task in col_tasks:
                priority_color = get_priority_color(task["priority"])
                
                with st.container():
                    st.markdown(f"""
                    <div class="kanban-card" style="border-left-color: {priority_color};">
                        <div class="kanban-title">{task['title']}</div>
                        <div class="kanban-desc">{task['description'][:100]}...</div>
                        <span class="priority-badge" style="background: {priority_color};">{task['priority']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Move buttons
                    col1, col2 = st.columns(2)
                    
                    current_idx = st.session_state.data["columns"].index(col_name)
                    
                    with col1:
                        if current_idx > 0:
                            if st.button("◀", key=f"left_{task['id']}"):
                                task["column"] = st.session_state.data["columns"][current_idx - 1]
                                save_data(st.session_state.data)
                                st.rerun()
                    
                    with col2:
                        if current_idx < len(st.session_state.data["columns"]) - 1:
                            if st.button("▶", key=f"right_{task['id']}"):
                                task["column"] = st.session_state.data["columns"][current_idx + 1]
                                save_data(st.session_state.data)
                                st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Delete", key=f"del_{task['id']}"):
                        st.session_state.data["tasks"] = [t for t in st.session_state.data["tasks"] if t["id"] != task["id"]]
                        save_data(st.session_state.data)
                        st.rerun()
                    
                    st.markdown("---")

if __name__ == "__main__":
    main()