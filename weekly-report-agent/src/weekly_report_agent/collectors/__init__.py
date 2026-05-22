from .base import Collector
from .git import GitCollector
from .github import GitHubCollector
from .manual import ManualCollector

__all__ = ["Collector", "GitCollector", "GitHubCollector", "ManualCollector"]
