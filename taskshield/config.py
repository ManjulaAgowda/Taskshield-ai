"""Central settings. Change values here instead of hunting through the code."""
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TASKS_CSV = DATA_DIR / "sample_tasks.csv"
MEETING_NOTES_TXT = DATA_DIR / "sample_meeting_notes.txt"

# The demo uses a FIXED "today" so the demo gives the same results every time.
# Set to None to use the real current date instead.
DEMO_AS_OF_DATE = date(2026, 10, 27)

# Columns every task file must have (see README for meanings).
REQUIRED_COLUMNS = [
    "task_id", "task_name", "description", "project", "assigned_owner",
    "status", "priority", "start_date", "due_date", "estimated_hours",
    "completed_percentage", "dependency_ids", "last_updated",
    "meeting_commitment", "source_reference",
]


def get_as_of_date() -> date:
    """Return the date the analysis treats as 'today'."""
    return DEMO_AS_OF_DATE or date.today()
