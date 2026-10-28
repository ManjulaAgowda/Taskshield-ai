# TaskShield AI (Phase 2 snapshot)

Your AI operations partner that catches what teams miss.

## Setup (Windows, VS Code terminal)
```
cd taskshield-ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
(macOS/Linux: `source .venv/bin/activate` and `cp .env.example .env`.)
Leave GEMINI_API_KEY empty for now; the AI layer arrives in Phase 5.

## Run
```
streamlit run app.py
python -m pytest
```

## Task CSV columns (data/sample_tasks.csv)
task_id (unique, e.g. T001) | task_name | description | project | assigned_owner (blank = no owner)
| status (Not Started / In Progress / Done) | priority (Critical / High / Medium / Low)
| start_date, due_date, last_updated (YYYY-MM-DD) | estimated_hours | completed_percentage (0-100)
| dependency_ids (task IDs separated by ";", blank = none) | meeting_commitment (Yes/No)
| source_reference (where the task came from)

## Fixed demo date
The analysis treats 2026-10-27 as "today" (see taskshield/config.py) so the demo is repeatable.

## Planted scenarios in the sample data
- T008 has no owner. T016 is overdue.
- T003 (due 10-30) depends on T004 (due 11-02, moved from 10-26): dependency/deadline conflict.
- T005, T006, T019 are downstream of that blocked chain.
- T012 is Critical with 15% progress and a 11-04 deadline.
- T017 and T018 (Priya) share a 10-29 deadline, on top of overdue T016.
- Budget approval appears only in meeting notes, not in the tracker.
- T001, T002, T007, T013, T015, T020 are healthy.
