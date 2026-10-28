import pandas as pd
from datetime import datetime

def detect_risks(df: pd.DataFrame, current_date="2026-10-27") -> list:
    """Deterministic risk engine that inspects tasks for deadlines, missing owners, and blockers."""
    findings = []
    today = datetime.strptime(current_date, "%Y-%m-%d")
    
    for _, row in df.iterrows():
        task_id = row['task_id']
        task_name = row['task_name']
        due_str = row['due_date']
        status = row['status']
        owner = str(row['assigned_owner']).strip()
        priority = row['priority']
        
        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d")
            days_to_due = (due_date - today).days
        except:
            days_to_due = 0

        # 1. Missing Owner Risk
        if (not owner or owner == "nan") and status != "Completed":
            findings.append({
                "finding_id": f"FIN-OWN-{task_id}",
                "task_id": task_id,
                "task_name": task_name,
                "category": "Missing Ownership",
                "severity": "High" if priority in ["Critical", "High"] else "Medium",
                "evidence": f"Task '{task_name}' has no assigned owner.",
                "explanation": "Unowned tasks often stall due to diffusion of responsibility.",
                "recommended_action": "Assign a responsible team member immediately.",
                "source": row.get('source_reference', 'Task Tracker')
            })

        # 2. Overdue Deadline Risk
        if status != "Completed" and days_to_due < 0:
            findings.append({
                "finding_id": f"FIN-DUE-{task_id}",
                "task_id": task_id,
                "task_name": task_name,
                "category": "Overdue Deadline",
                "severity": "Critical",
                "evidence": f"Task is overdue by {abs(days_to_due)} days (Due: {due_str}).",
                "explanation": "Overdue tasks directly threaten project milestones.",
                "recommended_action": "Review blockers and adjust schedule.",
                "source": f"Due Date: {due_str}"
            })

        # 3. Blocked Risk
        if status == "Blocked":
            findings.append({
                "finding_id": f"FIN-BLK-{task_id}",
                "task_id": task_id,
                "task_name": task_name,
                "category": "Blocked Dependency",
                "severity": "High",
                "evidence": f"Task status is explicitly marked as Blocked. Prerequisites: {row.get('dependency_ids', 'None')}",
                "explanation": "Work cannot proceed until prerequisites are cleared.",
                "recommended_action": "Inspect dependency tasks and resolve blockers.",
                "source": "Task Status"
            })
               
    return findings