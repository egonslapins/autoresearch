"""
Web search adapter for autoresearch.

Supports multiple search backends (priority order):
1. Perplexity Sonar API — best quality, returns cited answers (PERPLEXITY_API_KEY)
2. SearchAPI.io (Google Search) — raw search results (SEARCHAPI_API_KEY)
3. DuckDuckGo HTML lite — free fallback (unreliable)
4. Direct URL fetching via httpx
"""

from __future__ import annotations

import os
import json
import logging
import time
from dataclasses import dataclass, field

import httpx

logger = logging.getLogger(__name__)

SEARCHAPI_BASE = "https://www.searchapi.io/api/v1/search"
PERPLEXITY_BASE = "https://api.perplexity.ai/chat/completions"
DEFAULT_TIMEOUT = 30.0

# Path to centralized credentials
VT_SHARED_ENV = os.path.expanduser("~/Claude Code/vt-shared/.env")


def _load_key_from_vt_shared(key_name: str) -> str:
    """Load a key from vt-shared/.env (plain text, single source of truth)."""
    try:
        with open(VT_SHARED_ENV) as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{key_name}=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip()
    except FileNotFoundError:
        pass
    return ""


@dataclass
class SearchResult:
    """A single search result."""
    url: str
    title: str
    snippet: str
    content: str = ""  # Full page content if fetched


@dataclass
class Searcher:
    """Web search adapter with multiple backends."""
    searchapi_key: str | None = field(default=None)
    perplexity_key: str | None = field(default=None)
    timeout: float = DEFAULT_TIMEOUT

    def __post_init__(self):
        if self.searchapi_key is None:
            self.searchapi_key = os.environ.get("SEARCHAPI_API_KEY") or _load_key_from_vt_shared("SEARCHAPI_API_KEY") or None
        if self.perplexity_key is None:
            self.perplexity_key = os.environ.get("PERPLEXITY_API_KEY") or _load_key_from_vt_shared("PERPLEXITY_API_KEY") or None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(self, queries: list[str], max_results_per_query: int = 5) -> list[SearchResult]:
        """Execute multiple search queries and return combined results."""
        all_results: list[SearchResult] = []
        seen_urls: set[str] = set()

        for query in queries:
            try:
                results = self._search_single(query, max_results_per_query)
                for r in results:
                    if r.url not in seen_urls:
                        seen_urls.add(r.url)
                        all_results.append(r)
            except Exception as e:
                logger.warning("Search failed for query %r: %s", query, e)

        return all_results

    def fetch_url(self, url: str) -> str:
        """Fetch full text content from a URL."""
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
                resp.raise_for_status()
                return self._extract_text(resp.text)
        except Exception as e:
            logger.warning("Failed to fetch %s: %s", url, e)
            return ""

    # ------------------------------------------------------------------
    # Private — search backends
    # ------------------------------------------------------------------

    def _search_single(self, query: str, max_results: int) -> list[SearchResult]:
        """Search using the best available backend (priority: Perplexity > SearchAPI > DDG)."""
        if self.perplexity_key:
            results = self._search_perplexity(query, max_results)
            if results:
                return results
            logger.warning("Perplexity returned no results, trying fallbacks")
        if self.searchapi_key:
            return self._search_searchapi(query, max_results)
        return self._search_duckduckgo_html(query, max_results)

    def _search_perplexity(self, query: str, max_results: int) -> list[SearchResult]:
        """Search via Perplexity Sonar API — returns answer + cited sources."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(
                    PERPLEXITY_BASE,
                    headers={
                        "Authorization": f"Bearer {self.perplexity_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "sonar",
                        "messages": [
                            {"role": "system", "content": "Provide factual answers with specific data, statistics, and dates. Be comprehensive."},
                            {"role": "user", "content": query},
                        ],
                    },
                )
                resp.raise_for_status()
                data = resp.json()

            results: list[SearchResult] = []
            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            citations = data.get("citations", [])

            # Create a result from the synthesized answer
            if answer:
                results.append(SearchResult(
                    url="perplexity:sonar",
                    title=f"Perplexity: {query[:80]}",
                    snippet=answer[:300],
                    content=answer,
                ))

            # Add individual cited sources
            for url in citations[:max_results - 1]:
                results.append(SearchResult(
                    url=url,
                    title=url.split("/")[-1][:60] if "/" in url else url[:60],
                    snippet="",
                ))

            return results
        except Exception as e:
            logger.warning("Perplexity search failed for query %r: %s", query, e)
            return []

    def _search_searchapi(self, query: str, max_results: int) -> list[SearchResult]:
        """Search via SearchAPI.io (Google Search)."""
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(
                SEARCHAPI_BASE,
                params={
                    "engine": "google",
                    "q": query,
                    "num": max_results,
                    "api_key": self.searchapi_key,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        results: list[SearchResult] = []
        for item in data.get("organic_results", [])[:max_results]:
            results.append(SearchResult(
                url=item.get("link", ""),
                title=item.get("title", ""),
                snippet=item.get("snippet", ""),
            ))
        return results

    def _search_duckduckgo_html(self, query: str, max_results: int) -> list[SearchResult]:
        """Fallback: scrape DuckDuckGo HTML lite (no API key needed)."""
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(
                    "https://html.duckduckgo.com/html/",
                    params={"q": query},
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"},
                )
                resp.raise_for_status()
                return self._parse_ddg_html(resp.text, max_results)
        except Exception as e:
            logger.warning("DuckDuckGo search failed: %s", e)
            return []

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def _parse_ddg_html(self, html: str, max_results: int) -> list[SearchResult]:
        """Parse DuckDuckGo HTML lite results without external HTML parser."""
        results: list[SearchResult] = []
        # DuckDuckGo HTML lite has results in <a class="result__a" href="...">
        parts = html.split('class="result__a"')
        for part in parts[1 : max_results + 1]:
            try:
                # Extract URL
                href_start = part.index('href="') + 6
                href_end = part.index('"', href_start)
                url = part[href_start:href_end]

                # Extract title (text between > and </a>)
                tag_end = part.index(">") + 1
                title_end = part.index("</a>")
                title = part[tag_end:title_end].strip()
                title = self._strip_tags(title)

                # Extract snippet
                snippet = ""
                snippet_marker = 'class="result__snippet"'
                if snippet_marker in part:
                    snip_start = part.index(snippet_marker)
                    snip_tag_end = part.index(">", snip_start) + 1
                    snip_end = part.index("</", snip_tag_end)
                    snippet = self._strip_tags(part[snip_tag_end:snip_end]).strip()

                if url.startswith("//duckduckgo.com/l/?uddg="):
                    # Decode redirect URL
                    import urllib.parse
                    url = urllib.parse.unquote(url.split("uddg=")[1].split("&")[0])

                results.append(SearchResult(url=url, title=title, snippet=snippet))
            except (ValueError, IndexError):
                continue

        return results

    @staticmethod
    def _strip_tags(html: str) -> str:
        """Remove HTML tags from a string."""
        import re
        return re.sub(r"<[^>]+>", "", html)

    @staticmethod
    def _extract_text(html: str) -> str:
        """Extract readable text from HTML (basic approach)."""
        import re
        # Remove script and style blocks
        text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
        # Remove tags
        text = re.sub(r"<[^>]+>", " ", text)
        # Collapse whitespace
        text = re.sub(r"\s+", " ", text).strip()
        # Decode common entities
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
        # Truncate to avoid blowing up LLM context
        if len(text) > 15000:
            text = text[:15000] + "\n\n[... truncated ...]"
        return text
