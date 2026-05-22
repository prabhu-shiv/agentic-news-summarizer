# agents/reporter.py

import json
import os
import subprocess
import tempfile
from datetime import datetime
import config


def generate_report(articles):
    """
    Takes a list of analyzed articles and produces a .docx report.
    Delegates document building to build_report.js via subprocess.
    Returns the output file path, or None on failure.
    """

    if not articles:
        print("[Reporter] No articles to report. Skipping.")
        return None

    # Ensure output directory exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Timestamped output filename
    timestamp   = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = os.path.join(config.OUTPUT_DIR, f"Intel_AI_News_{timestamp}.docx")

    # Absolute paths so subprocess finds them regardless of cwd
    script_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    js_script   = os.path.join(script_dir, "build_report.js")
    config_path = os.path.join(script_dir, "report_config.json")

    # Sanity checks
    if not os.path.exists(js_script):
        print(f"[Reporter] ERROR: build_report.js not found at {js_script}")
        return None
    if not os.path.exists(config_path):
        print(f"[Reporter] ERROR: report_config.json not found at {config_path}")
        return None

    # Write articles to a temp JSON file for Node.js to consume
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(articles, tmp, ensure_ascii=False, indent=2)
            tmp_path = tmp.name

        print(f"[Reporter] Generating report for {len(articles)} articles...")

        result = subprocess.run(
            ["node", js_script, tmp_path, output_path, config_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"[Reporter] Node.js error:\n{result.stderr}")
            return None

        if result.stdout:
            print(result.stdout.strip())

        return output_path

    except FileNotFoundError:
        print("[Reporter] ERROR: Node.js not found. Install it from https://nodejs.org")
        return None

    except Exception as e:
        print(f"[Reporter] Unexpected error: {e}")
        return None

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)