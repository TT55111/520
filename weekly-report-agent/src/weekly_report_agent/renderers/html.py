"""HTML 渲染器"""

from datetime import datetime
from html import escape

from .base import Renderer
from weekly_report_agent.models import WeekReport


class HTMLRenderer(Renderer):

    _STYLE = """body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",sans-serif;max-width:960px;margin:40px auto;padding:0 24px;color:#1f2328;line-height:1.6}
h1{border-bottom:2px solid #0969da;padding-bottom:10px}
h2{color:#0969da;margin-top:28px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}
th,td{border:1px solid #d0d7de;padding:8px 12px;text-align:left}
th{background:#f6f8fa;font-weight:600}
tr:nth-child(even){background:#f6f8fa}
.meta{color:#656d76;font-size:14px}
a{color:#0969da;text-decoration:none}
a:hover{text-decoration:underline}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:12px;background:#ddf4ff;color:#0969da}
.highlight{background:#fff8c5;padding:12px 16px;border-radius:6px;margin:8px 0}"""

    def render(self, report: WeekReport) -> str:
        sections_html = ""
        for category, items in report.sections.items():
            rows = ""
            for item in items:
                project = escape(item.project) or "-"
                title = escape(item.title)
                cat = escape(item.category) or "-"
                url_td = f'<a href="{escape(item.url)}" target="_blank">链接</a>' if item.url else "-"
                desc = f"<br><small style='color:#656d76'>{escape(item.description)}</small>" if item.description else ""
                rows += f"<tr><td>{project}</td><td>{title}{desc}</td><td><span class='badge'>{cat}</span></td><td>{url_td}</td></tr>\n"
            sections_html += f"""
            <h2>{escape(category)} ({len(items)})</h2>
            <table>
                <thead><tr><th>项目</th><th>内容</th><th>分类</th><th>链接</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>"""

        highlights_html = ""
        if report.highlights:
            items_html = "".join(f"<li>{escape(h)}</li>" for h in report.highlights)
            highlights_html = f"<h2>本周亮点</h2><div class='highlight'><ul>{items_html}</ul></div>"

        plans_html = ""
        if report.next_week_plans:
            items_html = "".join(f"<li>{escape(p)}</li>" for p in report.next_week_plans)
            plans_html = f"<h2>下周计划</h2><ul>{items_html}</ul>"

        author_line = f"<p class='meta'>作者: {escape(report.author)}</p>" if report.author else ""

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(report.title)}</title>
<style>{self._STYLE}</style>
</head>
<body>
<h1>{escape(report.title)}</h1>
{author_line}
<p class='meta'>周期: {escape(report.start_date)} ~ {escape(report.end_date)}</p>
<h2>摘要</h2><p>{escape(report.summary)}</p>
{sections_html}
{highlights_html}
{plans_html}
<hr>
<p class='meta'><em>由 weekly-report-agent v1.0.0 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}</em></p>
</body>
</html>"""
