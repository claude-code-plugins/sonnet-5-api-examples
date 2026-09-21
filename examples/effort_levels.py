#!/usr/bin/env python3
"""Run one prompt on Claude Sonnet 5 at medium, high and xhigh effort.

The launch post compares Sonnet 5 at different effort levels and says
it is most cost-efficient at medium effort, with higher effort able to
match Opus 4.8 on some tasks. This prints output tokens and wall time
per level so you can see the trade-off on your own prompt.

Usage: ANTHROPIC_API_KEY=... python3 examples/effort_levels.py
"""
import os
import sys
import time

import anthropic

MODEL = "claude-sonnet-5"
LEVELS = ["medium", "high", "xhigh"]
PROMPT = (
    "You are given a folder of 40 SVG logos to turn into 3 mm thick STL plates. "
    "Write a short plan: what to check first, and in what order to do the work."
)


def run(client, effort):
    started = time.monotonic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        output_config={"effort": effort},
        messages=[{"role": "user", "content": PROMPT}],
    )
    seconds = time.monotonic() - started
    text = "".join(b.text for b in response.content if b.type == "text")
    return response.usage.output_tokens, seconds, text


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")
    client = anthropic.Anthropic()

    print(f"{'effort':8} {'out_tok':>8} {'seconds':>8}")
    for level in LEVELS:
        out_tokens, seconds, text = run(client, level)
        print(f"{level:8} {out_tokens:>8} {seconds:>8.1f}")
        print(f"    {text.strip()[:160]}")


if __name__ == "__main__":
    main()
