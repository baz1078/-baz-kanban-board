import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Data file path
DATA_FILE = "kanban_data.json"

# Default columns
DEFAULT_COLUMNS = ["Backlog", "To Do", "In Progress", "Review", "Done"]

# Default tasks based on the plan
DEFAULT_TASKS = {
    "Backlog": [
        {"id": 1, "title": "Expand contractor network in Chicago", "category": "Business Development", "created": "2025-01-10"},
        {"id": 2, "title": "Implement targeted marketing campaign", "category": "Business Development", "created": "2025-01-10"},
        {"id": 3, "title": "Establish partnerships with real estate agencies", "category": "Business Development", "created": "2025-01-10"},
        {"id": 4, "title": "Research AI solutions for task automation", "category": "AI Integration", "created": "2025-01-10"},
        {"id": 5, "title": "Develop autonomous AI agent prototype", "category": "AI Integration", "created": "2025-01-10"},
        {"id": 6, "title": "Integrate AI with existing business operations", "category": "AI Integration", "created": "2025-01-10"},
        {"id": 7, "title": "Define product requirements for white-label SaaS", "category": "White-label SaaS", "created": "2025-01-10"},
        {"id": 8, "title": "Design user interface and experience", "category": "White-label SaaS", "created": "2025-01-10"},
        {"id": 9, "title": "Develop MVP (Minimum Viable Product)", "category": "White-label SaaS", "created": "2025-01-10"},
        {"id": 10, "title": "Streamline inspection scheduling process", "category": "Operational Efficiency", "created": "2025-01-10"},
        {"id": 11, "title": "Implement automated invoicing system", "category": "Operational Efficiency", "created": "2025-01-10"},
        {"id": 12, "title": "Enhance customer communication channels", "category": "Operational Efficiency", "created": "2025-01-10"},
        {"id": 13, "title": "Redesign website with improved SEO", "category": "Marketing & Branding", "created": "2025-01-10"},
        {"id": 14, "title": "Create content marketing strategy", "category": "Marketing & Branding", "created": "2025-01-10"},
        {"id": 15, "title": "Launch social media campaign", "category": "Marketing & Branding", "created": "2025-01-10"},
    ],
    "To Do": [],
    "In Progress": [],
    "Review": [],
    "Done": []
}

CATEGORY_COLORS = {
    "Business Development": "#4CAF50",
    "AI Integration": "#2196F3",
    "White-label SaaS": "#9C27B0",
    "Operational Efficiency": "#FF9800",
    "Marketing & Branding": "#E91E63"
}

def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_TASKS.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_next_id(data):
    all_ids = []
    for column in data.values():
        for task in column:
            all_ids.append(task["id"])
    return max(all_ids, default=0) + 1

def main():
    st.set_page_config(
        page_title="Assure Inspections - Kanban Board",
        page_icon="🏠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .kanban-column {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 10px;
        min-height: 500px;
    }
    .column-header {
        font-weight: bold;
        font-size: 1.2em;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
    }
    .task-card {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2196F3;
    }
    .category-badge {
        font-size: 0.75em;
        padding: 2px 8px;
        border-radius: 12px;
        color: white;
        display: inline-block;
        margin-top: 5px;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🏠 Assure Home Inspections")
    st.subheader("Project Kanban Board")
    
    # Load data
    if "kanban_data" not in st.session_state:
        st.session_state.kanban_data = load_data()
    
    # Sidebar for adding new tasks
    with st.sidebar:
        st.header("➕ Add New Task")
        
        new_title = st.text_input("Task Title")
        new_category = st.selectbox(
            "Category",
            list(CATEGORY_COLORS.keys())
        )
        new_column = st.selectbox(
            "Add to Column",
            DEFAULT_COLUMNS
        )
        
        if st.button("Add Task", type="primary"):
            if new_title:
                new_task = {
                    "id": get_next_id(st.session_state.kanban_data),
                    "title": new_title,
                    "category": new_category,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.kanban_data[new_column].append(new_task)
                save_data(st.session_state.kanban_data)
                st.success("Task added!")
                st.rerun()
            else:
                st.error("Please enter a task title")
        
        st.divider()
        
        # Filter by category
        st.header("🔍 Filter")
        filter_category = st.selectbox(
            "Filter by Category",
            ["All"] + list(CATEGORY_COLORS.keys())
        )
        
        st.divider()
        
        # Stats
        st.header("📊 Statistics")
        total_tasks = sum(len(tasks) for tasks in st.session_state.kanban_data.values())
        done_tasks = len(st.session_state.kanban_data.get("Done", []))
        
        st.metric("Total Tasks", total_tasks)
        st.metric("Completed", done_tasks)
        if total_tasks > 0:
            st.progress(done_tasks / total_tasks)
        
        st.divider()
        
        if st.button("🔄 Reset to Default"):
            st.session_state.kanban_data = DEFAULT_TASKS.copy()
            save_data(st.session_state.kanban_data)
            st.rerun()
    
    # Main Kanban Board
    cols = st.columns(5)
    
    column_colors = {
        "Backlog": "#9E9E9E",
        "To Do": "#2196F3",
        "In Progress": "#FF9800",
        "Review": "#9C27B0",
        "Done": "#4CAF50"
    }
    
    for idx, column_name in enumerate(DEFAULT_COLUMNS):
        with cols[idx]:
            # Column header
            st.markdown(
                f'<div class="column-header" style="background-color: {column_colors[column_name]}; color: white;">'
                f'{column_name} ({len(st.session_state.kanban_data.get(column_name, []))})</div>',
                unsafe_allow_html=True
            )
            
            # Container for tasks
            with st.container():
                tasks = st.session_state.kanban_data.get(column_name, [])
                
                for task in tasks:
                    # Apply filter
                    if filter_category != "All" and task["category"] != filter_category:
                        continue
                    
                    category_color = CATEGORY_COLORS.get(task["category"], "#757575")
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="task-card" style="border-left-color: {category_color};">
                            <strong>{task['title']}</strong>
                            <br>
                            <span class="category-badge" style="background-color: {category_color};">
                                {task['category']}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Move buttons
                        col1, col2, col3 = st.columns([1, 1, 1])
                        
                        current_idx = DEFAULT_COLUMNS.index(column_name)
                        
                        with col1:
                            if current_idx > 0:
                                if st.button("◀", key=f"left_{task['id']}"):
                                    prev_column = DEFAULT_COLUMNS[current_idx - 1]
                                    st.session_state.kanban_data[column_name].remove(task)
                                    st.session_state.kanban_data[prev_column].append(task)
                                    save_data(st.session_state.kanban_data)
                                    st.rerun()
                        
                        with col2:
                            if st.button("🗑️", key=f"del_{task['id']}"):
                                st.session_state.kanban_data[column_name].remove(task)
                                save_data(st.session_state.kanban_data)
                                st.rerun()
                        
                        with col3:
                            if current_idx < len(DEFAULT_COLUMNS) - 1:
                                if st.button("▶", key=f"right_{task['id']}"):
                                    next_column = DEFAULT_COLUMNS[current_idx + 1]
                                    st.session_state.kanban_data[column_name].remove(task)
                                    st.session_state.kanban_data[next_column].append(task)
                                    save_data(st.session_state.kanban_data)
                                    st.rerun()
                        
                        st.markdown("---")
    
    # Footer
    st.divider()
    st.caption("🏠 Assure Home Inspections - Naperville, Illinois | Goal: 30-50 contractors in Chicago")

if __name__ == "__main__":
    main()