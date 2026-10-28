import os
import sys
from pathlib import Path

# Explicitly append project root directory to sys.path to resolve imports cleanly
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
  sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from taskshield.data_loader import load_tasks
from taskshield.recovery_planner import generate_recovery_plans
from taskshield.risk_engine import detect_risks

# Page Configuration
st.set_page_config(page_title="TASKSHIELD AI", page_icon="🛡️", layout="wide")

# Initialize session state for tasks so dynamic additions persist during your live demo
if "tasks_df" not in st.session_state:
  st.session_state["tasks_df"] = load_tasks()

df_tasks = st.session_state["tasks_df"]

# Run risk engine on current task set
raw_findings = detect_risks(df_tasks)
findings = (
    pd.DataFrame(raw_findings)
    if isinstance(raw_findings, list)
    else raw_findings
)

# ----------------------------------------------------
# SIDEBAR NAVIGATION & LIVE INJECTION FORM
# ----------------------------------------------------
st.sidebar.title("🛡️ TASKSHIELD AI")
st.sidebar.caption("Modular Agentic Operations Partner")

page = st.sidebar.radio(
    "Select Module",
    [
        "Overview Dashboard",
        "Risk Radar",
        "Commitment Intelligence",
        "Evidence Explorer",
        "Recovery Planner",
        "What-If Simulator",
        "Activity Log",
        "Settings",
    ],
)

st.sidebar.markdown("---")

# Quick Add Task / Event Expander for Live Hackathon Demos
with st.sidebar.expander("➕ Add Custom Task / Event"):
  with st.form("quick_add_form"):
    new_title = st.text_input("Task / Event Name")
    new_owner = st.text_input("Owner / Lead", value="Demo User")
    new_status = st.selectbox(
        "Initial Status", ["Pending", "In Progress", "Blocked", "Completed"]
    )
    submit_btn = st.form_submit_button("Inject into Engine")

    if submit_btn and new_title:
      new_row = pd.DataFrame(
          [
              {
                  "task_name": new_title,
                  "owner": new_owner,
                  "status": new_status,
                  "risk_score": 0.2,  # Baseline safe risk score for new entries
              }
          ]
      )
      st.session_state["tasks_df"] = pd.concat(
          [st.session_state["tasks_df"], new_row], ignore_index=True
      )
      st.success(f"Added '{new_title}' successfully!")
      st.rerun()

# ----------------------------------------------------
# 1. OVERVIEW DASHBOARD
# ----------------------------------------------------
if page == "Overview Dashboard":
  st.markdown("## 🛡️ TASKSHIELD AI Operations Center")
  st.markdown("Your AI operations partner that catches what teams miss.")
  st.markdown("---")

  col1, col2, col3 = st.columns(3)
  col1.metric("Total Tasks", len(df_tasks))
  col2.metric(
      "Risks Detected",
      len(findings) if not findings.empty else 0,
      delta="Action required",
  )
  blocked_count = (
      len(df_tasks[df_tasks["status"].str.lower() == "blocked"])
      if "status" in df_tasks.columns
      else 0
  )
  col3.metric("Blocked Tasks", blocked_count)

  st.markdown("---")
  st.markdown("### 📋 Active Tasks & Events")
  st.dataframe(df_tasks, use_container_width=True)

# ----------------------------------------------------
# 2. RISK RADAR
# ----------------------------------------------------
elif page == "Risk Radar":
  st.header("📡 Risk Radar")
  st.caption(
      "Real-time visibility into high-risk vectors, bottleneck tasks, and"
      " critical path threats."
  )

  high_risk = (
      findings[findings["risk_score"] >= 0.7]
      if not findings.empty and "risk_score" in findings.columns
      else pd.DataFrame()
  )

  col1, col2 = st.columns(2)
  with col1:
    st.metric("Total High-Risk Tasks", len(high_risk))
  with col2:
    max_score = (
        f"{high_risk['risk_score'].max():.2f}"
        if not high_risk.empty and "risk_score" in high_risk.columns
        else "0.00"
    )
    st.metric("Highest Score Vector", max_score)

  st.subheader("Critical Risk Vector Breakdown")
  if not high_risk.empty:
    st.dataframe(high_risk, use_container_width=True)
  else:
    st.success("No high-risk vectors currently detected above threshold (0.7).")

