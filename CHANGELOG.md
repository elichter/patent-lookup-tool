# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-03-27

### Added

#### Core Lookup Engine
- Google Patents scraping with multiple fallback strategies (direct URL, XHR endpoint, JSON-LD extraction)
- Smart caching to `patent_cache.json` — saves after each scrape, skips cached records on re-run
- Polite rate limiting with configurable random delay (default 3–6s) to avoid IP throttling
- Rotating user-agent headers for more natural request patterns

#### Patent Type Support
- **US utility patents** — direct GP URL construction from serial or patent number
- **US design patents (29/xxx)** — Playwright headless browser types serial into GP search box and follows the JS redirect to the granted `USD######S1` page
- **PCT / WO applications** — EPO OPS API resolves PCT serials to WO publication numbers; falls back to Patentscope web search and Espacenet
- **Provisional applications (63/xxx, 62/xxx)** — automatically flagged as unpublishable by US law; no lookup attempted

#### EPO OPS Integration
- OAuth2 token management with auto-refresh
- PCT serial → WO publication number lookup via family endpoint
- WO publication title fetch for mismatch detection
- English abstract fetch for AI summary generation (no scraping needed for PCT families)

#### AI Invention Summaries
- Generates two summaries per patent family from scraped patent text:
  - **Technical** — precise, IP-audience language capturing core claim scope
  - **Plain English** — accessible description for business development and non-technical stakeholders
- Fetches abstract, claims, and description from Google Patents where available
- Falls back to EPO OPS API for PCT families with no GP text
- Design patents handled specially — describes ornamental scope rather than fabricating technical content
- Skips families with no published text rather than hallucinating content
- Summaries appear in Family Summary sheet and as a standalone section in the text report

#### Data Quality & Mismatch Detection
- Title + inventor overlap comparison after all lookups complete (pre-Excel-write pass)
- Stemmed word matching (strips common suffixes) for fuzzy title comparison
- Inventor last-name overlap as secondary override — handles cases where title changed between provisional and national phase
- Mismatched rows have GP data fully cleared before Excel output; warning written to Not Found Reason
- Provisional-only families flagged with distinct purple color and explanatory note

#### Excel Output (two sheets)
- **Sheet 1 — All Applications**: one row per filing with internal + GP data side by side; hyperlinked View Patent; color-coded by family; green date cells
- **Sheet 2 — Family Summary**: one row per family; AI Invention Summary column; Has PCT?; PCT Publication No.; data gap flag (⚠ YES / ⚠ partial); ✓ Found / ✗ Not found breakdown
- Alternating blue/white family color banding; amber for partial gap families; red/orange/purple for gap flags

#### Text Report (`patent_summary.txt`)
- Lookup results (found / not found / provisionals / request count / method breakdown)
- Portfolio status breakdown from internal data
- Patent family breakdown (granted / pending / PCT / design / not found counts)
- Per-family filing detail with serial numbers, statuses, and GP links
- Standalone INVENTION SUMMARIES section with Tech ID, patent number, and full AI-generated descriptions

#### Input Handling
- Auto-detection of two input formats (Format A: one row per application with headers; Format B: one row per invention, no headers)
- Fuzzy column name matching via `COL_ALIASES` — handles common variations like "Application Number", "App No", "Serial Number" automatically
- `detect_columns()` runs at startup and prints which columns were resolved
- PCT serial normalization — converts 2-digit years and missing zero-padding transparently

#### Credentials & Configuration
- `.env` file loading from script directory or working directory, with multiple fallback paths
- EPO OPS credentials: reads from `.env`, prompts at runtime if missing, press Enter to skip
- Anthropic API key: reads from `.env`, prompts at runtime if missing, press Enter to skip
- `load_keys.py` helper reads a central `APIs.txt` file and writes a clean `.env`
- All user settings centralized in `config.py` (file paths, org name, delays, column aliases)

#### Developer Experience
- Dependency check at startup — detects missing packages and offers to auto-install via pip
- Playwright availability check with informative fallback message (non-blocking)
- Conda-compatible install path documented (core packages via conda-forge, Playwright via pip)
- `sample_patents.xlsx` with four anonymized patent families covering all supported types

---

## [Unreleased]

### Planned
- Support for EP, JP, CN national phase scraping
- USPTO Patent Center API integration for richer US-specific metadata
- Streamlit web frontend
- Automated test suite with sample portfolio fixture
- GitHub Actions CI for lint and syntax checks

---

[1.0.0]: https://github.com/elichter/patent-lookup-tool/releases/tag/v1.0.0
[Unreleased]: https://github.com/elichter/patent-lookup-tool/compare/v1.0.0...HEAD
