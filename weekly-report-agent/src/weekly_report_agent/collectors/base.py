"""数据采集器基类"""

from abc import ABC, abstractmethod
from datetime import datetime

from weekly_report_agent.models import WorkItem


class Collector(ABC):
    """数据采集器基类"""

    @abstractmethod
    def collect(self, since: datetime, until: datetime) -> list[WorkItem]:
        """采集指定时间范围内的工作记录"""
        ...
