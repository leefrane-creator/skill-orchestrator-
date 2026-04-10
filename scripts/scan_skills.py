#!/usr/bin/env python3
"""
Skill Scanner - Scans local skill directories and generates a structured registry.

Scans all SKILL.md files under the specified skill directories, extracts
name and description from YAML frontmatter, auto-categorizes skills by
keywords, and outputs a Markdown registry file.

Usage:
    python scan_skills.py [--paths <dir1> <dir2> ...] [--output <file>]

Examples:
    python scan_skills.py
    python scan_skills.py --paths C:\\Users\\lee\\.workbuddy\\skills --output registry.md
    python scan_skills.py --paths /home/user/skills /project/.workbuddy/skills
"""

import argparse
import re
import sys
from pathlib import Path


# Default skill directories to scan
DEFAULT_PATHS = [
    str(Path.home() / ".workbuddy" / "skills"),
]

# Category definitions: category_name -> list of keywords for matching
CATEGORIES = {
    "信息获取": [
        "搜索", "search", "fetch", "scrape", "crawl", "抓取", "查找",
        "web search", "read", "monitor", "监控", "订阅", "RSS",
        "twitter", "reddit", "youtube", "bilibili", "weibo", "微博",
        "微信", "wechat", "公众号", "新闻", "news", "趋势", "trending",
        "reach", "agent-reach", "搜索引擎",
    ],
    "内容创作": [
        "写", "写作", "writer", "writing", "创作", "文章", "article",
        "润色", "humaniz", "去味", "book", "书", "slides", "演示",
        "markdown", "内容", "content", "文案", "copy", "edit", "编辑",
    ],
    "视觉设计": [
        "设计", "design", "视觉", "canvas", "image", "图片", "图",
        "card", "卡片", "poster", "海报", "封面", "cover", "art",
        "图标", "icon", "lucide", "template", "模板",
    ],
    "社交发布": [
        "发布", "publish", "推送", "小红书", "xiaohongshu", "rednote",
        "头条", "toutiao", "公众号发布", "xhs", "社交", "social",
        "tweet", "twitter发布", "post",
    ],
    "数据分析": [
        "数据", "data", "分析", "analysis", "统计", "statistic",
        "可视化", "visualization", "chart", "图表", "excel", "xlsx",
        "金融", "finance", "stock", "股票", "基金", "fund",
        "financial", "trading", "量化", "quant",
    ],
    "视频音频": [
        "视频", "video", "音频", "audio", "music", "BGM", "音乐",
        "whisper", "语音", "speech", "字幕", "subtitle", "字幕",
        "remotion", "帧", "frame", "生成视频", "seedance",
        "libtv", "liblib", "图片生成", "图生视频",
    ],
    "工具基础设施": [
        "MCP", "mcp", "工具", "tool", "自动化", "automation",
        "workflow", "工作流", "skill", "技能", "配置", "config",
        "安全", "security", "审计", "audit", "vetter", "guard",
        "浏览器", "browser", "github", "git", "部署", "deploy",
        "trello", "看板", "obsidian", "笔记", "笔记管理",
        "天气", "weather", "日历", "calendar",
        "self-improving", "自我改进", "channel", "渠道",
        "summarize", "总结", "摘要",
    ],
}


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter fields from SKILL.md content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm_text = match.group(1)
    result = {}

    # Simple YAML parsing for name and description fields
    # Handle multi-line description (| or > style)
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # Match "key: value" or "key:" (for multi-line)
        key_match = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if key_match:
            key = key_match.group(1).strip()
            value = key_match.group(2).strip()

            # Handle multi-line strings (| or > style)
            if value in ("|", ">", "|+", ">+", "|-", ">-"):
                multiline = []
                i += 1
                while i < len(lines):
                    if lines[i] and not lines[i][0].isspace():
                        break
                    multiline.append(lines[i].strip())
                    i += 1
                result[key] = "\n".join(multiline).strip()
                continue
            # Handle quoted strings
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                result[key] = value[1:-1]
            else:
                result[key] = value
        i += 1

    return result


def categorize_skill(name: str, description: str) -> str:
    """Auto-categorize a skill based on its name and description keywords."""
    text = f"{name} {description}".lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[category] = score

    if not scores:
        return "其他"

    return max(scores, key=scores.get)


def scan_directory(skills_dir: str) -> list[dict]:
    """Scan a directory for SKILL.md files and extract metadata."""
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        print(f"  Directory does not exist, skipping: {skills_dir}")
        return []

    results = []

    # Find all SKILL.md files (including in subdirectories for nested skills)
    for skill_md in skills_path.rglob("SKILL.md"):
        try:
            content = skill_md.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)

            name = fm.get("name", skill_md.parent.name)
            description = fm.get("description", "")

            if not description:
                # Try description_en as fallback
                description = fm.get("description_en", "No description available")

            category = categorize_skill(name, description)

            results.append({
                "name": name,
                "description": description,
                "category": category,
                "path": str(skill_md.parent),
                "relative_path": str(skill_md.parent.relative_to(skills_path)),
            })
        except Exception as e:
            print(f"  Warning: Failed to parse {skill_md}: {e}")

    return results


