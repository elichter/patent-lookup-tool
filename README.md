# 🔬 Patent Lookup Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Google Patents](https://img.shields.io/badge/Source-Google%20Patents-4285F4?logo=google&logoColor=white)
![EPO OPS](https://img.shields.io/badge/API-EPO%20OPS-003087)
![Claude AI](https://img.shields.io/badge/AI-Claude%20Sonnet-blueviolet?logo=anthropic)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**Turn a raw patent spreadsheet into structured, analysis-ready intelligence — automatically.**

[Quick Start](#-quick-start) · [Features](#-features) · [AI Summaries](#-ai-powered-invention-summaries) · [Output](#-output) · [Configuration](#-configuration) · [Contributing](#-contributing)

</div>

---

## 🧩 The Problem

Patent teams, tech transfer offices, and IP researchers deal with the same pain:

> *You have a spreadsheet of patent applications. You need current status, dates, assignees, and family relationships — and it's all scattered across Google Patents, WIPO, and EPO. Updating it manually takes hours and goes stale immediately. And even when you have the data, you still need to explain each invention in plain English for licensing conversations.*

**This tool automates all of it.**

---

## ⚡ What It Does

Give it a spreadsheet of patent application numbers. It returns a clean, formatted Excel workbook with everything — fetched automatically from public databases, with AI-generated summaries for every invention.

```
Input:  patents.xlsx          (your raw list of application numbers)
              ↓
   patent_lookup.py           (~5 seconds per patent, runs unattended)
              ↓
Output: patent_results.xlsx   ✓ statuses, dates, links, family summaries
        patent_summary.txt    ✓ portfolio breakdown + AI invention summaries
```

---

## 🤖 Plain-English Invention Summaries — Automatically

Most patent tools stop at the data. This one doesn't.

For every patent family in your portfolio, the tool reads the abstract, claims, and description — then writes you two summaries you can actually use:

> **A technical summary** — precise enough for IP counsel, patent agents, and licensing due diligence. One sentence capturing the core claim scope in language an IP-literate reader expects.
>
> **A plain-English summary** — written for business development, executives, and industry partners who need to understand the invention without a law degree.

For example:

```
Technical: A portable toilet transfer device featuring a clip mechanism with interior
           and exterior engagement members that secures to a toilet bowl rim and
           connects to a weight-bearing handle for wheelchair-to-toilet transfers.

Plain:     A removable handle that clamps onto a toilet bowl to help wheelchair users
           safely transfer onto and off of the toilet seat.
```

**No prompting. No copy-pasting. No reading claims.** Just run the tool.

These summaries show up in the Family Summary sheet and in a dedicated section of the text report — ready to drop into a licensing one-pager, an annual report, or a board presentation.

**What it handles automatically:**
- Fetches full patent text from Google Patents where available
- Falls back to EPO's API for PCT families with no GP text
- Handles design patents correctly — explains they protect appearance, not function
- Skips families with no published text rather than making something up

**Who uses these summaries:**
- Tech transfer managers briefing leadership on the portfolio
- Licensing teams preparing outreach to industry partners
- Researchers documenting their innovation outputs
- Anyone who has ever spent 20 minutes reading a patent just to explain it in one sentence

**Cost:** roughly $0.02 per full run on a 20–30 patent portfolio. A $5 credit covers hundreds of runs.

---

## ✨ Full Feature List

| Feature | Description |
|---|---|
| 🤖 **Plain-English summaries** | Automatically generates technical + plain-English invention descriptions — no prompting required |
| 🔎 **Google Patents scraping** | Direct URL, XHR endpoint, JSON-LD — multiple fallback strategies |
| 🌍 **PCT / WO lookup** | EPO OPS API resolves PCT serials to WO publication numbers + abstracts |
| 🎨 **Design patent support** | Playwright headless browser types `29/xxxxxx` into GP search box |
| 👨‍👩‍👧 **Patent family grouping** | Aggregates all related filings under a shared family ID |
| ⚠️ **Data quality flags** | Detects title/inventor mismatches, wrong patents, provisional-only families |
| 📊 **Color-coded Excel output** | Two sheets — all applications + family summary — with conditional formatting |
| ⚡ **Smart caching** | Results saved after each scrape; re-runs skip already-fetched records |
| 🔑 **Zero mandatory API keys** | Works out of the box; EPO + Anthropic keys unlock additional features |

---

## 🎯 Built For

- **Tech transfer offices** — portfolio tracking, licensing diligence, annual reporting, and ready-to-use invention descriptions
- **IP counsel & patent agents** — quickly audit and summarize a client's filing portfolio without reading every claim
- **Research institutions** — map innovation outputs to public patent records with plain-English context for non-technical stakeholders
- **Data scientists & developers** — structured patent data + auto-generated descriptions as a foundation for analysis

---

## 🚀 Quick Start

### 1. Install

**Option A — pip (recommended)**
```bash
git clone https://github.com/elichter/patent-lookup-tool
cd patent-lookup-tool
pip install -r requirements.txt
playwright install chromium      # only needed for design patents (29/xxx serials)
```

**Option B — conda**
```bash
git clone https://github.com/elichter/patent-lookup-tool
cd patent-lookup-tool
conda create -n patent-lookup python=3.11
conda activate patent-lookup
conda install -c conda-forge requests beautifulsoup4 lxml pandas openpyxl python-dotenv
pip install playwright            # playwright not on conda-forge; install via pip
playwright install chromium
```

**Option C — manual (if you prefer to control your environment)**

Core requirements (all pip-installable):
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
pandas>=2.0.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
```
Optional (only needed for design patents):
```
playwright>=1.40.0   →   pip install playwright && playwright install chromium
```

> **Don't want to install manually?** Just run `python patent_lookup.py` — it detects missing packages and asks if you'd like to install them automatically.

### 2. Add your spreadsheet

Drop your patent list as `patents.xlsx` in the project folder.
The tool auto-detects column names — no configuration required for standard formats.
See [Input Format](#-input-format) for details.

### 3. (Optional but recommended) Add API keys

```bash
cp .env.example .env
# Edit .env with your EPO and/or Anthropic keys
```

| Key | Where to get it | What it unlocks |
|---|---|---|
| `EPO_KEY` + `EPO_SECRET` | [developers.epo.org](https://developers.epo.org) — free | PCT → WO lookup, EPO abstract fetching |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) — pay-as-you-go | **AI invention summaries** (~$0.02/run) |

> The tool works without any API keys — but the AI summaries are the most valuable output. A $5 credit will last hundreds of runs.

### 4. Run

```bash
python patent_lookup.py
```

Output files appear in the same folder: `patent_results.xlsx` and `patent_summary.txt`.

---

## 📁 Input Format

The tool auto-detects column names using fuzzy matching — `Application Number`, `App No`, and `Serial Number` all work automatically.

### Format A — Patent applications list *(recommended)*

One row per patent application, with a header row:

| Column | Example | Notes |
|---|---|---|
| Family ID | `SMITH_JON.001` | Groups related filings together |
| Title | `Widget for reducing friction` | Invention title |
| Serial Number | `17/072,674` or `PCT/US23/75015` | US, design, or PCT format |
| Patent Number | `12,121,656` or `D874,011` | Leave blank if pending |
| Publication Number | `WO 2023/064756` | Optional |
| File Date | `2020-10-16` | Any standard date format |
| Status | `Pending`, `Issued`, `Expired` | Your internal status |
| Inventors | `Smith, John, Doe, Jane` | Comma-separated |
| Country | `United States` | Filing country |

Column name aliases are fully configurable in `config.py`.

### Format B — Technology list

One row per invention (not per filing). Configure column positions in `config.py`.

---

## 📊 Output

### `patent_results.xlsx`

**Sheet 1 — All Applications**

One row per patent application — your internal data alongside GP-fetched fields:

- GP Title, Status, Filing / Priority / Issue / Expiration dates
- GP Assignee and Inventors, WO Publication Number
- Hyperlinked "View Patent" link
- Search method used + not-found reason
- Data quality flags (mismatch warnings)

Color-coded by patent family, with green highlighting for populated date fields.

**Sheet 2 — Family Summary**

One row per patent family:

- Invention title, all filings listed, overall status
- Earliest priority date, latest expiration date
- Has PCT? + PCT Publication Number
- **🤖 AI Invention Summary** — technical + plain-English description, one sentence each
- Data gap flag: `⚠ YES` / `⚠ partial` / clean
- Breakdown: `✓ Found: title A | ✗ Not found: title B`
- Mismatch warning if a serial number resolves to the wrong patent

### `patent_summary.txt`

Text report including:

- Lookup statistics (found / not found / provisionals / requests made)
- Portfolio status breakdown (internal data)
- Patent family breakdown (granted / pending / PCT / design counts)
- Per-family filing detail with links
- **🤖 INVENTION SUMMARIES** — standalone section with Tech ID, patent number, and full AI-generated technical + plain-English description for every family with available patent text

---

## 🔍 How Lookup Works

For each filing the tool tries strategies in order, stopping at first success:

```
63/xxx, 62/xxx  →  Flagged as provisional (legally unpublishable by US law)
29/xxx          →  Playwright types serial into GP search → follows JS redirect to USD######S1
PCT/USxx/xxxxx  →  EPO OPS API (WO number + abstract) → GP search → WIPO Patentscope
US + patent#    →  Direct GP URL (USD######S1 or US########B2)
US pending      →  Direct GP URL → title + inventor keyword search fallback
```

**Mismatch detection:** After all lookups complete, the tool compares internal titles and inventors against GP results using stemmed word overlap. If both title overlap (< 20%) and inventor overlap fail, the row is flagged, GP data is cleared, and a warning is written explaining the likely data entry error.

---

## ⚙️ Configuration

All user settings live in `config.py`:

```python
INPUT_FILE = "patents.xlsx"     # your input file
ORG_NAME   = "My Organization"  # appears in the summary report

DELAY_MIN = 3.0  # seconds between requests (be polite to Google)
DELAY_MAX = 6.0

# Column name aliases — extend these if auto-detection misses your column names
COL_ALIASES = {
    "family_id": ["Tech ID", "Family ID", "Case ID", "Docket"],
    "serial":    ["Serial Number", "Application Number", "App No"],
    # ... see config.py for full list
}
```

---

## 🗂️ Project Structure

```
patent-lookup-tool/
├── patent_lookup.py    # Main script
├── config.py           # All user configuration
├── load_keys.py        # Helper: reads a central API keys file → writes .env
├── requirements.txt    # Python dependencies
├── sample_patents.xlsx # Anonymized sample input (4 families, all patent types)
├── .env.example        # API key template
├── .gitignore
└── README.md
```

---

## 🔄 Caching

Results are saved to `patent_cache.json` after each scrape. Re-runs skip cached records instantly — a 24-record portfolio runs in ~2 minutes on first run and under 5 seconds on re-run.

```bash
# Remove a specific entry to force re-scrape
python3 -c "
import json; c = json.load(open('patent_cache.json'))
c.pop('17/072,674', None)
json.dump(c, open('patent_cache.json','w'), indent=2)
"

# Clear all cache
rm patent_cache.json
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `requests` + `beautifulsoup4` + `lxml` | HTTP requests and HTML parsing |
| `playwright` | Headless Chromium for JS-rendered pages |
| `pandas` + `openpyxl` | Excel I/O and formatting |
| `python-dotenv` | `.env` file loading |
| EPO OPS API *(free, key required)* | PCT → WO lookup + abstract fetching |
| Anthropic API *(pay-as-you-go, optional)* | **AI invention summaries via Claude** |

---

## ⚠️ Notes & Limitations

- **Rate limiting** — 3–6 second delays between requests by default. Don't reduce below 2s or Google will throttle your IP.
- **US pending apps** — applications filed less than 18 months ago are not yet published and won't appear on GP. This is expected and flagged in the output.
- **Design patents** — require Playwright. Without it, design patent rows fall back to a GP search link only.
- **PCT/WO lookup** — requires free EPO OPS credentials. Without them, PCT entries get a WIPO search link.
- **AI summaries** — require an Anthropic API key. Without one, the Invention Summary column is left blank. A $5 credit covers hundreds of runs.
- **Terms of service** — this tool scrapes public patent data. Use responsibly and in accordance with Google Patents' ToS.

---

## 🤝 Contributing

Contributions are welcome. Please fork the repo and submit a pull request.

This project uses [git-cliff](https://git-cliff.org) for changelog generation. When committing, use conventional commit prefixes for best results:

| Prefix | Changelog section |
|---|---|
| `feat:` or `add:` | Added |
| `fix:` or `bug:` | Fixed |
| `update:` or `change:` | Changed |
| `remove:` | Removed |
| `doc:` or `readme:` | Documentation |
| `chore:` or `ci:` | *(skipped)* |

See `generate_changelog.sh` for the full release workflow.

Ideas for improvement:

- Support for EP, JP, CN national phase scraping
- USPTO Patent Center API for richer US-specific metadata
- Streamlit or FastAPI web frontend
- Automated tests with a sample portfolio fixture
- GitHub Actions CI for lint + syntax checks

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

<div align="center">
<i>Built for patent teams who have better things to do than copy-paste from Google Patents.</i>
<br><br>
<i>Run it once. Walk away with summaries you can actually use.</i>
</div>
