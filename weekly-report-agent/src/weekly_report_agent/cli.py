"""CLI 入口"""

import argparse
import json
import sys
from datetime import datetime, timedelta

from . import __version__
from .agent import WeeklyReportAgent
from .config import load_config, build_agent_from_config, EXAMPLE_CONFIG
from .renderers import RENDERERS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weekly-report",
        description="多平台内容自动整理与周报生成 Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 当前仓库本周周报
  weekly-report --git . --author TT

  # 指定日期范围，输出 HTML
  weekly-report --git . -s 2026-05-12 -e 2026-05-18 -f html -o report.html

  # 多仓库 + GitHub
  weekly-report --git ./proj-a --git ./proj-b --github owner/repo -a TT

  # 使用配置文件
  weekly-report --config config.json

  # 生成示例配置
  weekly-report --generate-config
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # 数据源
    src = parser.add_argument_group("数据源")
    src.add_argument("--config", "-c", help="JSON 配置文件路径")
    src.add_argument("--git", action="append", default=[], metavar="PATH", help="Git 仓库路径 (可多次指定)")
    src.add_argument("--github", action="append", default=[], metavar="OWNER/REPO", help="GitHub 仓库 (可多次指定)")
    src.add_argument("--manual", metavar="FILE", help="自定义条目 JSON 文件")

    # 时间范围
    time_group = parser.add_argument_group("时间范围")
    time_group.add_argument("--start", "-s", metavar="YYYY-MM-DD", help="开始日期 (默认本周一)")
    time_group.add_argument("--end", "-e", metavar="YYYY-MM-DD", help="结束日期 (默认今天)")

    # 输出
    out = parser.add_argument_group("输出")
    out.add_argument("--title", "-t", help="周报标题")
    out.add_argument("--author", "-a", help="作者名")
    out.add_argument("--format", "-f", choices=list(RENDERERS.keys()), default="markdown", help="输出格式 (默认 markdown)")
    out.add_argument("--output", "-o", metavar="FILE", help="输出文件路径 (不指定则打印到终端)")

    # 其他
    parser.add_argument("--generate-config", action="store_true", help="生成示例配置文件")

    return parser


def main(argv: list[str] | None = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    # 生成示例配置
    if args.generate_config:
        with open("config.example.json", "w", encoding="utf-8") as f:
            json.dump(EXAMPLE_CONFIG, f, ensure_ascii=False, indent=2)
        print("已生成 config.example.json")
        return

    # 从配置文件构建
    if args.config:
        config = load_config(args.config)
        agent = build_agent_from_config(config)
        report_cfg = config.get("report", {})
        start_date = args.start or report_cfg.get("start_date", "")
        end_date = args.end or report_cfg.get("end_date", "")
        title = args.title or report_cfg.get("title", "")
        author = args.author or report_cfg.get("author", "")
        output_format = args.format or report_cfg.get("format", "markdown")
        output_path = args.output or report_cfg.get("output", "")
    else:
        if not args.git and not args.github and not args.manual:
            parser.error("请至少指定一个数据源 (--git / --github / --manual)，或使用 --config")

        agent = WeeklyReportAgent()
        for repo in args.git:
            agent.add_git_repo(repo)
        for gh in args.github:
            agent.add_github(gh)
        if args.manual:
            agent.add_manual(json_path=args.manual)

        start_date = args.start
        end_date = args.end
        title = args.title
        author = args.author
        output_format = args.format
        output_path = args.output

    # 默认本周
    today = datetime.now()
    if not start_date:
        monday = today - timedelta(days=today.weekday())
        start_date = monday.strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    # 生成
    result = agent.generate(
        start_date=start_date,
        end_date=end_date,
        title=title,
        author=author,
        output_format=output_format,
        output_path=output_path,
    )

    if output_path:
        print(f"周报已保存至: {output_path}")
    else:
        print(result)
