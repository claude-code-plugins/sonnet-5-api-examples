#!/usr/bin/env python3
"""Minimal Claude Sonnet 5 request with a cost estimate.

Model ID claude-sonnet-5 and the $2 / $10 per million token rates come
from the launch post. Adaptive thinking is on by default, so only text
blocks are printed here.

Usage: ANTHROPIC_API_KEY=... python3 examples/quickstart.py
"""
import os
import sys

import anthropic

MODEL = "claude-sonnet-5"
INPUT_USD_PER_MTOK = 2.0
OUTPUT_USD_PER_MTOK = 10.0


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "user", "content": "List three checks to run on an STL before slicing it."}
        ],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)

    u = response.usage
    estimate = (u.input_tokens * INPUT_USD_PER_MTOK + u.output_tokens * OUTPUT_USD_PER_MTOK) / 1_000_000
    print("---")
    print(f"model: {response.model}  stop_reason: {response.stop_reason}")
    print(f"input_tokens: {u.input_tokens}  output_tokens: {u.output_tokens}")
    print(f"estimated cost: ${estimate:.6f}  (check the pricing page for current rates)")


if __name__ == "__main__":
    main()
