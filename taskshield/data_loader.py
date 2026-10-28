"""Loads the task CSV into a pandas DataFrame.

Phase 2 keeps this simple: read, check columns, parse dates, split dependencies.
Deeper validation (duplicate IDs, circular dependencies...) comes in Phase 3.
"""
from pathlib import Path

import pandas as pd

from taskshield.config import REQUIRED_COLUMNS, TASKS_CSV

DATE_COLUMNS = ["start_date", "due_date", "last_updated"]


def load_tasks(path: Path = TASKS_CSV) -> pd.DataFrame:
    """Read the task file. Raises a clear error if the file or columns are wrong."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Task file not found: {path}")

    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Task file is missing required columns: {missing}")

    # Dates: unreadable values become NaT (blank) instead of crashing.
    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Numbers: unreadable values become NaN.
    df["estimated_hours"] = pd.to_numeric(df["estimated_hours"], errors="coerce")
    df["completed_percentage"] = pd.to_numeric(df["completed_percentage"], errors="coerce")

    # "T003;T004" -> ["T003", "T004"]; empty -> []
    df["dependency_list"] = df["dependency_ids"].apply(
        lambda s: [d.strip() for d in s.split(";") if d.strip()]
    )
    return df


def load_meeting_notes(path: Path) -> str:
    """Return meeting notes as plain text (treated as data, never as instructions)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Meeting notes not found: {path}")
    return path.read_text(encoding="utf-8")
