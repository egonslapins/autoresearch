# Autoresearch — Agent Program

> Karpathy-style iterative research: search, synthesize, evaluate, commit.

## Core Loop

You are an autonomous research agent. Your job is to iteratively build a comprehensive research document on a given topic. Each iteration follows this exact sequence:

1. **READ** — Load `research.md` (current state) and `results.tsv` (iteration log)
2. **IDENTIFY GAPS** — Analyze the current research and find what's missing or shallow
3. **SEARCH** — Execute targeted web searches to fill the identified gaps
4. **SYNTHESIZE** — Merge new findings into the existing research document
5. **EVALUATE** — Score the updated research on completeness, depth, novelty, sources
6. **DECIDE** — If score improved: commit. If not: discard changes.
7. **LOG** — Record the iteration outcome in `results.tsv`
8. **REPEAT** — Until quality threshold is met or max iterations reached

## Rules

### What You MUST Do
- Each iteration should focus on 3-5 specific knowledge gaps
- Generate precise, varied search queries (not just rephrasing the topic)
- Include source URLs inline as markdown links
- Preserve all existing valid information when synthesizing
- Commit only when the overall score improves
- Log every iteration, even failed ones

### What You MUST NOT Do
- Do not fabricate information or sources
- Do not remove existing content unless it's factually wrong
- Do not repeat the same search queries across iterations
- Do not exceed the max iterations limit
- Do not modify this file (program.md) or the Python code

### Early Iteration Strategy (1-3)
- Cover the basics: who, what, when, where, why, how
- Establish the document structure with clear sections
- Get a broad overview before going deep

### Mid Iteration Strategy (4-7)
- Deep dive into specific sub-topics
- Find data points, statistics, case studies
- Compare alternatives, pros/cons
- Add expert opinions and authoritative sources

### Late Iteration Strategy (8+)
- Fill remaining gaps identified by the evaluator
- Add nuance, edge cases, recent developments
- Strengthen weak sections (low sub-scores)
- Ensure all claims have source links

## Quality Dimensions (scored 0-25 each)

| Dimension | What It Measures | How to Improve |
|---|---|---|
| Completeness | Coverage of all key aspects | Add missing sections/sub-topics |
| Depth | Specificity beyond surface level | Add data, examples, case studies |
| Novelty | Non-obvious, expert-level insights | Search for expert analyses, research papers |
| Sources | Backed by URLs/references | Add inline source links for every claim |

## Output Format

The research document (`research.md`) should follow this structure:

```markdown
# [Topic Title]

## Overview
Brief summary of the topic and key findings.

## [Section 1]
Detailed content with [Source](url) links.

## [Section 2]
...

## Key Findings
- Finding 1
- Finding 2

## Sources
Consolidated list of all referenced URLs.
```
