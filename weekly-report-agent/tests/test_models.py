import pytest
from weekly_report_agent.models import WorkItem, WeekReport


class TestWorkItem:
    def test_create_with_defaults(self):
        item = WorkItem(source="git", project="test", title="feat: add feature")
        assert item.source == "git"
        assert item.category == ""
        assert item.tags == []

    def test_to_dict(self):
        item = WorkItem(source="manual", project="proj", title="task", category="其他")
        d = item.to_dict()
        assert d["source"] == "manual"
        assert d["project"] == "proj"
        assert isinstance(d["tags"], list)


class TestWeekReport:
    def test_to_dict(self):
        report = WeekReport(
            title="周报", author="TT",
            start_date="2026-05-12", end_date="2026-05-18",
            summary="测试", sections={"新功能": [WorkItem(source="git", project="p", title="t")]},
        )
        d = report.to_dict()
        assert d["title"] == "周报"
        assert len(d["sections"]["新功能"]) == 1
