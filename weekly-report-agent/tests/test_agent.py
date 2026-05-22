import pytest
import tempfile
import os

from weekly_report_agent.agent import WeeklyReportAgent
from weekly_report_agent.collectors.manual import ManualCollector


@pytest.fixture
def agent_with_manual():
    agent = WeeklyReportAgent()
    agent.add_manual(entries=[
        {"project": "测试项目", "title": "feat: 新功能A", "category": "新功能"},
        {"project": "测试项目", "title": "fix: 修复B", "category": "Bug修复"},
        {"project": "另一项目", "title": "docs: 文档更新", "category": "文档"},
    ])
    return agent


class TestAgent:
    def test_generate_markdown(self, agent_with_manual):
        result = agent_with_manual.generate(
            start_date="2026-01-01", end_date="2026-12-31",
            title="测试周报", author="TT", output_format="markdown",
        )
        assert "# 测试周报" in result
        assert "TT" in result
        assert "新功能" in result

    def test_generate_html(self, agent_with_manual):
        result = agent_with_manual.generate(
            start_date="2026-01-01", end_date="2026-12-31",
            output_format="html",
        )
        assert "<!DOCTYPE html>" in result

    def test_generate_json(self, agent_with_manual):
        result = agent_with_manual.generate(
            start_date="2026-01-01", end_date="2026-12-31",
            output_format="json",
        )
        import json
        data = json.loads(result)
        assert "sections" in data

    def test_output_to_file(self, agent_with_manual):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as f:
            path = f.name
        try:
            agent_with_manual.generate(
                start_date="2026-01-01", end_date="2026-12-31",
                title="Weekly Report", output_format="markdown", output_path=path,
            )
            assert os.path.exists(path)
            content = open(path, encoding="utf-8").read()
            assert "Weekly Report" in content
        finally:
            os.unlink(path)

    def test_highlights_and_plans(self, agent_with_manual):
        agent_with_manual.set_highlights(["亮点A", "亮点B"])
        agent_with_manual.set_next_week_plans(["计划X"])
        result = agent_with_manual.generate(
            start_date="2026-01-01", end_date="2026-12-31",
            output_format="markdown",
        )
        assert "亮点A" in result
        assert "计划X" in result

    def test_chaining(self):
        agent = WeeklyReportAgent()
        result = agent.add_git_repo(".").add_manual(entries=[{"title": "t", "project": "p"}])
        assert result is agent
