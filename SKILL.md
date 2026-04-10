---
name: skill-orchestrator
description: >
  Skill orchestration engine that discovers, selects, and chains multiple skills
  to complete complex tasks. Use when: (1) user task requires multiple skills
  working together, (2) user says "全流程", "一站式", "编排", "流水线",
  "skill组合", "帮我用skill", "多个skill", "协作", (3) task spans
  information gathering + content creation + publishing, (4) user wants
  cross-platform content distribution, (5) a single skill cannot fully
  address the request, (6) user asks to combine or chain capabilities
  like "search and publish", "research and create cards", "write and design".
  Reads references/skill_registry.md for skill capabilities, and
  references/pipeline_templates.md for pre-built workflows.
---

# Skill Orchestrator

Orchestrate multiple skills to accomplish tasks no single skill can handle alone.

## Core Principle

This skill is a meta-skill: it does NOT execute work directly. It analyzes tasks,
selects the right skill combination, defines execution order, and guides the AI
through each step with proper data handoff between skills.

## Quick Decision: Does This Task Need Orchestration?

Ask: "Can one skill handle this end-to-end?"

- **YES** -> Use that skill directly. Do NOT invoke skill-orchestrator.
- **NO** -> The task spans multiple capabilities. Continue below.

Examples of orchestration-needed tasks:
- "Write a WeChat article and publish it" (write + publish = 2 skills)
- "Research this topic and make XHS cards" (search + card-gen = 2 skills)
- "Find trending topics, write article, publish everywhere" (3+ skills)
- "Analyze this stock and make a visual report" (data + design = 2 skills)

## Orchestration Workflow

### Step 1: Task Analysis

Decompose the user's task into sub-tasks. For each sub-task, identify:
- What capability is needed (search, write, design, publish, analyze, etc.)
- What input the sub-task requires
- What output it should produce
- Whether it depends on a previous sub-task's output

Output a sub-task list like:
```
Sub-task 1: [capability] -> [expected output]
Sub-task 2: [capability] -> [expected output] (needs output from Sub-task 1)
...
```

### Step 2: Skill Matching

Read `references/skill_registry.md` to find matching skills for each sub-task.

Matching rules:
1. Check the category that matches the sub-task capability
2. For each skill in that category, evaluate if its description covers the sub-task
3. If multiple skills match, prefer: installed over not-installed, simpler over complex
4. If no local skill matches, use find-skills to search externally: `npx skills find [query]`
5. If still no match, note the gap and inform the user

### Step 3: Pipeline Selection or Construction

**Option A: Match existing template**

Read `references/pipeline_templates.md`. If the task matches a template trigger:
1. Load that template
2. Present the pipeline to the user: "I'll use the [template-name] pipeline: Step 1 -> Step 2 -> ..."
3. Proceed to execution

**Option B: Dynamic construction**

If no template matches:
1. Order sub-tasks by dependency (independent tasks can be parallel)
2. Define data handoff between each step: what specific data flows from step N to step N+1
3. Add error handling: for each critical step, identify a fallback skill
4. Present the constructed pipeline to the user before executing

### Step 4: Execution

Execute the pipeline step by step. For each step:

1. **Invoke the skill**: Use `use_skill` tool to load the skill, then follow its instructions
2. **Capture output**: Save the step's output to a known location or variable
3. **Transform if needed**: Adapt the output format for the next skill's input
4. **Pass to next step**: Feed transformed data into the next skill

Critical execution rules:
- After each step completes, briefly confirm the output before proceeding
- If a step fails, try the fallback skill before stopping
- If a step produces unexpected output, reassess whether subsequent steps need adjustment
- Never skip data transformation between steps - each skill expects specific input formats

### Step 5: Completion

After all steps complete:
1. Summarize what was accomplished at each step
2. List all output files with their locations
3. Note any steps that had issues or used fallback skills
4. Suggest if the workflow should be saved as a custom pipeline template

## Data Transformation Patterns

Common patterns for passing data between skills:

| From Skill | To Skill | Transformation |
|---|---|---|
| agent-reach search results | wechat-mp-writer | Extract key points as writing references |
| agent-reach URLs | xhs-link-to-card-pipeline | Pass URLs directly |
| wechat-mp-writer draft | humanizer | Pass raw Markdown text |
| humanizer polished text | wechat-publisher | Pass final Markdown |
| humanizer polished text | toutiao-publish | Extract plain text + images |
| toutiao-news-trends hot topics | wechat-mp-writer | Pass topic keywords + summary |
| xhs-link-to-card-pipeline output | xiaohongshu | Pass PNG paths + title + tags + body |
| neodata-financial-search data | xlsx | Structure as tabular data |
| canvas-design output | wechat-publisher | Pass image file path as cover |
| summarize output | obsidian | Format as Markdown note with metadata |

## Skill Discovery: Finding Skills Beyond Local

When the registry lacks a needed capability:

1. **Search external market**:
   ```bash
   npx skills find [query]
   ```

2. **Check installed but uncategorized**: Some skills may be misclassified. Do a keyword search in the registry.

3. **Consider tool-native capabilities**: Before searching for a skill, check if the AI's built-in tools (web_search, web_fetch, image_gen, etc.) can handle the sub-task without a skill.

4. **Compose from primitives**: If no skill exists for a specific sub-task, the AI can often accomplish it using basic tools (read_file, write_to_file, execute_command) guided by domain knowledge.

## Refreshing the Skill Registry

When skills are added, removed, or updated, refresh the registry:

```bash
python scripts/scan_skills.py --paths [skill-directories] --output references/skill_registry.md
```

Default paths: `~/.workbuddy/skills`

Run this when:
- User installs a new skill
- User says "refresh skills" or "update registry"
- A skill lookup fails and you suspect the registry is stale

## Common Orchestration Patterns

### Pattern 1: Research-Create-Publish
```
[gather info] -> [create content] -> [polish] -> [publish]
   agent-reach     wechat-mp-writer  humanizer   wechat-publisher
```

### Pattern 2: Data-Analyze-Visualize
```
[fetch data] -> [analyze] -> [visualize]
   neodata       xlsx       canvas-design
```

### Pattern 3: Content-Adapt-Distribute
```
[create base content] -> [adapt per platform] -> [publish each]
   wechat-mp-writer       format transform      multiple publishers
```

### Pattern 4: Search-Transform-Store
```
[search] -> [summarize/extract] -> [store]
  agent-reach    summarize          obsidian
```

## Error Handling Strategy

For each pipeline step, follow this escalation:

1. **Retry once** - The skill may have encountered a transient issue
2. **Use fallback skill** - Check the pipeline template for the designated fallback
3. **Use built-in tools** - Accomplish the sub-task using native AI capabilities
4. **Skip and continue** - If the step is non-critical, skip it and proceed
5. **Stop and report** - If a critical step fails with no workaround, stop and tell the user what failed and why

## References

- `references/skill_registry.md` - Categorized list of all installed skills with capabilities
- `references/pipeline_templates.md` - Pre-built workflow templates for common scenarios