def generate_registry(skills: list[dict], output_path: str):
    """Generate a Markdown skill registry file grouped by category."""
    # Group by category
    by_category = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(skill)

    # Category order
    cat_order = [
        "信息获取", "内容创作", "视觉设计", "社交发布",
        "数据分析", "视频音频", "工具基础设施", "其他",
    ]

    lines = [
        "# Skill Registry",
        "",
        "> Auto-generated by scan_skills.py. ",
        "> Last updated: run `python scripts/scan_skills.py` to refresh.",
        "",
        "## How to Use This Registry",
        "",
        "This registry categorizes all locally installed skills. When orchestrating",
        "a multi-skill workflow, use this registry to:",
        "1. Identify which skills can handle each sub-task",
        "2. Find skills that produce output compatible with another skill's input",
        "3. Discover skill combinations that create powerful workflows",
        "",
        "---",
        "",
    ]

    for cat in cat_order:
        if cat not in by_category:
            continue

        cat_skills = sorted(by_category[cat], key=lambda s: s["name"])
        lines.append(f"## {cat}")
        lines.append("")

        for skill in cat_skills:
            lines.append(f"### {skill['name']}")
            lines.append("")
            # Truncate long descriptions for readability
            desc = skill["description"]
            if len(desc) > 300:
                desc = desc[:297] + "..."
            lines.append(f"**Description**: {desc}")
            lines.append("")
            lines.append(f"**Path**: `{skill['relative_path']}`")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Add collaboration hints section
    lines.append("## Skill Collaboration Hints")
    lines.append("")
    lines.append("Common skill pairing patterns for workflow orchestration:")
    lines.append("")
    lines.append("| Upstream Skill | Downstream Skill | Data Passed | Use Case |")
    lines.append("|---|---|---|---|")
    lines.append("| agent-reach | xhs-link-to-card-pipeline | URL + extracted content | Search results to XHS cards |")
    lines.append("| agent-reach | summarize | URL content | Search results to summary |")
    lines.append("| wechat-mp-writer | wechat-publisher | Markdown article | Write then publish to WeChat |")
    lines.append("| wechat-mp-writer | canvas-design | Article topic + style | Write article then design cover |")
    lines.append("| toutiao-news-trends | wechat-mp-writer | Hot topic keywords | Trend to article |")
    lines.append("| toutiao-news-trends | toutiao-publish | Article content | Trend to Toutiao post |")
    lines.append("| neodata-financial-search | xlsx | Financial data | Query data then make spreadsheet |")
    lines.append("| xhs-link-to-card-pipeline | xiaohongshu | PNG cards + copy | Cards ready to publish on XHS |")
    lines.append("| agent-reach | video-generator-seedance | Content + script | Research to video |")
    lines.append("| summarize | obsidian | Summarized content | Summary to knowledge base |")
    lines.append("| canvas-design | image_gen | Design spec | Design spec to AI-generated image |")
    lines.append("| libtv | xiaohongshu | Generated image/video | AI art to XHS post |")
    lines.append("| humanizer | wechat-mp-writer | Draft text | De-AI article before publishing |")
    lines.append("| humanizer | toutiao-publish | Draft text | De-AI content before Toutiao |")
    lines.append("")

    # Write output
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Registry written to: {output}")
    print(f"Total skills: {len(skills)}, Categories: {len(by_category)}")


def main():
    parser = argparse.ArgumentParser(
        description="Scan local skill directories and generate a skill registry"
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        default=DEFAULT_PATHS,
        help="Directories to scan for skills (default: ~/.workbuddy/skills)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path for the registry (default: references/skill_registry.md next to this script)"
    )

    args = parser.parse_args()

    if args.output is None:
        script_dir = Path(__file__).parent.parent
        args.output = str(script_dir / "references" / "skill_registry.md")

    print("Scanning skill directories...")
    all_skills = []

    for path in args.paths:
        print(f"  Scanning: {path}")
        found = scan_directory(path)
        all_skills.extend(found)
        print(f"    Found {len(found)} skills")

    # Deduplicate by name
    seen_names = set()
    unique_skills = []
    for skill in all_skills:
        if skill["name"] not in seen_names:
            seen_names.add(skill["name"])
            unique_skills.append(skill)

    print(f"\nTotal unique skills: {len(unique_skills)}")
    generate_registry(unique_skills, args.output)


if __name__ == "__main__":
    main()
