# Unified AI API Model Catalog — 300+ Models Behind One OpenAI-Compatible API

A **unified AI API** needs one place that answers "which model ids exist, what modality are they, and what unit do they
bill in?". This repository is that place: a machine-readable catalog of the models reachable through a single
OpenAI-compatible base URL, regenerated every day from the public pricing payload.

<!-- snapshot:date -->2026-09-18<!-- /snapshot:date -->

**Attributed entry points:** [Browse the model catalog](https://go.apimart.ai/k-fa6008) · [Current pricing](https://go.apimart.ai/k-c8e2c4) · [Get an API key](https://go.apimart.ai/k-3b545d)

## What the catalog contains

`data/models.json` — one record per model:

```json
{
  "id": "gpt-image-2.5-ext",
  "name": "gpt-image-2.5-ext",
  "alias": "gpt-image-2.5-ext",
  "specification": "image",
  "unit": "usd_per_image",
  "prices": {
    "flare@1K":    { "list": 0.010625, "effective": 0.0085 },
    "flare@2K":    { "list": 0.0175,   "effective": 0.014 },
    "flare@4K":    { "list": 0.02625,  "effective": 0.021 }
  }
}
```

| Field | Meaning |
| --- | --- |
| `id` | the string you pass as `model` in a request |
| `name` / `alias` | display name and route alias where the platform defines one |
| `specification` | `image`, `second` (video), `token` (text/multimodal), `times` (per call) |
| `unit` | `usd_per_image`, `usd_per_second`, `usd_per_million_tokens`, … |
| `prices` | price cells keyed by resolution, variant or token direction; `effective` applies the default group discount |

## Coverage

<!-- catalog:summary:start -->
| Modality | Models captured | Typical billing unit |
| --- | --- | --- |
| Image | 41 | per delivered image (by resolution) |
| Video | 49 | per second of output (by resolution) |
| Text / multimodal | 209 | per million tokens (input / cached / output) |
| Other (per call, per track) | 6 | fixed unit per call |
<!-- catalog:summary:end -->

Headline routes per modality (the full list, with every model id, is in [`CATALOG.md`](CATALOG.md)):

### Image models

<!-- catalog:image:start -->
| Model id | Route | Headline price | Billing unit |
| --- | --- | --- | --- |
| `gpt-image-2.5-ext` | image2.5 per-image route | $0.0085 | usd_per_image |
| `gemini-3-pro-image-preview` | Nano Banana Pro | $0.03 | usd_per_image |
| `gemini-3.1-flash-image-preview` | Nano Banana 2 | $0.015 | usd_per_image |
| `gemini-2.5-flash-image-preview` | Nano Banana | $0.0125 | usd_per_image |
| `grok-imagine-1.5-apimart` | Grok Image 1.5 | $0.015 | usd_per_image |
| `seedream-4-5` | Seedance 4.5 image route | $0.026 | usd_per_image |
<!-- catalog:image:end -->

### Video models

<!-- catalog:video:start -->
| Model id | Route | Headline price | Billing unit |
| --- | --- | --- | --- |
| `seedance-2.5` | Seedance 2.5 | $0.216 | usd_per_second |
| `seedance-2.0` | Seedance 2.0 | $0.142 | usd_per_second |
| `seedance-2.0-mini` | Seedance 2.0 mini | $0.0229 | usd_per_second |
| `kling-3.0-turbo` | Kling 3.0 Turbo | $0.1144 | usd_per_second |
<!-- catalog:video:end -->

### Text and multimodal models

<!-- catalog:token:start -->
| Model id | Route | Headline price | Billing unit |
| --- | --- | --- | --- |
| `gpt-5.5` | GPT-5.5 | $4.00 | usd_per_million_tokens |
| `gpt-5.5-pro` | GPT-5.5 Pro | $24.00 | usd_per_million_tokens |
| `claude-opus-5` | Claude Opus 5 | $4.00 | usd_per_million_tokens |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | $2.40 | usd_per_million_tokens |
| `deepseek-v4-pro` | DeepSeek V4 Pro | $1.03 | usd_per_million_tokens |
| `deepseek-v4-flash` | DeepSeek V4 Flash | $0.3429 | usd_per_million_tokens |
| `gpt-5-mini` | GPT-5 mini | $0.2 | usd_per_million_tokens |
<!-- catalog:token:end -->

## Query it without writing a client

```bash
python examples/lookup.py --spec image --sort price | head            # cheapest image routes first
python examples/lookup.py --grep nano-banana                          # every Nano Banana record
python examples/lookup.py --id gpt-image-2.5-ext                      # one record, pretty-printed
python examples/lookup.py --models                                     # just the model ids, for a dropdown or a test fixture
```

The lookup script reads the local JSON only — no network, no API key — so it is safe inside CI and inside an agent loop.

## Why a catalog instead of a models endpoint

- **Diffable.** `data/models.json` is committed, so a new model or a price move shows up as a git diff with a timestamp.
- **Guess-free.** Display names and model ids diverge (`Nano Banana Pro` vs `gemini-3-pro-image-preview`), and a catalog
  is where that mapping lives instead of in someone's notebook.
- **Budget-ready.** Every record carries its billing unit, so a cost model can pick the right formula before the first
  paid request.

## Freshness and provenance

| Item | Value |
| --- | --- |
| Source | `https://apimart.ai/en/pricing` (public page, no API key required) |
| Extractor | [`tools/catalog.py`](tools/catalog.py) — fetch, parse, write `data/models.json`, rebuild `CATALOG.md` and the tables above |
| Schedule | daily at 06:23 UTC via [`.github/workflows/refresh-catalog.yml`](.github/workflows/refresh-catalog.yml); commits only when something changed |
| Snapshot | <!-- snapshot:date -->2026-09-18<!-- /snapshot:date --> |

## FAQ

**What is a unified AI API?**
One base URL, one credential and one billing surface in front of many models. The unified part is the envelope and the
credential, not the models: each provider keeps its own parameters, limits and quirks.

**How do I know which models are available right now?**
Read `data/models.json` in this repository (or `CATALOG.md`) rather than trusting a model list from a blog post. The CI
refresh commits a diff whenever the catalog moves.

**Do model ids and display names match?**
Often not. Image models are the worst offenders: the display name may read `Nano Banana Pro` while the API expects
`gemini-3-pro-image-preview`. Both are in the record — use `id` in requests and `name` in documentation.

**Can I use this catalog to estimate cost?**
Yes, at the unit level: each record carries the billing unit and the price cells. Multiply by your volume (images,
seconds, tokens) and compare against a completed task's `cost` field for reconciliation.

## Related searches

- `unified ai api`
- `ai api model catalog`
- `one api key many models`
- `ai api aggregator`
- `llm api list`
- `image generation api pricing`
- `openai compatible api`

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Browse the model catalog | <https://go.apimart.ai/k-fa6008> | `apimart.ai/model` |
| Current pricing page | <https://go.apimart.ai/k-c8e2c4> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-3b545d> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

APIMart is the service whose public pricing page supplies this snapshot; the repository is published to document that
catalog, not to claim official status. Model names, prices and documentation belong to their respective owners, and
relayed routes are third-party relay endpoints rather than first-party vendor endpoints.

## Repository map

```text
README.md          catalog overview, coverage and schema
CATALOG.md         every model id as a readable table (regenerated in CI)
data/models.json   machine-readable catalog
tools/catalog.py   extractor + table builder
tools/check_links.py  attribution guard
examples/lookup.py    offline query helper
.github/workflows/    daily refresh + validation
```

## License

MIT — see [LICENSE](LICENSE).
