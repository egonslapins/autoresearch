# Autoresearch

Karpathy-style iterative autonomous web research engine. Searches, analyzes, and synthesizes research on any topic through an iterative improvement loop.

## Tech Stack

- **Language:** Python 3.10+
- **LLM:** OpenRouter API (default: Claude Sonnet 4)
- **Search:** SearchAPI.io (Google) or DuckDuckGo fallback
- **HTTP:** httpx
- **Storage:** Markdown (research.md) + TSV (results.tsv)
- **VCS:** Git (auto-commits on improvement)

## Architecture

```
autoresearch.py  →  CLI entry point (argparse)
researcher.py    →  Core loop: gap→search→synthesize→evaluate→commit
evaluator.py     →  LLM-based quality scoring (4 dimensions, 0-100)
searcher.py      →  Web search adapter (SearchAPI.io / DuckDuckGo / URL fetch)
program.md       →  Agent instructions (Karpathy-style)
```

### The Loop (researcher.py)

Each iteration:
1. Identify knowledge gaps in current research via LLM
2. Generate targeted search queries for each gap
3. Execute web searches + fetch top result pages
4. Synthesize findings into existing research via LLM
5. Evaluate quality score (completeness + depth + novelty + sources)
6. If score improved → write research.md + git commit
7. Log iteration to results.tsv

### Scoring (evaluator.py)

Four dimensions, 0-25 each:
- **Completeness:** All key aspects covered?
- **Depth:** Beyond surface level? Specific data?
- **Novelty:** Non-obvious, expert-level?
- **Sources:** Claims backed by URLs?

## Quick Start

```bash
cd ~/Claude\ Code/autoresearch
pip install -r requirements.txt

# Basic usage
python autoresearch.py "EU elevator compliance regulations 2026"

# With options
python autoresearch.py "AI marketing trends" -n 15 -t 70 -o marketing-report.md

# Cheaper model
python autoresearch.py "topic" --model google/gemini-2.5-flash-preview
```

## Usage from Other Projects

This is a cross-project research tool. Use from any project:

```bash
# From any directory
cd ~/Claude\ Code/autoresearch
python autoresearch.py "your research topic" --output ~/path/to/output.md

# Or with project-dir flag
python autoresearch.py "topic" --project-dir ~/Claude\ Code/some-project/
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key (in ~/.zshrc) |
| `SEARCHAPI_API_KEY` | No | SearchAPI.io key for Google Search |

## Commands

```bash
# Run research
python autoresearch.py "topic"

# See all options
python autoresearch.py --help

# Check results log
cat results.tsv | column -t -s $'\t'

# View git history of research improvements
git log --oneline research.md
```

## Output Files

| File | Description |
|---|---|
| `research.md` | The research document (iteratively improved) |
| `results.tsv` | Iteration log (score, dimensions, gaps, actions) |

## Cost Estimation

Each iteration makes ~3 LLM calls (gap identification, synthesis, evaluation).
- 10 iterations with Claude Sonnet: ~$0.50-1.00
- 10 iterations with Gemini Flash: ~$0.05-0.10

## Git Behavior

The tool auto-commits to the local git repo when research improves. Each commit message includes the iteration number and score. This mirrors Karpathy's original pattern where successful training improvements are committed.
