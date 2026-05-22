"""配置文件加载"""

import json
from pathlib import Path

from .agent import WeeklyReportAgent


def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_agent_from_config(config: dict) -> WeeklyReportAgent:
    agent = WeeklyReportAgent()

    for repo in config.get("git_repos", []):
        agent.add_git_repo(
            repo_path=repo["path"],
            project_name=repo.get("name", ""),
            author=repo.get("author", ""),
        )

    for gh in config.get("github_repos", []):
        agent.add_github(
            repo=gh["repo"],
            item_types=gh.get("types", ["pr", "issue"]),
            author=gh.get("author", ""),
        )

    manual = config.get("manual_entries", {})
    if manual:
        agent.add_manual(
            entries=manual.get("entries", []),
            json_path=manual.get("json_path", ""),
        )

    report_cfg = config.get("report", {})
    if report_cfg.get("highlights"):
        agent.set_highlights(report_cfg["highlights"])
    if report_cfg.get("next_week_plans"):
        agent.set_next_week_plans(report_cfg["next_week_plans"])

    return agent


EXAMPLE_CONFIG = {
    "git_repos": [
        {"path": "./my-project", "name": "我的项目", "author": ""},
        {"path": "../another-project", "name": "另一个项目"},
    ],
    "github_repos": [
        {"repo": "owner/repo", "types": ["pr", "issue"], "author": ""},
    ],
    "manual_entries": {
        "json_path": "entries.json",
        "entries": [
            {
                "project": "产品",
                "title": "完成需求评审",
                "category": "其他",
                "description": "评审了3个需求",
            }
        ],
    },
    "report": {
        "title": "工作周报",
        "author": "张三",
        "start_date": "2026-05-12",
        "end_date": "2026-05-18",
        "format": "markdown",
        "output": "weekly-report.md",
        "highlights": ["完成核心功能开发", "修复 3 个线上 Bug"],
        "next_week_plans": ["继续开发剩余功能", "准备技术分享"],
    },
}
