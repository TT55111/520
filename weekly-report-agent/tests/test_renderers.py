import json
import pytest

from weekly_report_agent.models import WorkItem, WeekReport
from weekly_report_agent.renderers import MarkdownRenderer, HTMLRenderer, PlainTextRenderer, JsonRenderer


@pytest.fixture
def report():
    items = [
        WorkItem(source="git", project="proj", title="feat: add", category="新功能"),
        WorkItem(source="git", project="proj", title="fix: bug", category="Bug修复"),
    ]
    sections = {}
    for item in items:
        sections.setdefault(item.category, []).append(item)
    return WeekReport(
        title="测试周报", author="TT",
        start_date="2026-05-12", end_date="2026-05-18",
        summary="本周完成 2 项工作", sections=sections,
        highlights=["亮点1"], next_week_plans=["计划1"],
    )


class TestMarkdownRenderer:
    def test_contains_sections(self, report):
        output = MarkdownRenderer().render(report)
        assert "# 测试周报" in output
        assert "## 新功能" in output
        assert "## Bug修复" in output
        assert "## 本周亮点" in output
        assert "## 下周计划" in output
        assert "亮点1" in output
        assert "计划1" in output

    def test_metadata(self, report):
        output = MarkdownRenderer().render(report)
        assert "TT" in output
        assert "2026-05-12" in output


class TestHTMLRenderer:
    def test_valid_html(self, report):
        output = HTMLRenderer().render(report)
        assert output.startswith("<!DOCTYPE html>")
        assert "</html>" in output
        assert "测试周报" in output

    def test_xss_prevention(self):
        item = WorkItem(source="manual", project="<script>alert(1)</script>", title="test", category="其他")
        report = WeekReport(
            title="<img onerror=alert(1)>", author="<script>",
            start_date="2026-05-12", end_date="2026-05-18",
            sections={"其他": [item]},
        )
        output = HTMLRenderer().render(report)
        assert "<script>" not in output
        assert "&lt;script&gt;" in output


class TestPlainTextRenderer:
    def test_basic_output(self, report):
        output = PlainTextRenderer().render(report)
        assert "测试周报" in output
        assert "TT" in output
        assert "【新功能】" in output


class TestJsonRenderer:
    def test_valid_json(self, report):
        output = JsonRenderer().render(report)
        data = json.loads(output)
        assert data["title"] == "测试周报"
        assert "新功能" in data["sections"]
