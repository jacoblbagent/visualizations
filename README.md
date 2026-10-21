# Visualizations

The hub for the interactive explainers. One card per visualization; every card
opens the live piece, and carries a localhost link and a source link.

**Live:** https://jacoblbagent.github.io/visualizations/
**Local:** http://localhost:5192/
**Repo:** https://github.com/jacoblbagent/visualizations

A single page, no build step, no dependencies. `index.html` plus two fonts and
four thumbnails is the whole thing.

## What's in it

| Card | Live | Local |
|---|---|---|
| The Energy Value Chain | [energy-infographic](https://jacoblbagent.github.io/energy-infographic/) | :5184 |
| How a VPN Works | [vpn-infographic](https://jacoblbagent.github.io/vpn-infographic/) | :5185 |
| How LLM tool calling works | [agent-tool-calling-viz](https://jacoblbagent.github.io/agent-tool-calling-viz/) | :5186 |
| Prompt → Response | [prompt-to-response-viz](https://jacoblbagent.github.io/prompt-to-response-viz/) | :5189 |

Each visualization also keeps its own project under `~/Code/` — that is where it
is edited. The hub only points at it; it holds no copies.

## Adding a new visualization

1. **Capture a thumbnail** at 1440×900 from the running piece, into
   `assets/thumbs/<slug>.png`:

   ```bash
   # with the visualization's own dev server up on <port>
   # headless Chromium at 1440x900, deviceScaleFactor 2, then downscale to 1440x900
   ```

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

## Design notes

Tokens at `:root` with a `prefers-color-scheme: dark` block; Instrument Sans
self-hosted from `assets/fonts/`; cards commit to a border rather than a border
plus a shadow; hover, focus-visible, selection and scrollbars are all themed.
Cards render in the markup, not from JS, so the page is complete with scripts
disabled — the only script sets the count chip.
