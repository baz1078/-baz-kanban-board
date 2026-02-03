import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Data file path
DATA_FILE = "kanban_data.json"

# Default columns
DEFAULT_COLUMNS = ["Backlog", "To Do", "In Progress", "Review", "Done"]

# Default tasks from the plan
DEFAULT_TASKS = {
    "Backlog": [
        {"id": 1, "title": "Expand contractor network to 30 in Chicago by Q2", "category": "Business Development", "created": "2025-01-13"},
        {"id": 2, "title": "Identify and reach out to potential clients in Naperville area", "category": "Business Development", "created": "2025-01-13"},
        {"id": 3, "title": "Develop marketing materials (brochures, website content)", "category": "Business Development", "created": "2025-01-13"},
        {"id": 4, "title": "Research AI technologies for home inspection industry", "category": "AI Integration", "created": "2025-01-13"},
        {"id": 5, "title": "Define AI project scope and requirements", "category": "AI Integration", "created": "2025-01-13"},
        {"id": 6, "title": "Develop prototype of autonomous AI agent", "category": "AI Integration", "created": "2025-01-13"},
        {"id": 7, "title": "Test and iterate AI agent based on feedback", "category": "AI Integration", "created": "2025-01-13"},
        {"id": 8, "title": "Integrate AI with business operations (CRM, scheduling, reporting)", "category": "AI Integration", "created": "2025-01-13"},
        {"id": 9, "title": "Identify key features for white-label SaaS platform", "category": "White-label SaaS", "created": "2025-01-13"},
        {"id": 10, "title": "Develop MVP for white-label SaaS platform", "category": "White-label SaaS", "created": "2025-01-13"},
        {"id": 11, "title": "Test and iterate platform based on user feedback", "category": "White-label SaaS", "created": "2025-01-13"},
        {"id": 12, "title": "Launch marketing campaign for white-label SaaS", "category": "White-label SaaS", "created": "2025-01-13"},
        {"id": 13, "title": "Implement CRM system for client/contractor management", "category": "Operational Efficiency", "created": "2025-01-13"},
        {"id": 14, "title": "Streamline scheduling with automated tools", "category": "Operational Efficiency", "created": "2025-01-13"},
        {"id": 15, "title": "Develop standard operating procedures for inspections", "category": "Operational Efficiency", "created": "2025-01-13"},
        {"id": 16, "title": "Train contractors on new processes and technologies", "category": "Operational Efficiency", "created": "2025-01-13"},
        {"id": 17, "title": "Implement client feedback/rating system", "category": "Quality Assurance", "created": "2025-01-13"},
        {"id": 18, "title": "Set up inspection report quality review process", "category": "Quality Assurance", "created": "2025-01-13"},
        {"id": 19, "title": "Create contractor performance audit system", "category": "Quality Assurance", "created": "2025-01-13"},
        {"id": 20, "title": "Develop ongoing contractor training program", "category": "Quality Assurance", "created": "2025-01-13"},
        {"id": 21, "title": "Research potential new markets for expansion", "category": "Expansion Planning", "created": "2025-01-13"},
        {"id": 22, "title": "Develop business plan for market expansion", "category": "Expansion Planning", "created": "2025-01-13"},
        {"id": 23, "title": "Build relationships with real estate agents in target markets", "category": "Expansion Planning", "created": "2025-01-13"},
        {"id": 24, "title": "Establish operations in new markets", "category": "Expansion Planning", "created": "2025-01-13"},
    ],
    "To Do": [],
    "In Progress": [],
    "Review": [],
    "Done": []
}

CATEGORIES = [
    "Business Development",
    "AI Integration", 
    "White-label SaaS",
    "Operational Efficiency",
    "Quality Assurance",
    "Expansion Planning"
]

