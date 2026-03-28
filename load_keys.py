"""
load_keys.py
Reads API keys from APIs.txt and writes them to a .env file.
Fully automatic — no hardcoded key names. Any new keys you add to APIs.txt
will be picked up automatically on next run.

Usage:
    python load_keys.py
    python load_keys.py --apis "C:/path/to/APIs.txt"
    python load_keys.py --env "/path/to/output/.env"
"""

import re
import os
import argparse

DEFAULT_APIS_PATH = r"C:\Users\licht\Dropbox\Career\TJU_tech_transfer\Admin\APIs.txt"

SUBKEY_PATTERNS = [
    r"^consumer", r"^secret", r"^api key", r"^access",
    r"^token", r"^private", r"^public", r"^client",
    r"^username", r"^password",
]

ALIASES = {
    "CLAUDE":                  "ANTHROPIC_API_KEY",
    "ANTHROPIC":               "ANTHROPIC_API_KEY",
    "EPO_CONSUMER_KEY":        "EPO_KEY",
    "EPO_CONSUMER_SECRET_KEY": "EPO_SECRET",
    "SERAPI":                  "SERPAPI_KEY",
    "SERPAPI":                 "SERPAPI_KEY",
    "USPTP":                   "USPTO_API_KEY",
    "USPTO":                   "USPTO_API_KEY",
}

def is_subkey(name, current_section):
    if not current_section:
        return False
    return any(re.match(pat, name.lower().strip()) for pat in SUBKEY_PATTERNS)

def to_env_name(section, name):
    parts = ([section] if section else []) + [name]
    combined = "_".join(parts).upper().replace(" ", "_").replace("-", "_")
    return re.sub(r"[^A-Z0-9_]", "", combined)

def parse_apis_file(path):
    result = {}
    current_section = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line.strip():
                current_section = None
                continue
            m = re.match(r'^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)', line)
            if not m:
                continue
            name, value = m.group(1).strip(), m.group(2).strip()
            if value:
                if is_subkey(name, current_section):
                    env_name = to_env_name(current_section, name)
                else:
                    current_section = None
                    env_name = to_env_name(None, name)
                result[env_name] = value
            else:
                current_section = name
    return result

def apply_aliases(parsed):
    """Replace raw names with standard env var names where known."""
    result = {}
    for k, v in parsed.items():
        # Use alias if one exists, otherwise keep original
        standard = ALIASES.get(k, k)
        result[standard] = v
    # Deduplicate — if both raw and alias pointed to same standard name, keep once
    return result

def write_env(env_vars, output_path=".env"):
    existing = {}
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    existing[k.strip()] = v.strip()
    existing.update(env_vars)
    with open(output_path, "w") as f:
        f.write("# Auto-generated from APIs.txt — do not commit this file\n\n")
        for k, v in sorted(existing.items()):
            f.write(f"{k}={v}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load API keys from APIs.txt into .env")
    parser.add_argument("--apis", default=DEFAULT_APIS_PATH)
    parser.add_argument("--env",  default=".env")
    args = parser.parse_args()

    if not os.path.exists(args.apis):
        print(f"APIs.txt not found at: {args.apis}")
        print("Pass correct path with: python load_keys.py --apis \"C:/path/to/APIs.txt\"")
        exit(1)

    parsed = parse_apis_file(args.apis)
    parsed = apply_aliases(parsed)
    write_env(parsed, args.env)

    print(f"Wrote {len(parsed)} keys to {os.path.abspath(args.env)}:")
    for k, v in sorted(parsed.items()):
        print(f"  {k:<30} = {v[:6]}{'*' * max(0, len(v)-6)}")
    print(f"\nDone. {args.env} will be read automatically by patent_lookup.py.")
