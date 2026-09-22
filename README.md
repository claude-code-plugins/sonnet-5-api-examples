# Claude Sonnet 5 examples

*Unofficial community examples for Claude Sonnet 5. Not affiliated with Anthropic. All trademarks belong to their owners.*

Short Python scripts for calling Claude Sonnet 5 through the Anthropic Python SDK. The model ID `claude-sonnet-5`, the $2/$10 per million token pricing, the 1M context window, the 128k max output, the adaptive-thinking default and the three behaviour changes from Sonnet 4.6 all come from the launch post and the platform docs page for sonnet 5. Anything the sources do not state is marked illustrative in the code.

> Need image, video or audio generation next to the text model? [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=sonnet-5-api-examples&utm_content=readme-top&utm_term=tier-r).

## Files

| Path | What it shows |
| --- | --- |
| `examples/quickstart.py` | Minimal `messages.create` call to `claude-sonnet-5`, printing text blocks, usage, and a cost estimate at the $2/$10 rates. |
| `examples/effort_levels.py` | The same prompt at `medium`, `high` and `xhigh` effort, the range the launch charts cover, with output tokens per level. |
| `examples/migrate_from_4_6.py` | Sends a request the Sonnet 4.6 way (custom `temperature`), catches the 400 the docs say Sonnet 5 returns, and retries with the parameter removed. |

## Setup

```
pip install anthropic
export ANTHROPIC_API_KEY=YOUR_KEY_HERE
```

Every script reads `ANTHROPIC_API_KEY` from the environment. No script contains a key.

## quickstart.py

One request, one response. Sonnet 5 runs adaptive thinking by default, so `response.content` can contain a `thinking` block before the `text` block; the script prints only text. It then multiplies `usage.input_tokens` and `usage.output_tokens` by the $2 and $10 per-million rates from the announcement to print an estimate. Treat that as an estimate: the [pricing page](https://platform.claude.com/docs/en/about-claude/pricing) is the source of truth.

## effort_levels.py

The launch post's charts compare Sonnet 5 with Sonnet 4.6 and Opus 4.8 "at different effort levels" and say Sonnet 5 "provides substantially improved cost efficiency at medium effort; its higher-effort performance can match Opus 4.8 on some tasks". The script runs one prompt at `medium`, `high` and `xhigh` and prints output tokens and wall time per level, so you can find your own point on that curve.

## migrate_from_4_6.py

The docs call Sonnet 5 "a drop-in upgrade for Claude Sonnet 4.6 with three behavior changes": adaptive thinking on by default, manual extended thinking returning a 400, and non-default `temperature`, `top_p` or `top_k` returning a 400. This script deliberately sends `temperature=0.2`, catches `anthropic.BadRequestError`, prints the message, and retries without the parameter. Run it once against your own request builder to see which of your call sites still set sampling parameters. The docs also mention a new tokenizer, so re-check any token budgets you tuned on Sonnet 4.6.

## When to use Synexa instead

These scripts do text in, text out. If your product also has to produce an image, a video clip or an audio track, a Sonnet-class model does not do that, and wiring separate vendors for each media type is the part that eats the integration budget. [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=sonnet-5-api-examples&utm_content=readme-top&utm_term=tier-r): keep `claude-sonnet-5` for planning and text, and send the media step to one endpoint.


_Last reviewed: 2026-09-22_
