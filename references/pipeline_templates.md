# Pipeline Templates

Pre-defined workflow templates for common multi-skill collaboration scenarios.
Each template specifies the skill sequence, data flow, and execution guidance.

---

## Template 1: WeChat Official Account Full Pipeline

**Name**: wechat-full-pipeline
**Trigger**: "写公众号文章并发布", "公众号全流程", "写微信推文", "公众号选题到发布"
**Scenario**: End-to-end WeChat official account content creation and publishing.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | wechat-search / agent-reach | Topic keywords | Trending articles, references |
| 2 | wechat-mp-writer | References + topic | Draft article (Markdown) |
| 3 | humanizer | Draft article | De-AI polished article |
| 4 | canvas-design | Article title + theme | Cover image |
| 5 | wechat-publisher | Final article + cover | Published to draft box |

### Data Flow
- Step 1 -> Step 2: Extract key points from search results, pass as writing references
- Step 2 -> Step 3: Pass raw Markdown draft
- Step 3 -> Step 4: Pass article title and theme for cover design
- Step 4 -> Step 5: Combine final article text and cover image path

### Error Handling
- If wechat-search returns no results, fall back to agent-reach for web search
- If wechat-publisher fails (login issue), save Markdown locally and instruct user to publish manually
- If canvas-design times out, use image_gen as fallback for cover image

---

## Template 2: XiaoHongShu Note Full Pipeline

**Name**: xhs-full-pipeline
**Trigger**: "做小红书笔记", "小红书全流程", "做小红书图文", "小红书选题到发布"
**Scenario**: End-to-end XiaoHongShu note creation from topic research to publishing.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | agent-reach / wechat-search | Topic keywords | Content references |
| 2 | xhs-link-to-card-pipeline | URLs or structured content | PNG cards + XHS copy |
| 3 | xiaohongshu | PNG files + title + tags + body | Published note |

### Data Flow
- Step 1 -> Step 2: Pass discovered URLs directly to pipeline
- Step 2 -> Step 3: Pass generated PNG file paths, title, tags, and body text

### Error Handling
- If xhs-link-to-card-pipeline fails for a URL, try agent-reach to extract content, then use xhs-trending-cards or canvas-design to create cards manually
- If xiaohongshu publishing fails, save all assets locally with a clear file manifest

---

## Template 3: Toutiao Content Full Pipeline

**Name**: toutiao-full-pipeline
**Trigger**: "发头条", "头条全流程", "今日头条写文章发布", "微头条到发布"
**Scenario**: End-to-end Toutiao content creation leveraging trending topics.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | toutiao-news-trends | None (auto-fetch) | Hot topic list |
| 2 | wechat-mp-writer | Selected hot topic | Draft article |
| 3 | humanizer | Draft article | Polished article |
| 4 | toutiao-publish / toutiao-publisher | Final article + images | Published post |

### Data Flow
- Step 1 -> Step 2: User selects a topic, pass topic keywords and brief description
- Step 2 -> Step 3: Pass draft Markdown
- Step 3 -> Step 4: Pass polished text and optional AI-suggested images

### Error Handling
- If toutiao-news-trends fails, fall back to agent-reach searching "今日热点" or "今日新闻"
- For short-form content (微头条), use toutiao-publisher; for long articles, use toutiao-publish

---

## Template 4: Financial Data Analysis Pipeline

**Name**: financial-analysis-pipeline
**Trigger**: "金融数据分析", "股票分析报告", "基金数据", "看下XX股票"
**Scenario**: Query financial data, analyze, and produce a visual report.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | neodata-financial-search | Stock/fund query | Raw financial data |
| 2 | xlsx (if spreadsheet needed) | Structured data | Excel file with analysis |
| 3 | canvas-design / frontend-slides | Analysis highlights | Visual report or presentation |

### Data Flow
- Step 1 -> Step 2: Extract key metrics (price, PE, volume, etc.) as structured data
- Step 2 -> Step 3: Pass summary statistics and key findings for visualization

### Error Handling
- If neodata-financial-search returns no data, try agent-reach to search for financial news
- For quick analysis, skip xlsx and directly produce a text-based report

---

## Template 5: Content Research & Knowledge Curation Pipeline

