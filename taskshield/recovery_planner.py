def generate_recovery_plans(findings):
    """Generates practical recovery actions for each detected risk finding."""
    plans = []
    for f in findings:
        action_text = f.get('recommended_action', 'Review and resolve issue.')
        plans.append({
            "action_id": f"ACT-{f['finding_id']}",
            "finding_id": f['finding_id'],
            "task_id": f['task_id'],
            "task_name": f['task_name'],
            "proposed_action": action_text,
            "reason": f['explanation'],
            "requires_approval": True,
            "status": "Pending"
        })
    return plans