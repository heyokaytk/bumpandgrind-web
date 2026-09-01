# Bump & Grind Homepage Redesign — Design

**Date:** 2026-09-01
**Scope:** `index.html` only. No other pages, no plumbing changes.
**Status:** Approved direction, pending spec review.

---

## Goal

Rework the homepage into a leaner, type-led page inspired by the restraint of
`anafrornbexperience.com` (Love Me Jeje) — huge display lettering, generous
whitespace, full-width event rows, a photo gallery that carries the vibe — while
keeping Bump & Grind's existing warm blush/terracotta identity and every piece of
current plumbing.

Reference takeaways we are adopting: oversized hero type, minimal chrome, event
list as the spine, a "Memories" gallery, short About, social links in the footer.

Reference takeaways we are **not** adopting: purple palette, multi-city tour
layout, dark theme.

---

## Visual direction (locked via visual companion)

- **Palette:** "Tightened Warm" — the current tokens (`--off-white #fdf8f7`,
  `--blush #fceee9`, `--blush-deep #b8543a`, `--blush-deep-text #ac4c34`,
  `--dark #181412`, `--mid-gray #6b6b6b`), used with far more restraint and air.
  No new colours.
- **Hero lettering:** the **tagline** ("Your favourite R&B party" / "Good music.
  Good people. No skips.") set **huge** in **Anton** (new Google Font — add to the
  existing `fonts.googleapis.com` link). All-caps, `line-height` ~0.9, tight
  tracking, stacked across 3 lines.
- **Other display type:** keep **Bebas Neue** for the wordmark, nav, event date
  blocks, stat numbers. Keep **Cormorant Garamond** for section headings
  ("Events", "Listen back.", etc.). Keep **Outfit** for body/UI.
- **Hero layout (Option A):** lettering first, then the current-event flyer as a
  framed 16:9 image card directly beneath it, then a row with the "Get tickets"
  button + a compact countdown pill. The flyer is a link to the ticket URL. Flyer
  art stays undistorted and fully legible (no text overlaid on it).

---

## Page structure (top → bottom)

| # | Section | Notes |
|---|---------|-------|
| 1 | **Sticky nav** | Wordmark "BUMP & GRIND" (Bebas) left; anchor links Events · Mixes · Memories · About; keep the mobile burger. Keep a single ticket `nav-cta` button pointing at the current event. |
| 2 | **Hero** | Eyebrow "Halifax · R&B · since 2016" → giant Anton tagline → one supporting line → framed 16:9 event flyer (links to tickets) → "Get tickets" button + countdown pill. |
| 3 | **Events** | Section heading + full-width rows: date block (Bebas) / title / venue + time / ticket button. Upcoming dates only. Unannounced dates render as a muted "Soon" row. JSON-LD `Event` data re-emitted from the same source info. |
| 4 | **Mixes** | Blush panel. Heading + recent monthly mixes as rows (cover art, title, tags, duration, play). Keeps the existing mix player mechanism. Link out to Mixcloud/SoundCloud. **Song Requests folded in here** as one compact inline input (same web3forms POST as today), not its own section. |
| 5 | **Memories** | 3-column photo grid from `IMAGES/GALLERY/` (21 photos). "See the full gallery →". Replaces the current gallery carousel + Instagram grid. Lightbox optional (see Open questions). |
| 6 | **About** | Short paragraph + three small stats (e.g. Since 2016 / Nights / Sold out). No testimonials. |
| 7 | **Newsletter** | Dark panel. Email → existing Cloudflare Worker endpoint, unchanged (keeps `event_id` + `fbp`/`fbc` for Meta CAPI dedup). |
| 8 | **Contact** | Kept, but slimmed and restyled — compact block just above the footer (name / email / message, same web3forms POST). |
| 9 | **Footer** | Wordmark, "Halifax, NS · © 2026", social links (Instagram, TikTok, Facebook, Mixcloud). |

### Removed from the homepage
- Hero flyer **carousel** → single framed flyer image.
- **Season Pass** promo block and any nav/link to `seasonpass.html`.
- **Waitlist** callout and any nav/link to `waitlist.html`.
- **Testimonials** section ("What The People Are Saying / Our B&G Family").
- Standalone **Song Requests** section (folded into Mixes).
- Gallery **carousel** + **Instagram grid** (replaced by the static grid).

### Untouched
`seasonpass.html` and `waitlist.html` stay in the repo, live but unlinked.
`sitemap.xml`, `robots.txt`, `404.html`, `CNAME`, GSC verification file — no change.

---

## Plumbing — explicitly unchanged

- Single-file static `index.html`, no build step. GitHub Pages + Cloudflare
  DNS/proxy. Deploy = push to `main`; purge Cloudflare cache if it doesn't show.
- **Meta Pixel** `1478717332720361`: `PageView` on load; `InitiateCheckout` on
  every ticket-link click (incl. the `sendBeacon` → CAPI call); `Lead` on
  newsletter submit; `ViewContent` as currently fired. All handlers must survive
  the markup change — re-bind to the new elements.
- **JSON-LD**: `Event` array + `Organization` blocks kept and kept valid after the
  date/venue/copy for the current event moves into the new markup.
- **Newsletter**: on-page form still POSTs to the Cloudflare Worker (not Beehiiv
  directly); keep the CAPI dedup fields.
- **web3forms**: song-request and contact POSTs unchanged.
- **SEO**: `<title>`, meta description, OG/Twitter tags, `rel=canonical`
  (www) all preserved. Maintain one `<h1>` (the hero tagline) and a sane
  H2/H3 hierarchy. Keep `alt` text on all images.
- Fonts: add **Anton** to the existing Google Fonts `<link>`; keep the other three
  families.

---

## Testing / verification

1. Visual pass at mobile (~375px), tablet, desktop (≥1200px) widths.
2. Google Rich Results / schema validator on the page's JSON-LD — `Event` and
   `Organization` both valid.
3. Confirm in the browser + Meta Events Manager test tool that ticket clicks fire
   `InitiateCheckout` (and the CAPI beacon) and newsletter submit fires `Lead`.
4. Newsletter form still hits the Worker and shows success/error states.
5. Song-request and contact forms still POST and show success/error states.
6. Nav anchor links + mobile burger work; sticky nav doesn't overlap content.
7. Run the repo's Pre-Commit / Pre-Push Audit (four pillars in `CLAUDE.md`) on the
   final diff. Present findings as a punch list; TK decides fix-now vs. later.
8. Lighthouse sanity check — total image weight (gallery is the risk); lazy-load
   below-the-fold images.

---

## Open questions for spec review

1. **Contact**: slim form as specced, or cut to a single "bookings →
   bumpandgrindhfx@gmail.com" line in the footer?
2. **Memories**: click-to-enlarge lightbox, or plain grid linking out to
   Instagram?
3. **Mixes**: how many mixes shown on the homepage (3? 4?) before the "all mixes"
   link.
4. **Countdown**: hide the pill entirely once an event has passed and no next date
   is set, or show "New dates soon"?
5. **Stats in About**: are "50+ nights / 100% sold out" numbers accurate enough to
   print, or keep it to "Since 2016" only?
