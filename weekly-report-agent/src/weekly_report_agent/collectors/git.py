"""Git 提交记录采集器"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

from .base import Collector
from weekly_report_agent.models import WorkItem


class GitCollector(Collector):
    """从本地 Git 仓库采集提交记录"""

    CATEGORY_MAP = {
        "feat": "新功能",
        "fix": "Bug修复",
        "chore": "杂项",
        "docs": "文档",
        "refactor": "重构",
        "test": "测试",
        "ci": "CI/CD",
        "style": "样式",
        "perf": "性能",
        "build": "构建",
    }

    def __init__(self, repo_path: str, project_name: str = "", author: str = ""):
        self.repo_path = Path(repo_path).resolve()
        self.project_name = project_name or self.repo_path.name
        self.author = author

    def _parse_category(self, message: str) -> str:
        match = re.match(r"^(\w+)(?:\(.*?\))?[:：]", message)
        if match:
            prefix = match.group(1).lower()
            return self.CATEGORY_MAP.get(prefix, prefix)
        return "其他"

    def collect(self, since: datetime, until: datetime) -> list[WorkItem]:
        since_str = since.strftime("%Y-%m-%d")
        until_str = until.strftime("%Y-%m-%d")

        cmd = [
            "git", "-C", str(self.repo_path), "log",
            f"--since={since_str}", f"--until={until_str}",
            "--pretty=format:%H|%s|%an|%ai",
            "--no-merges",
        ]
        if self.author:
            cmd.extend(["--author", self.author])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding="utf-8", errors="replace", check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"Git 采集失败 {self.repo_path}: {e}") from e

        items = []
        output = result.stdout or ""
        for line in output.strip().splitlines():
            if not line:
                continue
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            commit_hash, message, author, date = parts
            items.append(WorkItem(
                source="git",
                project=self.project_name,
                title=message.strip(),
                category=self._parse_category(message),
                url=str(self.repo_path),
                timestamp=date.strip(),
                author=author.strip(),
            ))
        return items
