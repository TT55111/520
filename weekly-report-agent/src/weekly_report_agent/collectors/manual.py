"""自定义条目采集器"""

import json
from datetime import datetime
from pathlib import Path

from .base import Collector
from weekly_report_agent.models import WorkItem


class ManualCollector(Collector):
    """从 JSON 文件或直接传入的条目列表采集"""

    def __init__(self, entries: list[dict] | None = None, json_path: str = ""):
        self.entries = entries or []
        self.json_path = json_path

    def collect(self, since: datetime, until: datetime) -> list[WorkItem]:
        items = list(self.entries)
        if self.json_path and Path(self.json_path).exists():
            with open(self.json_path, "r", encoding="utf-8") as f:
                items.extend(json.load(f))

        result = []
        for entry in items:
            result.append(WorkItem(
                source="manual",
                project=entry.get("project", "其他"),
                title=entry.get("title", ""),
                description=entry.get("description", ""),
                category=entry.get("category", "其他"),
                url=entry.get("url", ""),
                timestamp=entry.get("timestamp", ""),
                author=entry.get("author", ""),
                tags=entry.get("tags", []),
            ))
        return result
