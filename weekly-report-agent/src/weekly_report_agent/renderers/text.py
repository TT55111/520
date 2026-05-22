"""纯文本渲染器"""

from .base import Renderer
from weekly_report_agent.models import WeekReport


class PlainTextRenderer(Renderer):

    def render(self, report: WeekReport) -> str:
        lines = [
            report.title,
            "=" * len(report.title.encode("gbk", errors="replace")),
        ]

        if report.author:
            lines.append(f"作者: {report.author}")
        if report.start_date and report.end_date:
            lines.append(f"周期: {report.start_date} ~ {report.end_date}")
        lines.append("")

        if report.summary:
            lines.append(f"摘要: {report.summary}")
            lines.append("")

        for category, items in report.sections.items():
            lines.append(f"【{category}】({len(items)}项)")
            lines.append("-" * 48)
            for item in items:
                prefix = f"[{item.project}] " if item.project else ""
                lines.append(f"  * {prefix}{item.title}")
                if item.description:
                    lines.append(f"    {item.description}")
            lines.append("")

        if report.highlights:
            lines.append("本周亮点")
            lines.append("-" * 48)
            for h in report.highlights:
                lines.append(f"  * {h}")
            lines.append("")

        if report.next_week_plans:
            lines.append("下周计划")
            lines.append("-" * 48)
            for p in report.next_week_plans:
                lines.append(f"  * {p}")
            lines.append("")

        return "\n".join(lines)
