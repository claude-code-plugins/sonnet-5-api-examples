#!/usr/bin/env python3
"""See one of the Sonnet 4.6 to Sonnet 5 behaviour changes in practice.

The platform docs say Sonnet 5 returns a 400 error when temperature,
top_p or top_k are set to non-default values, and when manual extended
thinking is requested. This script sends a request the old way with a
custom temperature, catches the 400, and retries without it.

Usage: ANTHROPIC_API_KEY=... python3 examples/migrate_from_4_6.py
"""
import os
import sys

import anthropic

MODEL = "claude-sonnet-5"
MESSAGES = [{"role": "user", "content": "Reply with the single word: ready"}]


def old_style_request(client):
    # Sonnet 4.6 code often pinned temperature for repeatability.
    return client.messages.create(
        model=MODEL,
        max_tokens=64,
        temperature=0.2,
        messages=MESSAGES,
    )


def new_style_request(client):
    # Sonnet 5: leave sampling parameters at their defaults.
    return client.messages.create(
        model=MODEL,
        max_tokens=64,
        messages=MESSAGES,
    )


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY in the environment first")
    client = anthropic.Anthropic()

    print("1. sending with temperature=0.2 (Sonnet 4.6 style)")
    try:
        response = old_style_request(client)
        print("   accepted (the docs say this should be a 400; check the docs page)")
    except anthropic.BadRequestError as e:
        print(f"   400 as documented: {e.message}")
        print("2. retrying without sampling parameters")
        response = new_style_request(client)

    text = "".join(b.text for b in response.content if b.type == "text")
    print(f"   response: {text.strip()}")


if __name__ == "__main__":
    main()
