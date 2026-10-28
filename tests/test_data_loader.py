"""Tests for taskshield.data_loader (run with: pytest)."""
import pandas as pd

from taskshield.config import get_as_of_date
from taskshield.data_loader import load_tasks


def test_loads_20_tasks_with_unique_ids():
    df = load_tasks()
    assert len(df) == 20
    assert df["task_id"].is_unique


def test_dates_are_parsed():
    df = load_tasks()
    assert df["due_date"].notna().all()


def test_dependencies_are_split_into_lists():
    df = load_tasks().set_index("task_id")
    assert df.loc["T003", "dependency_list"] == ["T002", "T004"]
    assert df.loc["T001", "dependency_list"] == []


def test_sample_contains_required_scenarios():
    df = load_tasks()
    as_of = pd.Timestamp(get_as_of_date())
    active = df[df["status"] != "Done"]
    # exactly one active task has no owner (T008)
    assert list(active[active["assigned_owner"] == ""]["task_id"]) == ["T008"]
    # exactly one active task is overdue (T016)
    assert list(active[active["due_date"] < as_of]["task_id"]) == ["T016"]


def test_missing_file_gives_clear_error():
    try:
        load_tasks("data/does_not_exist.csv")
    except FileNotFoundError as err:
        assert "not found" in str(err)
    else:
        raise AssertionError("expected FileNotFoundError")
