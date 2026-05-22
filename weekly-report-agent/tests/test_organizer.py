import pytest
from datetime import datetime

from weekly_report_agent.models import WorkItem
from weekly_report_agent.organizer import Organizer


@pytest.fixture
def organizer():
    return Organizer()


@pytest.fixture
def sample_items():
    return [
        WorkItem(source="git", project="proj", title="feat: new feature", category="新功能"),
        WorkItem(source="git", project="proj", title="fix: bug fix", category="Bug修复"),
        WorkItem(source="git", project="proj", title="docs: update readme", category="文档"),
        WorkItem(source="git", project="proj", title="chore: cleanup", category="杂项"),
        WorkItem(source="manual", project="other", title="meeting", category="其他"),
    ]


class TestOrganizer:
    def test_basic_organization(self, organizer, sample_items):
        report = organizer.organize(sample_items, title="测试周报", author="TT",
                                     start_date="2026-05-12", end_date="2026-05-18")
        assert report.title == "测试周报"
        assert report.author == "TT"
        assert "新功能" in report.sections
        assert "Bug修复" in report.sections
        assert len(report.sections["新功能"]) == 1

    def test_category_order(self, organizer, sample_items):
        report = organizer.organize(sample_items)
        keys = list(report.sections.keys())
        assert keys.index("新功能") < keys.index("Bug修复")
        assert keys.index("Bug修复") < keys.index("文档")

    def test_empty_items(self, organizer):
        report = organizer.organize([], start_date="2026-05-12", end_date="2026-05-18")
        assert report.sections == {}
        assert "0 项工作" in report.summary

    def test_summary_counts(self, organizer, sample_items):
        report = organizer.organize(sample_items)
        assert "5 项工作" in report.summary
        assert "2 个项目" in report.summary
