"""内容整理器"""

from weekly_report_agent.models import WorkItem, WeekReport


class Organizer:
    """将原始 WorkItem 整理成结构化周报"""

    CATEGORY_ORDER = [
        "新功能", "Bug修复", "重构", "文档",
        "测试", "CI/CD", "性能", "构建", "样式", "杂项", "其他",
    ]

    def organize(
        self,
        items: list[WorkItem],
        title: str = "",
        author: str = "",
        start_date: str = "",
        end_date: str = "",
    ) -> WeekReport:
        # 按分类聚合
        sections: dict[str, list[WorkItem]] = {}
        for item in items:
            key = item.category or "其他"
            sections.setdefault(key, []).append(item)

        # 按预定义顺序排序
        sorted_sections = {}
        for cat in self.CATEGORY_ORDER:
            if cat in sections:
                sorted_sections[cat] = sections[cat]
        for cat in sections:
            if cat not in sorted_sections:
                sorted_sections[cat] = sections[cat]

        # 自动生成摘要
        total = len(items)
        projects = len({i.project for i in items})
        categories = len(sorted_sections)
        summary = f"本周共处理 {total} 项工作，涉及 {projects} 个项目，覆盖 {categories} 个类别。"

        return WeekReport(
            title=title or f"周报 ({start_date} ~ {end_date})",
            author=author,
            start_date=start_date,
            end_date=end_date,
            summary=summary,
            sections=sorted_sections,
        )
