"""多平台内容自动整理与周报生成 Agent"""

__version__ = "1.0.0"

from .agent import WeeklyReportAgent
from .models import WorkItem, WeekReport

__all__ = ["WeeklyReportAgent", "WorkItem", "WeekReport"]
