"""周报生成 Agent 主类"""

from datetime import datetime, timedelta
from pathlib import Path

from .models import WorkItem, WeekReport
from .collectors import Collector, GitCollector, GitHubCollector, ManualCollector
from .organizer import Organizer
from .renderers import RENDERERS


class WeeklyReportAgent:
    """周报生成 Agent"""

    def __init__(self):
        self.collectors: list[Collector] = []
        self.organizer = Organizer()
        self.highlights: list[str] = []
        self.next_week_plans: list[str] = []

    def add_git_repo(self, repo_path: str, project_name: str = "", author: str = "") -> "WeeklyReportAgent":
        self.collectors.append(GitCollector(repo_path, project_name, author))
        return self

    def add_github(self, repo: str, item_types: list[str] | None = None, author: str = "") -> "WeeklyReportAgent":
        self.collectors.append(GitHubCollector(repo, item_types, author))
        return self

    def add_manual(self, entries: list[dict] | None = None, json_path: str = "") -> "WeeklyReportAgent":
        self.collectors.append(ManualCollector(entries, json_path))
        return self

    def set_highlights(self, highlights: list[str]) -> "WeeklyReportAgent":
        self.highlights = highlights
        return self

    def set_next_week_plans(self, plans: list[str]) -> "WeeklyReportAgent":
        self.next_week_plans = plans
        return self

    def generate(
        self,
        start_date: str,
        end_date: str,
        title: str = "",
        author: str = "",
        output_format: str = "markdown",
        output_path: str = "",
    ) -> str:
        since = datetime.strptime(start_date, "%Y-%m-%d")
        until = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)

        # 采集
        all_items: list[WorkItem] = []
        for collector in self.collectors:
            items = collector.collect(since, until)
            all_items.extend(items)

        # 整理
        report = self.organizer.organize(all_items, title, author, start_date, end_date)
        report.highlights = self.highlights
        report.next_week_plans = self.next_week_plans

        # 渲染
        renderer_cls = RENDERERS.get(output_format)
        if not renderer_cls:
            raise ValueError(f"不支持的输出格式: {output_format}，可选: {', '.join(RENDERERS.keys())}")
        output = renderer_cls().render(report)

        # 写入文件
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(output, encoding="utf-8")

        return output