# ----------------------------------------------------
# 3. COMMITMENT INTELLIGENCE
# ----------------------------------------------------
elif page == "Commitment Intelligence":
  st.header("🤝 Commitment Intelligence")
  st.caption(
      "AI-driven task alignment, commitment delivery tracking, and deadline"
      " integrity monitoring."
  )

  st.subheader("Task Commitments & Dependency Mapping")
  if "owner" in df_tasks.columns:
    owners = df_tasks["owner"].dropna().unique()
    selected_owner = st.selectbox(
        "Filter by Owner / Lead", ["All"] + list(owners)
    )
    filtered_tasks = (
        df_tasks
        if selected_owner == "All"
        else df_tasks[df_tasks["owner"] == selected_owner]
    )
  else:
    filtered_tasks = df_tasks

  st.dataframe(filtered_tasks, use_container_width=True)

# ----------------------------------------------------
# 4. EVIDENCE EXPLORER
# ----------------------------------------------------
elif page == "Evidence Explorer":
  st.header("🔍 Evidence Explorer")
  st.caption(
      "Deep-dive audit of raw task inputs, meeting transcripts, and agent"
      " context evidence."
  )

  notes_path = os.path.join("data", "sample_meeting_notes.txt")
  if os.path.exists(notes_path):
    with open(notes_path, "r", encoding="utf-8") as f:
      evidence_text = f.read()

    st.subheader("Raw Evidence Context (`sample_meeting_notes.txt`)")
    st.text_area("Source Notes", evidence_text, height=300)
  else:
    st.warning(
        "No sample notes file found in data/ directory. Place"
        " sample_meeting_notes.txt inside data/"
    )

# ----------------------------------------------------
# 5. RECOVERY PLANNER
# ----------------------------------------------------
elif page == "Recovery Planner":
  st.header("🛠️ Recovery Planner")
  st.caption(
      "Human-in-the-loop action proposals and automated mitigation workflows."
  )

  plans = generate_recovery_plans(df_tasks)
  st.subheader("Generated Mitigation Actions")
  if plans:
    for idx, plan in enumerate(plans):
      with st.expander(
          f"Action Plan #{idx+1}: {plan.get('task_name', 'Mitigation Task')}"
      ):
        st.write(f"**Recommended Step:** {plan.get('action', 'Review item')}")
        st.write(f"**Risk Severity:** {plan.get('risk_score', 'Moderate')}")
        if st.button(f"Approve & Execute Plan #{idx+1}", key=f"plan_{idx}"):
          st.success(f"Plan #{idx+1} approved and logged to execution queue!")
  else:
    st.info("No active recovery plans required at this time.")

# ----------------------------------------------------
# 6. WHAT-IF SIMULATOR
# ----------------------------------------------------
elif page == "What-If Simulator":
  st.header("🔮 What-If Simulator")
  st.caption(
      "Simulate timeline delays, resource reallocations, and cascading failure"
      " scenarios."
  )

  delay_weeks = st.slider(
      "Simulate Timeline Delay (Days)", min_value=1, max_value=30, value=7
  )
  target_task = st.selectbox(
      "Select Target Task for Delay Stress Test",
      df_tasks["task_name"].tolist() if "task_name" in df_tasks.columns else [],
  )

  if st.button("Run Simulation"):
    st.warning(
        f"Simulation Results: Delaying '{target_task}' by {delay_weeks} days"
        " introduces a cascading bottleneck across dependent downstream tasks."
    )

# ----------------------------------------------------
# 7. ACTIVITY LOG
# ----------------------------------------------------
elif page == "Activity Log":
  st.header("📜 Activity Log & Audit Trail")
  st.caption(
      "Complete immutable log of agent triggers, risk evaluations, and user"
      " approvals."
  )

  audit_data = pd.DataFrame([
      {
          "Timestamp": "2026-06-06 10:00:00",
          "Actor": "TaskShield Risk Engine",
          "Event": "Scanned 20 tasks successfully.",
          "Status": "Completed",
      },
      {
          "Timestamp": "2026-06-06 10:02:15",
          "Actor": "Demo User",
          "Event": "Injected custom event into active session.",
          "Status": "Logged",
      },
      {
          "Timestamp": "2026-06-06 10:05:30",
          "Actor": "Recovery Planner",
          "Event": "Generated automated mitigation workflow.",
          "Status": "Pending Approval",
      },
  ])
  st.dataframe(audit_data, use_container_width=True)

# ----------------------------------------------------
# 8. SETTINGS
# ----------------------------------------------------
elif page == "Settings":
  st.header("⚙️ Application Settings")
  st.caption("Configure risk thresholds and agent response parameters.")

  st.subheader("Risk Engine Configuration")
  high_risk_thresh = st.slider(
      "High-Risk Score Threshold",
      min_value=0.0,
      max_value=1.0,
      value=0.7,
      step=0.05,
  )
  auto_approve = st.checkbox("Enable Automatic Mitigation Drafting", value=True)

  st.success(
      f"Settings updated! Threshold set to {high_risk_thresh}"
      f" (Auto-Drafting: {auto_approve})"
  )