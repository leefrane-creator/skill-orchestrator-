# Skill Orchestrator

A meta-skill that discovers, selects, and chains multiple skills to complete complex tasks that no single skill can handle alone.

## Overview

Skill Orchestrator solves a key pain point: you have 50+ skills installed, but they can't work together effectively. This skill acts as a conductor - it analyzes your task, picks the right combination of skills, defines execution order, and manages data flow between them.

## Features

- **Automatic Skill Discovery** - Scans installed skills and builds a categorized registry
- **Smart Pipeline Selection** - Matches your task to pre-built workflow templates
- **Dynamic Orchestration** - Constructs custom pipelines when no template matches
- **Data Handoff Management** - Handles transformation between skill outputs/inputs
- **8 Pre-built Templates** - Covering WeChat, XiaoHongShu, Toutiao, financial analysis, and more

## File Structure

```
skill-orchestrator/
├── SKILL.md                          # Core orchestration logic
├── scripts/
│   └── scan_skills.py                # Local skill scanner
└── references/
    ├── skill_registry.md            # All installed skills (auto-generated)
    └── pipeline_templates.md         # 8 workflow templates
```

## Quick Start

### Trigger Keywords

Activate this skill when you say:
- "全流程", "一站式", "编排", "流水线"
- "skill组合", "帮我用skill", "多个skill协作"
- "帮我用xxx和xxx"
- Cross-platform tasks like "research and publish", "search and create cards"

### How It Works

1. **Analyze** - Decomposes your task into sub-tasks
2. **Match** - Finds the right skills from the registry
3. **Orchestrate** - Selects or builds a pipeline
4. **Execute** - Runs each step with proper data passing
5. **Deliver** - Summarizes results and output locations

### Example Pipelines

**WeChat Article → Publish:**
```
agent-reach → wechat-mp-writer → humanizer → canvas-design → wechat-publisher
```

**XiaoHongShu Note:**
```
agent-reach → xhs-link-to-card-pipeline → xiaohongshu
```

**Financial Analysis:**
```
neodata-financial-search → xlsx → canvas-design
```

## Refreshing the Skill Registry

When you install new skills, run:

```bash
python scripts/scan_skills.py --paths ~/.workbuddy/skills --output references/skill_registry.md
```

## For WorkBuddy Users

This skill is designed for the [WorkBuddy](https://github.com/codebuddy-pvt-ltd/workbuddy) AI agent ecosystem. Place in your user-level skills directory:

```
~/.workbuddy/skills/skill-orchestrator/
```

## License

MIT
