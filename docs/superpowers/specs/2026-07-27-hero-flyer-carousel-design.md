# Hero Flyer Carousel

## Problem

The homepage hero (`index.html` `#hero`) is a full-viewport photo background with a giant "B&G" watermark, an eyebrow line, an H1, a live countdown timer, and one outline-style ticket button. It doesn't showcase the actual event flyer, and the ticket CTA is visually small relative to how hard we want to push Aug 22 ticket sales.

We have two things to sell right now: the Aug 22 show and Season Passes. Both have (or will have) dedicated flyer artwork designed for Instagram.

## Goal

Replace the current text-and-photo hero with a 2-slide flyer carousel:

1. **Slide 1 (default, shown first): Aug 22 show flyer** — full flyer image + a large "Get Tickets" button
2. **Slide 2: Season Pass flyer** — full flyer image + a large "Get Tickets" button

Aug 22 is the priority sell, so it's the slide visitors land on. Nothing auto-advances away from it.

## Out of scope

- Countdown timer, "B&G" watermark lettering, eyebrow text, and current H1 copy are all removed from the hero, not repurposed.
- No changes to `seasonpass.html`'s own hero — that page keeps its existing `SEASONPASSHERO.jpg` background treatment.
- No CMS/build step — this stays hand-edited static HTML per the existing site stack.
- `og:image`, Twitter card image, and JSON-LD `image` fields keep pointing at `IMAGES/BUMPANDGRIND-HERO-TOP.jpg` for now — swapping social-share/schema imagery to a flyer is a separate decision TK hasn't made yet, not part of this change.

## Design

### Layout

- Hero section keeps roughly full-viewport presence but is restructured around the flyer image rather than a cropped photo background.
- Each flyer image is shown **in full** (no cropping) — `object-fit: contain`, centered, capped at a max-height (e.g. `78vh` desktop) so it never overflows the viewport, full-width on mobile.
- Background behind the letterboxed flyer uses the site's existing dark background color (`var(--dark)` or equivalent) rather than a busy image, so the flyer reads cleanly regardless of its exact aspect ratio.
- The "Get Tickets" button sits in its own row **below** the flyer image — not overlaid on top of the artwork, so flyer text/graphics are never obscured.
- Button style: new, visually bigger than the current `.btn-outline` (larger padding, larger font-size), high-contrast fill so it reads as the primary action.

### Carousel mechanics

- Exactly 2 slides: Aug 22 (index 0, default/active on load) and Season Pass (index 1).
- **No autoplay.** Rationale: autoplay risks rotating away from the priority Aug 22 CTA before a visitor acts on it.
- Controls: left/right arrow buttons + 2 dot indicators below the button row.
- Touch swipe support on mobile (drag left/right to switch slides).
- Keyboard support: left/right arrow keys move between slides when the carousel has focus, for accessibility.
- Switching slides swaps: the flyer `<img>` source/visibility, the button `href`, and the button label (both read "Get Tickets" but point at different URLs) and the active dot state.
- Implementation: vanilla JS (no external library), consistent with the site's existing no-build-step static stack.

### Content / links

| Slide       | Image                              | Button href                                                                                        |
| ----------- | ----------------------------------- | --------------------------------------------------------------------------------------------------- |
| Aug 22 show | `IMAGES/AUG22-HERO-FLYER.jpg`      | `https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee` |
| Season Pass | `IMAGES/SEASONPASS-HERO-FLYER.jpg` | `https://bump-grind-r-b-party.bloomtickets.ca/event/1878?B&G2026SeasonPass:All-Access`               |

### Image specs

Final assets delivered and in place at `IMAGES/AUG22-HERO-FLYER.jpg` and `IMAGES/SEASONPASS-HERO-FLYER.jpg` — both 1600×2000px (4:5), JPG, under 450KB each.

### Removed elements

- `.hero-bg-letters` ("B&G" watermark)
- `.hero-eyebrow` ("Bump & Grind · Est. 2016")
- `.hero-h1` ("Halifax's original & favourite R&B party.")
- `#heroCountdown` and its JS (`countdown` logic tied to `heroCtaPrimary` in the `<script>` block) — the countdown-driven CTA swap logic is superseded by the carousel's own slide-to-link mapping.
- `background: url('IMAGES/BUMPANDGRIND-HERO-TOP.jpg') ...` on `#hero`.

## Testing

- Manual verification in browser (dev server or direct file open): both slides render at correct aspect ratio, arrows/dots/swipe/keyboard all switch slides correctly, button hrefs match the table above, mobile viewport shows full-width flyer with no cropping.
- Confirm no leftover references to removed countdown/eyebrow/watermark elements elsewhere in the page (CSS or JS) after deletion.
- Run the site's standard pre-commit/pre-push audit (UX/conversion, performance, SEO/schema, roadmap) from `CLAUDE.md` before pushing, since this touches `og:image`/JSON-LD `image` references that currently point at `BUMPANDGRIND-HERO-TOP.jpg`.
