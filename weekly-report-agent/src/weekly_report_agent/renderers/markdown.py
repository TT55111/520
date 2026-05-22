"""Markdown 渲染器"""

from datetime import datetime

from .base import Renderer
from weekly_report_agent.models import WeekReport


class MarkdownRenderer(Renderer):

    def render(self, report: WeekReport) -> str:
        lines = [
            f"# {report.title}",
            "",
        ]

        meta = []
        if report.author:
            meta.append(f"**作者**: {report.author}")
        if report.start_date and report.end_date:
            meta.append(f"**周期**: {report.start_date} ~ {report.end_date}")
        if meta:
            lines.extend(meta)
            lines.append("")

        if report.summary:
            lines.extend(["## 摘要", "", report.summary, ""])

        for category, items in report.sections.items():
            lines.append(f"## {category} ({len(items)})")
            lines.append("")
            for item in items:
                prefix = f"`{item.project}`" if item.project else ""
                url_part = f" [→]({item.url})" if item.url else ""
                desc_part = f"\n  > {item.description}" if item.description else ""
                lines.append(f"- {prefix} {item.title}{url_part}{desc_part}")
            lines.append("")

        if report.highlights:
            lines.extend(["## 本周亮点", ""])
            for h in report.highlights:
                lines.append(f"- {h}")
            lines.append("")

        if report.next_week_plans:
            lines.extend(["## 下周计划", ""])
            for p in report.next_week_plans:
                lines.append(f"- {p}")
            lines.append("")

        lines.extend([
            "---",
            f"_由 weekly-report-agent v1.0.0 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        ])
        return "\n".join(lines)
