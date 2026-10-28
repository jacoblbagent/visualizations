# Visualizations

The hub for the interactive explainers. One card per visualization; every card
opens the live piece, and carries a localhost link and a source link.

**Live:** https://jacoblbagent.github.io/visualizations/
**Local:** http://localhost:5192/
**Repo:** https://github.com/jacoblbagent/visualizations

A single page, no build step, no dependencies. `index.html` plus two fonts and
five thumbnails is the whole thing.

## What's in it

| Card | Live | Local |
|---|---|---|
| The Energy Value Chain | [energy-infographic](https://jacoblbagent.github.io/energy-infographic/) | :5184 |
| How a VPN Works | [vpn-infographic](https://jacoblbagent.github.io/vpn-infographic/) | :5185 |
| How LLM tool calling works | [agent-tool-calling-viz](https://jacoblbagent.github.io/agent-tool-calling-viz/) | :5186 |
| Prompt → Response | [prompt-to-response-viz](https://jacoblbagent.github.io/prompt-to-response-viz/) | :5189 |
| How a tailnet works | [tailnet-viz](https://jacoblbagent.github.io/tailnet-viz/) | :5193 |
| How models get tuned | [model-tuning-viz](https://jacoblbagent.github.io/model-tuning-viz/) | :5194 |
| Latent space of a small LLM | [latent-space-viz](https://jacoblbagent.github.io/latent-space-viz/) | :5205 |

Each visualization also keeps its own project under `~/Code/` — that is where it
is edited. The hub only points at it; it holds no copies.

Every piece is also registered in the **Hermes Web UI sidebar**, but not as a
project of its own: it is a **piece of the Visualizations row** (`children` in
`~/Code/hermes-web-ui/scripts/projects.json`), which the sidebar draws in a fold
under that one row — closed until its chevron is pressed, each piece with its own
start button and link glyphs. The hub is the list of the pieces; the sidebar is
where they are started.

## Adding a new visualization

1. **Capture a thumbnail** at 1440×900 into `assets/thumbs/<slug>.png` — real
   pixels from the running piece, never a mockup. With the visualization's own
   server up, screenshot it headlessly at 1440×900 with `deviceScaleFactor` 2
   (crisper hairlines) and downscale to 1440×900 before saving.

2. **Add a card.** Copy an existing `<article class="card">` block in
   `index.html` and change four things: the `<img src>` slug, the `<h2>` live
   link and its text, the one-line description, and the two links in
   `.links` (localhost port, source repo). The count chip in the header reads
   the number of cards from the DOM, so it never needs updating by hand.

3. **Deploy:** commit and push — GitHub Pages serves `main` at the repo root,
   so the push *is* the deploy:

   ```bash
   git add -A && git commit -m "viz: add <name>" && git push
   ```

Keep thumbnails at 16:10. The card crops with `object-fit: cover`, so anything
else loses its edges.

## Staying in sync

`tools/check_hub.py` compares the hub against what is actually on disk, and the
hub's start script runs it on every boot. It flags two things:

- a card that has gone stale — thumbnail missing or a different size than the
  card declares, localhost port no longer in `projects.json`, project directory
  or start script gone, no source repo link
- a project under `~/Code` with an `index.html` that has no card

```bash
python3 tools/check_hub.py     # exit 0 when the hub is sound and nothing is unflagged
```

When something new turns up, either add a card or record the decision in
`tools/hub-exclude.txt`, one project name per line. That file is the written
record of what is deliberately not in the hub, so a thing is never silently
forgotten or silently added. The checker only reports; it never edits the page.

## Design notes

Tokens at `:root` with a `prefers-color-scheme: dark` block; Instrument Sans
self-hosted from `assets/fonts/`; cards commit to a border rather than a border
plus a shadow; hover, focus-visible, selection and scrollbars are all themed.
Cards render in the markup, not from JS, so the page is complete with scripts
disabled — the only script sets the count chip.
