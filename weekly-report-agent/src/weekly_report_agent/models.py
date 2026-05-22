"""数据模型定义"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class WorkItem:
    """单条工作记录"""
    source: str           # 来源: git/github/gitlab/manual
    project: str          # 项目名
    title: str            # 标题/提交信息
    description: str = "" # 详细描述
    category: str = ""    # 分类: feat/fix/chore/docs/other
    url: str = ""         # 链接
    timestamp: str = ""   # 时间
    author: str = ""      # 作者
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class WeekReport:
    """周报"""
    title: str
    author: str
    start_date: str
    end_date: str
    summary: str = ""
    sections: dict = field(default_factory=dict)  # category -> [WorkItem]
    highlights: list = field(default_factory=list)
    next_week_plans: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "summary": self.summary,
            "sections": {k: [i.to_dict() for i in v] for k, v in self.sections.items()},
            "highlights": self.highlights,
            "next_week_plans": self.next_week_plans,
        }
