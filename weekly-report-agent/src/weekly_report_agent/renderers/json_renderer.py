"""JSON 渲染器"""

import json

from .base import Renderer
from weekly_report_agent.models import WeekReport


class JsonRenderer(Renderer):

    def render(self, report: WeekReport) -> str:
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
