"""渲染器基类"""

from abc import ABC, abstractmethod

from weekly_report_agent.models import WeekReport


class Renderer(ABC):
    """输出渲染器基类"""

    @abstractmethod
    def render(self, report: WeekReport) -> str:
        ...
