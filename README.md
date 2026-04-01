# autoresearch

Karpathy-style iterative autonomous web research engine.

Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch), which iteratively improves ML model training. This adaptation applies the same loop concept to **web research**: search the web, synthesize findings, evaluate quality, commit improvements, repeat.

## How It Works

```
WHILE not done:
  1. Read current research state
  2. Identify knowledge gaps via LLM
  3. Execute targeted web searches
  4. Synthesize new findings with existing research
  5. Evaluate quality score (0-100)
  6. IF improved → update research.md + git commit
     ELSE → skip
  7. Log iteration to results.tsv
  8. Repeat until threshold or max iterations
```

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic
python autoresearch.py "EU elevator compliance regulations 2026"

# With options
python autoresearch.py "AI agents in marketing" \
  --max-iterations 15 \
  --threshold 70 \
  --output marketing-report.md \
  --model google/gemini-2.5-flash-preview

# All options
python autoresearch.py --help
```

## Environment

```bash
# Required
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional (enables Google Search via SearchAPI.io)
export SEARCHAPI_API_KEY="..."
```

## Output

- `research.md` — The research document, iteratively improved
- `results.tsv` — Iteration log with scores and actions

## Quality Scoring

Each iteration is scored on 4 dimensions (0-25 each):

| Dimension | What It Measures |
|---|---|
| Completeness | All key aspects covered? |
| Depth | Specific data, not just surface level? |
| Novelty | Non-obvious, expert-useful insights? |
| Sources | Claims backed by URLs? |

The loop stops when the total score reaches the threshold (default: 80/100) or max iterations are exhausted.

## License

MIT