**Name**: research-to-knowledge-pipeline
**Trigger**: "研究XX话题", "帮我调研", "知识整理", "做个专题研究"
**Scenario**: Research a topic online, summarize, and store in knowledge base.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | agent-reach | Research query | Search results + content |
| 2 | summarize | URLs / content | Structured summaries |
| 3 | obsidian | Summaries + topic | Knowledge base notes |

### Data Flow
- Step 1 -> Step 2: Pass URLs and extracted content
- Step 2 -> Step 3: Pass structured summaries with key points and sources

### Error Handling
- If agent-reach returns few results, supplement with multi-search-engine
- If obsidian is not configured, save as local Markdown files organized by topic

---

## Template 6: Visual Content Creation Pipeline

**Name**: visual-creation-pipeline
**Trigger**: "做个海报", "设计封面", "做张图", "知识卡片", "视觉设计"
**Scenario**: Create visual content from concept to final output.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | canvas-design | Design brief | Visual design (.png/.pdf) |
| 2 | image_gen (if AI art needed) | Prompt from design | AI-generated images |
| 3 | xhs-trending-cards (if XHS format) | Content + ranking data | XHS-format cards |

### Data Flow
- Step 1 produces the primary visual output
- Step 2 supplements with AI-generated imagery if canvas-design suggests it
- Step 3 is optional for XHS-specific card format

### Error Handling
- If canvas-design fails or times out, fall back to image_gen for AI-generated visuals
- If image_gen also fails, use HTML+CSS approach to create the visual locally

---

## Template 7: Video Content Pipeline

**Name**: video-content-pipeline
**Trigger**: "生成视频", "做个视频", "视频内容", "图生视频"
**Scenario**: Create video content from concept or existing images.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | agent-reach (if research needed) | Topic query | Content research |
| 2 | libtv / video-generator-seedance | Script or image + prompt | Generated video |
| 3 | openai-whisper (if transcription needed) | Audio/video file | Transcription text |

### Data Flow
- Step 1 is optional, only if research is needed before video creation
- Step 2 is the core: libtv for image/video generation, seedance for text-to-video
- Step 3 is optional, for post-processing transcriptions

### Error Handling
- If libtv API fails, try video-generator-seedance as alternative
- If both video generation APIs fail, use frontend-slides to create an animated HTML presentation as fallback

---

## Template 8: Cross-Platform Content Distribution Pipeline

**Name**: cross-platform-distribution
**Trigger**: "多平台发布", "全网分发", "同时发到", "一键多平台"
**Scenario**: Create content once and distribute to multiple social platforms.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | wechat-mp-writer | Topic + references | Base article (Markdown) |
| 2 | humanizer | Base article | Polished article |
| 3a | wechat-publisher | Polished article | WeChat published |
| 3b | toutiao-publish | Polished article | Toutiao published |
| 3c | xhs-link-to-card-pipeline | Key points from article | XHS cards + copy |
| 3d | xiaohongshu | XHS cards + copy | XHS published |

### Data Flow
- Step 2 -> Step 3a/3b/3c: The same polished article feeds multiple distribution channels
- 3c -> 3d: XHS-specific content flows from card pipeline to XHS publisher
- Steps 3a, 3b, 3d are independent and can run in parallel

### Error Handling
- If any single platform fails, continue with other platforms
- Each platform may need format adaptation (e.g., XHS needs image cards, Toutiao needs different tag format)
- Save all generated content locally as backup

---

## Custom Pipeline Template Specification

To define your own pipeline, follow this format:

```markdown
## Template N: [Your Pipeline Name]

**Name**: [unique-kebab-case-id]
**Trigger**: "trigger phrase 1", "trigger phrase 2"
**Scenario**: One-line description of what this pipeline accomplishes.

### Skill Sequence

| Step | Skill | Input | Output |
|------|-------|-------|--------|
| 1 | [skill-name] | [what it receives] | [what it produces] |
| 2 | [skill-name] | [what it receives] | [what it produces] |

### Data Flow
- Step X -> Step Y: [How data is passed between steps]

### Error Handling
- If [skill] fails: [fallback strategy]
```

### Guidelines for Creating Templates

1. Each step should map to exactly one skill with a clear, singular purpose
2. Define data flow explicitly - what exact format is passed between steps
3. Always include at least one fallback strategy for the most critical step
4. Consider parallel execution when steps are independent (e.g., publishing to multiple platforms)
5. Include the trigger phrases that users would naturally say to invoke this pipeline
6. Keep pipelines focused - if it needs more than 5 steps, consider splitting into two pipelines
