---
name: full-audit
description: >
  Run all web quality skills in parallel: SEO (technical, content, schema, sitemap, images,
  hreflang, page, geo, programmatic), performance, accessibility, best practices, and
  Core Web Vitals. Generates a unified report. Use when asked to "full audit", "run all
  checks", "complete site review", or "audit everything".
---

# Full Web Quality Audit

Run every Addy Osmani web-quality-skill against a target URL, then synthesize a unified report.

## Arguments

The user provides a URL (e.g., `/full-audit http://localhost:4321`). If no URL is provided, ask for one.

## Process

### Phase 1: Launch parallel subagents

Launch the following specialist agents **in parallel** using the Agent tool. Each agent receives the target URL and its specific skill instructions.

**Core Quality (4 agents):**
1. `seo-technical` — Crawlability, indexability, security, URL structure, mobile, Core Web Vitals, structured data, JS rendering
2. `seo-content` — E-E-A-T signals, readability, content depth, AI citation readiness, thin content
3. `performance` — Resource optimization, loading strategy, caching, image/font/CSS/JS optimization
4. `accessibility` — WCAG 2.1 compliance: perceivable, operable, understandable, robust

**SEO Specialists (6 agents):**
5. `seo-schema` — Detect, validate, generate Schema.org structured data (JSON-LD)
6. `seo-sitemap` — XML sitemap validation, structure, missing pages
7. `seo-images` — Alt text, file sizes, formats, responsive images, lazy loading, CLS
8. `seo-page` — On-page elements, meta tags, heading hierarchy, link text
9. `core-web-vitals` — LCP, INP, CLS measurements and optimization
10. `best-practices` — Security, modern standards, UX patterns

**Advanced SEO (3 agents — optional, launch if site has these features):**
11. `seo-hreflang` — Only if multi-language detected
12. `seo-geo` — AI Overviews / GEO optimization
13. `seo-programmatic` — Only if programmatic/template pages detected

### Phase 2: Collect results

Wait for all agents to complete. Collect findings from each.

### Phase 3: Synthesize unified report

Generate a single report with this structure:

```markdown
# Full Audit Report — {URL}
**Date:** {date}
**Skills executed:** {count}

## Health Score: {0-100}/100

| Category | Score | Issues |
|----------|-------|--------|
| Performance | {score} | {count} |
| Accessibility | {score} | {count} |
| SEO | {score} | {count} |
| Best Practices | {score} | {count} |

## Critical Issues ({count})
{grouped by category, with file paths and fix recommendations}

## High Priority ({count})
{...}

## Medium Priority ({count})
{...}

## Low Priority ({count})
{...}

## Action Plan
1. {First fix — why and how}
2. {Second fix}
...

## Per-Skill Summaries
### SEO Technical
{summary}
### Content Quality
{summary}
...
```

### Scoring

| Category | Weight | Sources |
|----------|--------|---------|
| Performance | 30% | performance, core-web-vitals |
| Accessibility | 25% | accessibility |
| SEO | 30% | seo-technical, seo-content, seo-schema, seo-sitemap, seo-images, seo-page |
| Best Practices | 15% | best-practices |

**Score per category:** Start at 100, deduct per issue severity:
- Critical: -15 points
- High: -8 points
- Medium: -3 points
- Low: -1 point
- Minimum: 0

## Important

- Always ask the user to confirm the URL before launching agents
- Use `subagent_type` matching the skill name when available (seo-technical, seo-content, seo-schema, seo-sitemap, seo-performance)
- For skills without a dedicated subagent_type, use `general-purpose` with the skill instructions in the prompt
- Present the unified report to the user, not individual agent outputs
- If the site is not running locally, remind the user to start the dev server first
