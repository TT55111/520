# weekly-report-agent

多平台内容自动整理与周报生成 Agent。

从 Git 仓库、GitHub PR/Issue、自定义条目等多数据源采集工作记录，按 conventional commits 规范自动分类，输出 Markdown / HTML / 纯文本 / JSON 格式的结构化周报。

## 安装

```bash
# 从源码安装
pip install -e .

# 或直接打包
pip install .
```

## 快速开始

```bash
# 当前仓库本周周报
weekly-report --git . --author TT

# 指定日期范围，输出 HTML 文件
weekly-report --git . -s 2026-05-12 -e 2026-05-18 -f html -o report.html

# 多仓库
weekly-report --git ./project-a --git ./project-b -a TT

# GitHub PR/Issue（需要 gh CLI 已登录）
weekly-report --github owner/repo -a TT

# 使用配置文件
weekly-report --config config.json

# 生成示例配置
weekly-report --generate-config
```

## 输出格式

| 格式 | 说明 |
|------|------|
| `markdown` | Markdown 文档（默认） |
| `html` | 带样式的 HTML 页面 |
| `text` | 纯文本 |
| `json` | 结构化 JSON |

## 配置文件

```json
{
  "git_repos": [
    {"path": "./my-project", "name": "我的项目", "author": "TT"}
  ],
  "github_repos": [
    {"repo": "owner/repo", "types": ["pr", "issue"]}
  ],
  "manual_entries": {
    "entries": [
      {"project": "产品", "title": "完成需求评审", "category": "其他"}
    ]
  },
  "report": {
    "title": "工作周报",
    "author": "TT",
    "start_date": "2026-05-12",
    "end_date": "2026-05-18",
    "format": "markdown",
    "output": "weekly-report.md",
    "highlights": ["完成核心功能"],
    "next_week_plans": ["继续开发"]
  }
}
```

## 自动分类

提交信息按 conventional commits 前缀自动归类：

| 前缀 | 分类 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug修复 |
| `refactor` | 重构 |
| `docs` | 文档 |
| `test` | 测试 |
| `ci` | CI/CD |
| `perf` | 性能 |
| `chore` | 杂项 |

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 类型检查
mypy src/
```

## License

MIT
