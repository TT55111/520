import pytest
from datetime import datetime, timedelta

from weekly_report_agent.collectors.git import GitCollector
from weekly_report_agent.collectors.manual import ManualCollector


class TestGitCollector:
    def test_parse_category(self):
        c = GitCollector(".")
        assert c._parse_category("feat: add feature") == "新功能"
        assert c._parse_category("fix(auth): login bug") == "Bug修复"
        assert c._parse_category("random commit message") == "其他"

    def test_parse_category_all_types(self):
        c = GitCollector(".")
        assert c._parse_category("refactor: clean up") == "重构"
        assert c._parse_category("docs: update") == "文档"
        assert c._parse_category("test: add tests") == "测试"
        assert c._parse_category("ci: update workflow") == "CI/CD"
        assert c._parse_category("style: format") == "样式"
        assert c._parse_category("perf: optimize") == "性能"


class TestManualCollector:
    def test_collect_from_entries(self):
        entries = [
            {"project": "测试", "title": "任务1", "category": "新功能"},
            {"project": "测试", "title": "任务2", "category": "Bug修复"},
        ]
        collector = ManualCollector(entries=entries)
        since = datetime(2026, 1, 1)
        until = datetime(2026, 12, 31)
        items = collector.collect(since, until)
        assert len(items) == 2
        assert items[0].source == "manual"
        assert items[0].category == "新功能"

    def test_empty_collector(self):
        collector = ManualCollector()
        items = collector.collect(datetime(2026, 1, 1), datetime(2026, 12, 31))
        assert items == []