CATEGORY_COLORS = {
    "Business Development": "#FF6B6B",
    "AI Integration": "#4ECDC4",
    "White-label SaaS": "#45B7D1",
    "Operational Efficiency": "#96CEB4",
    "Quality Assurance": "#FFEAA7",
    "Expansion Planning": "#DDA0DD"
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
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        min-height: 500px;
    }
    .kanban-header {
        font-weight: bold;
        font-size: 1.1em;
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
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        border-left: 4px solid #4ECDC4;
    }
    .category-badge {
        font-size: 0.75em;
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-bottom: 5px;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🏠 Assure Home Inspections")
    st.subheader("Project Kanban Board")
    
    # Initialize data
    if "data" not in st.session_state:
        st.session_state.data = load_data()
    
    # Sidebar for adding tasks
    with st.sidebar:
        st.header("➕ Add New Task")
        
        new_title = st.text_input("Task Title")
        new_category = st.selectbox("Category", CATEGORIES)
        new_column = st.selectbox("Add to Column", DEFAULT_COLUMNS)
        
        if st.button("Add Task", type="primary"):
            if new_title:
                new_task = {
                    "id": get_next_id(st.session_state.data),
                    "title": new_title,
                    "category": new_category,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.data[new_column].append(new_task)
                save_data(st.session_state.data)
                st.success("Task added!")
                st.rerun()
            else:
                st.error("Please enter a task title")
        
        st.divider()
        
        # Filter by category
        st.header("🔍 Filter")
        filter_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
        
        st.divider()
        
        # Stats
        st.header("📊 Statistics")
        total_tasks = sum(len(tasks) for tasks in st.session_state.data.values())
        done_tasks = len(st.session_state.data.get("Done", []))
        
        st.metric("Total Tasks", total_tasks)
        st.metric("Completed", done_tasks)
        if total_tasks > 0:
            st.progress(done_tasks / total_tasks)
            st.caption(f"{(done_tasks/total_tasks)*100:.1f}% complete")
        
        st.divider()
        
        # Category breakdown
        st.header("📁 By Category")
        for cat in CATEGORIES:
            count = sum(1 for col in st.session_state.data.values() for task in col if task.get("category") == cat)
            color = CATEGORY_COLORS.get(cat, "#gray")
            st.markdown(f"<span style='color:{color}'>●</span> {cat}: **{count}**", unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🔄 Reset to Default"):
            st.session_state.data = DEFAULT_TASKS.copy()
            save_data(st.session_state.data)
            st.rerun()
    
    # Main Kanban Board
    cols = st.columns(len(DEFAULT_COLUMNS))
    
    column_colors = {
        "Backlog": "#6c757d",
        "To Do": "#007bff",
        "In Progress": "#ffc107",
        "Review": "#17a2b8",
        "Done": "#28a745"
    }
    
    for idx, (col, column_name) in enumerate(zip(cols, DEFAULT_COLUMNS)):
        with col:
            color = column_colors.get(column_name, "#6c757d")
            task_count = len(st.session_state.data.get(column_name, []))
            
            st.markdown(f"""
            <div class="kanban-header" style="background-color: {color}; color: white;">
                {column_name} ({task_count})
            </div>
            """, unsafe_allow_html=True)
            
            tasks = st.session_state.data.get(column_name, [])
            
            # Filter tasks
            if filter_category != "All":
                tasks = [t for t in tasks if t.get("category") == filter_category]
            
            for task in tasks:
                cat_color = CATEGORY_COLORS.get(task.get("category", ""), "#gray")
                
                with st.container():
                    st.markdown(f"""
                    <div class="task-card" style="border-left-color: {cat_color};">
                        <span class="category-badge" style="background-color: {cat_color}20; color: {cat_color};">
                            {task.get('category', 'General')}
                        </span>
                        <div style="font-weight: 500; margin-top: 5px;">{task['title']}</div>
                        <div style="font-size: 0.75em; color: #666; margin-top: 5px;">
                            Created: {task.get('created', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Move buttons
                    button_cols = st.columns(4)
                    
                    current_idx = DEFAULT_COLUMNS.index(column_name)
                    
                    with button_cols[0]:
                        if current_idx > 0:
                            if st.button("◀", key=f"left_{task['id']}_{column_name}", help="Move left"):
                                new_col = DEFAULT_COLUMNS[current_idx - 1]
                                st.session_state.data[column_name].remove(task)
                                st.session_state.data[new_col].append(task)
                                save_data(st.session_state.data)
                                st.rerun()
                    
                    with button_cols[1]:
                        if current_idx < len(DEFAULT_COLUMNS) - 1:
                            if st.button("▶", key=f"right_{task['id']}_{column_name}", help="Move right"):
                                new_col = DEFAULT_COLUMNS[current_idx + 1]
                                st.session_state.data[column_name].remove(task)
                                st.session_state.data[new_col].append(task)
                                save_data(st.session_state.data)
                                st.rerun()
                    
                    with button_cols[3]:
                        if st.button("🗑", key=f"del_{task['id']}_{column_name}", help="Delete"):
                            st.session_state.data[column_name].remove(task)
                            save_data(st.session_state.data)
                            st.rerun()
                    
                    st.markdown("---")

if __name__ == "__main__":
    main()