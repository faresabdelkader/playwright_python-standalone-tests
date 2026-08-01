"""
Central configuration for the QA Playground test framework.

This module is the single source of truth
for the target URL and the browser runtime defaults. Edit the values here to
change how the suite runs.
"""

# --- Application under test -------------------------------------------------
BASE_URL: str = "https://qaplayground.com/practice"

# --- Browser / runtime ------------------------------------------------------
# BROWSER_TYPE: "chromium" | "firefox" | "webkit"
BROWSER_TYPE: str = "chromium"
# HEADLESS: run without a visible browser window.
HEADLESS: bool = False
# SLOW_MO: milliseconds to pause between Playwright actions (0 = full speed).
SLOW_MO: int = 1000


