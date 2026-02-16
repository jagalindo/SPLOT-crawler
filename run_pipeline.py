"""Unified pipeline to run all SPLOT crawler steps."""

import logging
import subprocess
import sys
from pathlib import Path

from config import BASE_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

STEPS = [
    {
        "name": "Download models",
        "command": [sys.executable, str(BASE_DIR / "1.download.py")],
    },
    {
        "name": "Convert models (SPLOT -> FAMA -> UVL)",
        "command": ["bash", str(BASE_DIR / "2.convert.sh")],
    },
    {
        "name": "Generate README summary",
        "command": ["bash", str(BASE_DIR / "3.summarize.sh")],
    },
    {
        "name": "Extract statistics",
        "command": [sys.executable, str(BASE_DIR / "4.get_statistics.py")],
    },
]


def run_step(step):
    """Run a single pipeline step, returning True on success."""
    logger.info("=== Step: %s ===", step["name"])
    result = subprocess.run(
        step["command"],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
    )

    if result.stdout:
        for line in result.stdout.strip().splitlines():
            logger.info("  %s", line)

    if result.returncode != 0:
        logger.error("Step '%s' failed (exit code %d)", step["name"], result.returncode)
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                logger.error("  %s", line)
        return False

    return True


def main():
    logger.info("Starting SPLOT crawler pipeline")
    failed = []

    for step in STEPS:
        if not run_step(step):
            failed.append(step["name"])
            logger.warning("Continuing to next step despite failure...")

    if failed:
        logger.error("Pipeline completed with failures: %s", ", ".join(failed))
        sys.exit(1)
    else:
        logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
