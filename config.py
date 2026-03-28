"""
config.py — User configuration for patent-lookup-tool
"""

# ── INPUT / OUTPUT FILES ──────────────────────────────────────────────────────
INPUT_FILE  = "patents.xlsx"
OUTPUT_XLSX = "patent_results.xlsx"
OUTPUT_TXT  = "patent_summary.txt"
CACHE_FILE  = "patent_cache.json"

# ── ORGANIZATION NAME ─────────────────────────────────────────────────────────
# Used in the summary report header
ORG_NAME = "My Organization"

# ── SCRAPING BEHAVIOR ─────────────────────────────────────────────────────────
DELAY_MIN = 3.0   # Minimum seconds between requests (be polite to Google)
DELAY_MAX = 6.0   # Maximum seconds between requests

# ── INPUT COLUMN AUTO-DETECTION ───────────────────────────────────────────────
# The script will try to match your spreadsheet's column names automatically
# using fuzzy matching. You only need to add entries here if auto-detection
# fails (e.g. your column is named something unexpected).
#
# Keys are internal names. Values are lists of possible column names to try,
# in order of preference. The first match found in your spreadsheet is used.
COL_ALIASES = {
    "family_id":   ["Tech ID", "Family ID", "Case ID", "Docket", "Reference"],
    "title":       ["Title", "Invention Title", "Patent Title", "Description"],
    "serial":      ["Serial Number", "Application Number", "App Number", "Serial No", "Appl No"],
    "patent_num":  ["Patent Number", "Patent No", "Grant Number", "Issued Patent"],
    "pub_num":     ["Publication Number", "Pub Number", "Publication No", "WO Number"],
    "file_date":   ["File Date", "Filing Date", "Application Date", "Filed"],
    "status":      ["Status", "Application Status", "Filing Status"],
    "status_date": ["Status Date", "Status Updated", "Date of Status"],
    "country":     ["Country", "Filing Country", "Jurisdiction"],
    "inventors":   ["Inventors", "Inventor", "Inventor Names", "Named Inventors"],
    "mgr_first":   ["Licensing Manager First Name", "Manager First", "LM First"],
    "mgr_last":    ["Licensing Manager Last Name", "Manager Last", "LM Last"],
}
