"""GitHub API 采集器 (通过 gh CLI)"""

import json
import subprocess
from datetime import datetime

from .base import Collector
from weekly_report_agent.models import WorkItem


class GitHubCollector(Collector):
    """通过 GitHub CLI (gh) 采集 PR 和 Issue"""

    def __init__(self, repo: str, item_types: list[str] | None = None, author: str = ""):
        self.repo = repo  # owner/repo
        self.item_types = item_types or ["pr", "issue"]
        self.author = author

    def _run_gh(self, args: list[str]) -> list[dict]:
        cmd = ["gh"] + args + ["--json", "title,createdAt,url,author,state,labels"]
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding="utf-8", errors="replace", check=True,
            )
            return json.loads(result.stdout) if result.stdout.strip() else []
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"gh 命令执行失败: {e}") from e

    def collect(self, since: datetime, until: datetime) -> list[WorkItem]:
        items = []

        if "pr" in self.item_types:
            prs = self._run_gh(["pr", "list", "-R", self.repo, "--state", "all", "-L", "100"])
            for pr in prs:
                created = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
                if since <= created.replace(tzinfo=None) <= until:
                    author_login = pr.get("author", {}).get("login", "")
                    if self.author and author_login != self.author:
                        continue
                    items.append(WorkItem(
                        source="github",
                        project=self.repo,
                        title=f"[PR] {pr['title']}",
                        category="新功能",
                        url=pr["url"],
                        timestamp=pr["createdAt"],
                        author=author_login,
                        tags=[pr.get("state", "")],
                    ))

        if "issue" in self.item_types:
            issues = self._run_gh(["issue", "list", "-R", self.repo, "--state", "all", "-L", "100"])
            for issue in issues:
                created = datetime.fromisoformat(issue["createdAt"].replace("Z", "+00:00"))
                if since <= created.replace(tzinfo=None) <= until:
                    author_login = issue.get("author", {}).get("login", "")
                    if self.author and author_login != self.author:
                        continue
                    items.append(WorkItem(
                        source="github",
                        project=self.repo,
                        title=f"[Issue] {issue['title']}",
                        category="Bug修复",
                        url=issue["url"],
                        timestamp=issue["createdAt"],
                        author=author_login,
                        tags=[issue.get("state", "")],
                    ))
        return items
