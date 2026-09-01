# Bump & Grind Homepage Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `index.html` into a leaner, type-led homepage — a giant Anton tagline hero with the current-event flyer beneath it, then Events → Mixes → Memories → About → Newsletter → Contact — keeping Bump & Grind's warm identity and every piece of existing plumbing.

**Architecture:** Single static `index.html`, no build step. One `<style>` block, one `<script>` block, both inline. Work top-to-bottom, one page region per task: replace that region's markup, swap its CSS rules, rewire or delete its JS, verify in a browser, commit. The page must render and all forms must work after every task.

**Tech Stack:** Hand-written HTML/CSS/vanilla JS. Google Fonts (add Anton). Meta Pixel + a Cloudflare Worker for CAPI. Cloudflare Workers for newsletter signup. web3forms for contact + song requests. Mixcloud iframe widget. GitHub Pages + Cloudflare proxy for hosting.

**Spec:** `docs/superpowers/specs/2026-09-01-homepage-redesign-design.md` — read it before starting. The "Resolved decisions" section is authoritative.

**Visual reference:** `docs/superpowers/plans/assets/2026-09-01-homepage-redesign/`
- `mockup-full-homepage.html` — the whole page, section order, spacing, the warm palette in use
- `mockup-hero-options.html` — Option A hero (chosen): lettering, then framed flyer card
- `mockup-hero-lettering.html` — the Anton tagline treatment (T2, chosen)

These mockups are the **styling target**. Their exact pixel values (font sizes, paddings, radii) are guidance, not law — match the *feel*. The acceptance test for each task is the verification steps in that task, not a diff against the mockup.

## Global Constraints

- **One file only:** all changes are in `index.html`. Do not touch `seasonpass.html`, `waitlist.html`, `sitemap.xml`, `robots.txt`, `404.html`, `CNAME`, `FAVICON.ico`, or the GSC verification file.
- **No build step, no dependencies, no framework.** No npm, no bundler. Plain `<script>`, no `type="module"`, no imports. Any new JS goes in the existing single `<script>` block at the end of `<body>`.
- **No new external requests** beyond what exists today (Google Fonts, Meta Pixel/`connect.facebook.net`, the two `*.okaytkokay.workers.dev` Workers, `api.web3forms.com`, `mixcloud.com` iframe, `thumbnailer.mixcloud.com` images). The Behold Instagram feed (`feeds.behold.so`) is being **removed** — one fewer request.
- **Preserve every tracking + form contract exactly** (see "Plumbing contracts to preserve" below). Element IDs listed there must survive verbatim because JS binds to them by `getElementById`.
- **Palette:** use only the existing `:root` custom properties — `--white #ffffff`, `--off-white #fdf8f7`, `--blush-light #fceee9`, `--blush #f0b3a0`, `--blush-deep #b8543a`, `--blush-deep-text #ac4c34`, `--light-gray #eee9e7`, `--mid-gray #6b6b6b`, `--dark #181412`. No new colours. One new font family only: **Anton**.
- **Exactly one `<h1>`** on the page: the hero tagline. Everything else stays `<h2>`/`<h3>`. (The page currently has no `<h1>` — this is a deliberate SEO fix.)
- **Keep valid** the two `<script type="application/ld+json">` blocks in `<head>` (`Event` array + `Organization`). If event copy/date/venue changes in the markup, mirror it in the `Event` JSON-LD.
- **Keep** all existing `<head>` content: `<title>`, meta description, OG/Twitter tags, `rel=canonical` (www), `facebook-domain-verification`, favicon link, Meta Pixel snippet.
- **Deploy = push to `main`** (GitHub Pages auto-builds); if it doesn't show, purge Cloudflare cache. Do NOT push until Task 12 passes and TK approves.
- Respect `prefers-reduced-motion` for any new animation (follow the existing `@media (prefers-reduced-motion: reduce)` block).

---

## Plumbing contracts to preserve

Copy these verbatim into the new markup. JS in the `<script>` block binds to them.

### Meta Pixel — ticket clicks (script lines ~1120–1138)
Handler selects **`document.querySelectorAll('a[href*="bloomtickets.ca"]')`** and on click fires `fbq('track','InitiateCheckout', {content_name}, {eventID})` plus a `navigator.sendBeacon` to `https://bumpandgrind-track.okaytkokay.workers.dev/`.
- **Every ticket link** (hero flyer link, hero "Get tickets" button, nav CTA, event-row ticket buttons) must be an `<a>` whose `href` contains `bloomtickets.ca`. If a real ticket URL for a future event is on a different host, widen the selector in the handler to `a[href*="bloomtickets.ca"], a[href*="showpass.com"]` — otherwise leave it.
- Keep the handler code unchanged.

### Newsletter form (script lines ~1140–1168)
Required IDs/attrs, unchanged: form `#newsletterForm`, email input `#newsletterEmail` (`type="email" required`), submit button `#newsletterBtn`, success `#newsletterSuccess`, error `#newsletterError`, and the hidden honeypot `<input type="text" name="website">` inside the form. POSTs JSON `{email, event_id, fbp, fbc}` to `https://bumpandgrind-subscribe.okaytkokay.workers.dev/`; on success hides the form, shows `#newsletterSuccess`, fires `fbq('track','Lead', {content_name:'Newsletter Signup'}, {eventID})`. Keep the handler unchanged.

### Contact form (script lines ~1170–1195)
Required IDs/attrs, unchanged: form `#contactForm` with `action="https://api.web3forms.com/submit" method="POST"`, inputs `#contactName` (`name="name"`), `#contactEmail` (`name="email"`), `#contactMessage` (`name="message"`), button `#contactBtn`, success `#contactSuccess`, error `#contactError`. Hidden inputs `access_key` = `b6fb76de-b533-4d31-98c4-b805f0e711e1` and `subject` = `New Inquiry — Bump & Grind Website`. Keep the handler unchanged.

### Song request form (script lines ~1197–1223)
Required IDs/attrs, unchanged: form `#requestsForm` with `action="https://api.web3forms.com/submit" method="POST"`, text input `#songRequestInput` (`name="song_request" required`), button `#requestsBtn`, success `#requestsSuccess`, error `#requestsError`. Hidden inputs `access_key` (same key), `subject` = `New Song Request — Bump & Grind Website`, and the hidden honeypot `<input type="text" name="website">`. Keep the handler unchanged. This form moves *into* the Mixes section (Task 6) but keeps all IDs.

### Keep as-is
- `getCookie(name)` helper (top of script).
- `.reveal` + IntersectionObserver reveal-on-scroll (script ~1225–1238). New sections may use `class="reveal"`; keep the `setTimeout(showAllReveals, 1200)` failsafe.
- `loadMix(card, url)` (script ~1240–1249) + `#mixPlayer` / `#mixFrame`. Mix cards call it via inline `onclick`.
- Burger menu IIFE (script ~1308–1320): binds `#navBurger`, `nav`, `.nav-links`. Keep markup hooks.

### Delete (JS + markup + CSS)
- Hero flyer carousel IIFE (script ~1322–1367) — hero becomes static.
- Gallery carousel IIFE (script ~1274–1306) — gallery becomes a static grid.
- Behold Instagram feed fetch (script ~1251–1272) and `#instagramGrid` markup + `.instagram-*` CSS.
- `#love-section` testimonials markup + `.love-*` CSS.
- Nav ticket-CTA milestones IIFE (script ~1369–1404) is **replaced** by the `NEXT_EVENT` config in Task 1 (it drives both the nav CTA and the hero countdown).

---

## File structure

Everything is `index.html`. Regions, in document order, with their current line ranges (approximate — re-check before editing):

| Region | Current lines | Task |
|---|---|---|
| `<head>` fonts link | ~96 | 1 |
| `<style>` `:root` + shared classes | ~99–314 | 1 |
| `<script>` new `NEXT_EVENT` config + countdown | end of script | 1, 3 |
| `<nav>` | ~703–725 | 2 |
| `#hero` + `.ticker-wrap` | ~727–803 | 3, 4 |
| `#about-section` | ~805–819 | 8 |
| `#events-section` | ~821–845 | 5 |
| `#mixes-section` (incl. `#requests`) | ~847–944 | 6 |
| `#gallery-section` (incl. Instagram) | ~946–1016 | 7 |
| `#love-section` | ~1018–1040 | 11 (delete) |
| `#newsletter-section` | ~1042–1075 | 9 |
| `#contact-section` | ~1077–1098 | 10 |
| `<footer>` | ~1100–1112 | 11 |
| `<script>` cleanup | ~1114–1405 | 12 |

**ID rename:** section wrappers currently use `#about-section`, `#events-section`, etc. as anchor targets. Standardize new nav anchors to `#events`, `#mixes`, `#memories`, `#about`. Keep the existing inner `#events` / `#mixes` / `#about` IDs where they already exist; add `id="memories"` to the gallery section. Update every in-page `href="#..."` to match (there are anchor links in the events footer note and the newsletter recap link too).

---

## Task 1: Foundation — Anton font, shared type/layout classes, `NEXT_EVENT` config

**Files:**
- Modify: `index.html` `<head>` fonts `<link>` (~96)
- Modify: `index.html` `<style>` — `:root` and the "SHARED" block (~99–314)
- Modify: `index.html` `<script>` — add config + helper near the top of the block (after `getCookie`)

**Interfaces:**
- Produces: CSS classes `.hero-giant`, `.eyebrow`, `.pill`, and a tightened `.section-shell` wrapper convention, used by Tasks 2–11.
- Produces: JS globals `NEXT_EVENT` (object) and `formatCountdown(ms)` (returns string), consumed by Task 3 (hero countdown) and Task 12 (nav CTA wiring).

- [ ] **Step 1: Add Anton to the Google Fonts link**

Change the `<link href="https://fonts.googleapis.com/css2?...">` to include Anton. Final value:

```html
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600;1,700&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Add the `--display-fat` token and shared classes**

In `:root`, add under the existing font vars:

```css
--display-fat: 'Anton', 'Bebas Neue', Impact, sans-serif;
```

In the `/* ── SHARED ── */` block, add:

```css
/* Big type-led hero headline */
.hero-giant {
  font-family: var(--display-fat);
  font-weight: 400;
  font-size: clamp(52px, 12vw, 132px);
  line-height: 0.88;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  color: var(--dark);
  margin: 0;
  text-wrap: balance;
}
/* Small uppercase kicker used above headings */
.eyebrow {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--blush-deep-text);
}
/* Pill — countdown / status chips */
.pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--sans);
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.05em;
  padding: 9px 15px;
  border-radius: 999px;
  border: 1px solid var(--light-gray);
  background: var(--white);
  color: var(--dark);
}
.pill b { color: var(--blush-deep-text); font-weight: 600; }
```

- [ ] **Step 3: Tighten the shared section rhythm**

The redesign wants more air and a consistent max-width. Leave per-section `#id { padding }` rules for later tasks, but add one shared helper and use it in Tasks 2–11:

```css
.shell { max-width: 1120px; margin: 0 auto; padding: clamp(64px, 10vw, 120px) clamp(20px, 5vw, 48px); }
```

- [ ] **Step 4: Add the `NEXT_EVENT` config + `formatCountdown` helper**

In the `<script>` block, immediately after the `getCookie` function, add:

```js
// Single source of truth for the next event — drives the hero countdown pill
// and the nav ticket CTA. Set `date` to null (or leave it in the past) when
// nothing is announced; the UI then shows "New dates soon".
var NEXT_EVENT = {
  name: 'R&B Patio Day Party',
  date: '2026-09-20T15:00:00-03:00',            // ISO 8601 with TZ, or null
  ticketUrl: 'https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee',
  venue: 'The Pint Patio'
};

function nextEventMs() {
  if (!NEXT_EVENT.date) return null;
  var t = new Date(NEXT_EVENT.date).getTime();
  return (isFinite(t) && t > Date.now()) ? t : null;
}

function formatCountdown(targetMs) {
  var diff = targetMs - Date.now();
  if (diff <= 0) return null;
  var d = Math.floor(diff / 86400000);
  var h = Math.floor((diff % 86400000) / 3600000);
  var m = Math.floor((diff % 3600000) / 60000);
  if (d > 0) return d + 'd ' + h + 'h';
  if (h > 0) return h + 'h ' + m + 'm';
  return m + 'm';
}
```

- [ ] **Step 5: Verify**

Open `index.html` in a browser (just double-click / `file://` is fine for layout; use a local static server — `python3 -m http.server` — for anything that fetches).
- DevTools → Network → filter "font": `Anton` woff2 loads (200).
- DevTools → Console: `NEXT_EVENT` and `formatCountdown(Date.now()+90000000)` are defined; the latter returns `"1d 1h"`.
- The page looks **unchanged** (new classes are not used yet).
- No new console errors.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Add Anton font, shared hero/pill classes, NEXT_EVENT config"
```

---

## Task 2: Nav

**Files:**
- Modify: `index.html` `<nav>` markup (~703–725)
- Modify: `index.html` `<style>` `/* ── NAV ── */` (~127–193) and the mobile nav rules (~649–697)

**Interfaces:**
- Consumes: nothing.
- Produces: anchor targets `#events`, `#mixes`, `#memories`, `#about`; ticket CTA `#navCta` (kept). Burger hooks `#navBurger`, `.nav-links` (kept).

- [ ] **Step 1: Replace the nav link list**

New link set (order): Events · Mixes · Memories · About, then the ticket CTA. Keep the wordmark `<a>` and its `.wordmark` shimmer, keep `#navBurger`, keep `.nav-social` (Instagram + Facebook — add TikTok if a handle is known; otherwise leave the two). Markup skeleton:

```html
<nav>
  <a href="#" class="wordmark">BUMP <span>&amp;</span> GRIND</a>
  <div class="nav-links">
    <a href="#events">Events</a>
    <a href="#mixes">Mixes</a>
    <a href="#memories">Memories</a>
    <a href="#about">About</a>
    <a href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee" class="nav-cta" id="navCta">Tickets</a>
  </div>
  <button class="nav-burger" id="navBurger" aria-label="Open menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
  <div class="nav-social"><!-- keep existing IG + FB anchors --></div>
</nav>
```

Note the wordmark loses the trailing `<span>R&amp;B PARTY</span>` — keep just "BUMP & GRIND" for a cleaner mark. `#navCta` text is now just "Tickets" (Task 12 wires it to `NEXT_EVENT`).

- [ ] **Step 2: Restyle the nav**

Target (see `mockup-full-homepage.html` `.nav`): height ~64px, `padding: 14px clamp(20px,5vw,48px)`, `background: rgba(253,248,247,0.9)` (`--off-white` at 90%), `backdrop-filter: blur(8px)`, 1px `--light-gray` bottom border. `.nav-links` gap ~24px, links `font-size: 11px`, `letter-spacing: 0.12em`, uppercase, `color: var(--dark)` at ~0.75 opacity, hover `--blush-deep`. `.nav-cta` keeps the filled `--blush-deep` pill style (reuse existing rule, just verify padding matches the lighter nav). Update the `#hero` top padding in Task 3 to match the new nav height.

- [ ] **Step 3: Verify**

- Desktop ≥1000px: nav shows all four links + Tickets button; sticky on scroll; blur visible over content.
- Mobile ≤768px: burger shows; tapping it opens the full-screen menu with the four links; tapping a link closes it and scrolls to the section; `Esc` closes it.
- Each nav link scrolls to the correct section (they exist as `#events`, `#mixes` today; `#memories` / `#about` land correctly after Tasks 7 / 8 — for now `#about` still resolves to the About block if you also add `id="about"` is already present at ~807; `#memories` will 404-scroll until Task 7, that's expected).
- Console clean.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Rebuild nav: Events / Mixes / Memories / About + Tickets, lighter bar"
```

---

## Task 3: Hero (Option A) — Anton tagline + framed flyer + countdown pill

**Files:**
- Modify: `index.html` `#hero` markup (~727–737)
- Modify: `index.html` `<style>` `/* ── HERO ── */` (~195–280)
- Modify: `index.html` `<script>` — remove hero carousel IIFE (~1322–1367); add countdown render
- Modify: `<head>` `Event` JSON-LD only if the hero event copy diverges from it

**Interfaces:**
- Consumes: `NEXT_EVENT`, `nextEventMs()`, `formatCountdown()` from Task 1; `.hero-giant`, `.eyebrow`, `.pill` from Task 1.
- Produces: `#countdownPill` element; ticket links carrying `bloomtickets.ca` in `href`.

- [ ] **Step 1: Replace the hero markup**

```html
<section id="hero">
  <div class="hero-inner">
    <p class="eyebrow">Halifax · R&amp;B · since 2016</p>
    <h1 class="hero-giant">Your<br>favourite<br>R&amp;B party</h1>
    <p class="hero-sub">Good music. Good people. No skips. The one the group chat already planned around.</p>

    <a class="hero-flyer" id="heroFlyer" href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee">
      <img src="IMAGES/SEP20-PATIO-PARTY-HERO-FLYER.jpg" width="1920" height="1080" fetchpriority="high" loading="eager"
           alt="Bump & Grind R&B Patio Day Party — Sunday September 20 at The Pint Patio, Halifax">
    </a>

    <div class="hero-actions">
      <a class="hero-ticket-btn" href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee">Get tickets</a>
      <span class="pill" id="countdownPill" hidden></span>
    </div>
  </div>
</section>
```

Both the flyer `<a>` and the button `<a>` have `bloomtickets.ca` in the href → the existing Pixel handler picks them up automatically.

- [ ] **Step 2: Replace the hero CSS**

Delete the carousel rules (`.hero-carousel`, `.hero-track`, `.hero-slide`, `.hero-slide-img`, `.hero-nav-zone`, `.hero-arrow`, and the absolute-positioned `.hero-ticket-btn` variant). Keep a restyled `.hero-ticket-btn` (now a normal inline button in `.hero-actions`, keep the `::after` shimmer + reduced-motion off-switch). New rules (match `mockup-hero-options.html` `.phone.a`):

```css
#hero { background: linear-gradient(180deg, var(--blush-light), var(--off-white)); padding-top: 64px; }
.hero-inner { max-width: 1120px; margin: 0 auto; padding: clamp(32px,7vw,72px) clamp(20px,5vw,48px) clamp(48px,8vw,88px); }
.hero-inner .eyebrow { display: block; margin-bottom: 18px; }
.hero-sub { font-family: var(--sans); font-weight: 300; font-size: clamp(15px,2.2vw,19px); line-height: 1.5; color: #555; max-width: 40ch; margin: 18px 0 0; }
.hero-flyer { display: block; margin: 26px 0 0; border-radius: 14px; overflow: hidden; border: 1px solid var(--light-gray); box-shadow: 0 14px 34px rgba(24,20,18,0.16); max-width: 760px; }
.hero-flyer img { display: block; width: 100%; height: auto; aspect-ratio: 16/9; object-fit: cover; }
.hero-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 14px; margin-top: 22px; }
.hero-ticket-btn { position: relative; overflow: hidden; display: inline-block; background: var(--blush-deep); border: 1.5px solid var(--blush-deep); color: var(--white); font-family: var(--sans); font-size: 12px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; text-decoration: none; padding: 14px 30px; border-radius: 999px; transition: background .25s, border-color .25s, color .25s; }
.hero-ticket-btn:hover { background: var(--blush); border-color: var(--blush); color: var(--dark); }
```

Keep the existing `.hero-ticket-btn::after` shimmer rule and its entry in `@media (prefers-reduced-motion: reduce)`.

- [ ] **Step 3: Render the countdown pill**

Add to the `<script>` block (after the reveal code is fine):

```js
(function renderCountdown() {
  var pill = document.getElementById('countdownPill');
  if (!pill) return;
  function paint() {
    var ms = nextEventMs();
    if (!ms) { pill.textContent = 'New dates soon'; pill.hidden = false; return; }
    var cd = formatCountdown(ms);
    if (!cd) { pill.textContent = 'New dates soon'; pill.hidden = false; return; }
    pill.innerHTML = 'Next: ' + NEXT_EVENT.name + ' · <b>' + cd + '</b>';
    pill.hidden = false;
  }
  paint();
  setInterval(paint, 60000);
})();
```

- [ ] **Step 4: Delete the hero carousel IIFE**

Remove the entire `// Hero flyer carousel` IIFE (~1322–1367). Grep to confirm no remaining reference to `heroCarousel`, `heroTrack`, `hero-slide`.

- [ ] **Step 5: Check the JSON-LD**

Open the `<head>` `Event` block. Confirm `name`, `startDate`, `location.name`, `location.address`, `offers`/ticket URL still match `NEXT_EVENT` and the flyer `alt`. If they differ, update the JSON-LD to match. Validate the JSON parses (paste into a JSON linter).

- [ ] **Step 6: Verify**

- One `<h1>` on the page (`document.querySelectorAll('h1').length === 1`), and it's the tagline.
- Hero shows: kicker, huge Anton three-line tagline, sub line, framed 16:9 flyer, "Get tickets" button, countdown pill reading `Next: R&B Patio Day Party · 12d 4h` (numbers depend on today).
- Set `NEXT_EVENT.date = null` in DevTools and re-run the `renderCountdown` IIFE (or edit + reload): pill reads "New dates soon". Put it back.
- Click the flyer and the "Get tickets" button → both navigate to the bloomtickets URL. In DevTools Network, a `sendBeacon` POST to `bumpandgrind-track.okaytkokay.workers.dev` fires on each click, and (with the Meta Pixel Helper extension or Events Manager Test Events) `InitiateCheckout` fires.
- Mobile ≤768px: tagline scales down (`clamp` floor 52px), flyer full-width, button + pill stack/wrap.
- Console clean; no `heroCarousel` errors.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "Rebuild hero: Anton tagline + framed event flyer + countdown pill"
```

---

## Task 4: Artist ticker — keep, quieted

**Files:**
- Modify: `index.html` `.ticker-wrap` markup (~739–803) — only if trimming
- Modify: `index.html` `<style>` `/* ── TICKER ── */` (~282–287)

**Interfaces:** none.

The scrolling R&B-artist ticker sits between hero and About. The spec doesn't remove it; keep it but make it quieter so it reads as texture, not decoration.

- [ ] **Step 1: Restyle**

```css
.ticker-wrap { background: var(--off-white); color: var(--blush-deep-text); border-top: 1px solid var(--light-gray); border-bottom: 1px solid var(--light-gray); overflow: hidden; padding: 12px 0; }
.ticker-inner span { font-family: var(--sans); font-weight: 500; font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; padding: 0 26px; white-space: nowrap; }
.ticker-inner span.dot { color: var(--blush); padding: 0 6px; }
```

Leave the marquee animation and its reduced-motion off-switch (~617) as-is.

- [ ] **Step 2: Verify**

- Ticker is now a thin hairline band, not a bold terracotta bar. Still scrolls; pauses on hover; static under reduced-motion.
- If TK decides during review it still competes with the hero, delete the `.ticker-wrap` markup block and its CSS entirely — no JS depends on it.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Quiet the artist ticker to a hairline band"
```

---

## Task 5: Events

**Files:**
- Modify: `index.html` `#events-section` markup (~821–845)
- Modify: `index.html` `<style>` `/* ── EVENTS ── */` (~333–378)
- Modify: `<head>` `Event` JSON-LD if event data changes

**Interfaces:**
- Consumes: `.eyebrow`, `.shell`.
- Produces: event-row ticket `<a>`s with `bloomtickets.ca` href (Pixel).

- [ ] **Step 1: Rebuild the markup**

Keep the outer `id="events"` for the nav anchor. Full-width rows; each row is a date block + title/meta + a ticket action. Skeleton:

```html
<section id="events">
  <div class="shell">
    <p class="eyebrow reveal">Upcoming</p>
    <h2 class="section-title reveal">Events</h2>

    <div class="ev-list">
      <a class="ev-row reveal" href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee">
        <span class="ev-date"><span class="ev-mon">Sep</span><span class="ev-day">20</span></span>
        <span class="ev-info">
          <span class="ev-name">R&amp;B Patio Day Party</span>
          <span class="ev-meta">The Pint Patio · 1575 Argyle St · 3–7pm</span>
        </span>
        <span class="ev-cta">Tickets</span>
      </a>

      <!-- Unannounced date: render as a non-link div with a muted "Soon" chip -->
      <div class="ev-row is-soon reveal">
        <span class="ev-date"><span class="ev-mon">Oct</span><span class="ev-day">—</span></span>
        <span class="ev-info">
          <span class="ev-name">Fall Night Event</span>
          <span class="ev-meta">Venue TBA · newsletter gets it first</span>
        </span>
        <span class="ev-cta soon">Soon</span>
      </div>
    </div>

    <p class="ev-note reveal">Tickets drop closer to each date. <a href="#newsletter">Get on the newsletter</a> for first access &amp; VIP pricing.</p>
  </div>
</section>
```

If there is genuinely only one upcoming date, ship just that one row — do not invent events. The "Soon" row is a template for when a second date exists but isn't on sale.

- [ ] **Step 2: Replace the CSS**

Delete `.event-card`, `.event-date-block`, `.event-month`, `.event-day`, `.event-name`, `.event-meta`, `.event-actions`, `.event-status*`, `.event-flag`, `.btn-ticket`, `.events-footer-note`. Add (match `mockup-full-homepage.html` `.evrow`):

```css
#events-section, #events { background: var(--white); }
.ev-list { margin-top: 8px; }
.ev-row { display: flex; align-items: center; gap: clamp(14px,3vw,28px); padding: 22px 0; border-top: 1px solid var(--light-gray); text-decoration: none; color: var(--dark); }
.ev-row:last-child { border-bottom: 1px solid var(--light-gray); }
.ev-date { flex: none; text-align: center; width: 64px; }
.ev-mon { display: block; font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--blush-deep-text); }
.ev-day { display: block; font-family: var(--display); font-size: 40px; line-height: 0.9; color: var(--dark); }
.ev-info { flex: 1; }
.ev-name { display: block; font-family: var(--serif); font-size: clamp(18px,2.6vw,24px); font-weight: 700; }
.ev-meta { display: block; font-family: var(--sans); font-weight: 300; font-size: 13px; color: var(--mid-gray); margin-top: 3px; }
.ev-cta { flex: none; font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; padding: 9px 16px; border-radius: 999px; background: var(--dark); color: var(--off-white); white-space: nowrap; }
a.ev-row:hover .ev-cta { background: var(--blush-deep); }
.ev-cta.soon { background: transparent; color: var(--mid-gray); border: 1px solid var(--light-gray); }
.ev-note { font-family: var(--sans); font-weight: 300; font-size: 13px; color: var(--mid-gray); margin-top: 28px; }
.ev-note a { color: var(--blush-deep); text-decoration: none; }
```

Add a mobile rule near the other `@media (max-width:768px)` entries: `.ev-day { font-size: 32px; }`.

- [ ] **Step 3: Sync JSON-LD**

Ensure the `<head>` `Event` array still reflects exactly the on-page upcoming event(s). Remove any past event objects. Validate JSON parses.

- [ ] **Step 4: Verify**

- Events section shows the upcoming row(s) with date block, name, venue/time, "Tickets" chip.
- Clicking a real event row navigates to the ticket URL; `InitiateCheckout` + the Worker beacon fire (Pixel Helper / Network).
- The `is-soon` row (if present) is not a link and shows a muted "Soon".
- `#events` is reachable from the nav.
- Mobile: rows stay readable, date block narrower.
- Rich Results Test (search.google.com/test/rich-results) on the local file's JSON-LD, or paste the JSON-LD into validator.schema.org — `Event` valid, no errors.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Rebuild Events as full-width rows with Soon state"
```

---

## Task 6: Mixes + folded-in Song Requests

**Files:**
- Modify: `index.html` `#mixes-section` markup (~847–944), including `#requests`
- Modify: `index.html` `<style>` `/* ── MIXES ── */` (~380–454) and `/* ── REQUESTS ── */` (~456–481)

**Interfaces:**
- Consumes: `.eyebrow`, `.shell`, `loadMix()` (kept).
- Produces: nothing new; preserves `#mixPlayer`, `#mixFrame`, `#requestsForm` + its IDs.

- [ ] **Step 1: Rebuild the Mixes markup as a row list of 3**

Keep `id="mixes"`. Keep each card's `onclick="loadMix(this, '<url>')"` and the three real Mixcloud URLs + `thumbnailer.mixcloud.com` cover images + alt text from the current markup. Skeleton per mix:

```html
<section id="mixes">
  <div class="shell">
    <p class="eyebrow reveal">Monthly Mixes</p>
    <h2 class="section-title reveal">Listen back.</h2>

    <div class="mix-list">
      <div class="mix-row reveal" onclick="loadMix(this, 'https://www.mixcloud.com/heyokaytk/bump-grind-rb-mix-august-2026-okay-tk-x-baby-yu-x-jester/')">
        <span class="mix-cov"><img src="https://thumbnailer.mixcloud.com/unsafe/640x640/extaudio/e/b/8/2/8108-4fe8-4228-92aa-c9e50d0e8896" alt="Cover art for the Bump & Grind R&B Mix, August 2026" loading="lazy" decoding="async"></span>
        <span class="mix-info">
          <span class="mix-t">August 2026 — Okay TK × Baby Yu × Jester</span>
          <span class="mix-m">Monthly R&amp;B set</span>
        </span>
        <span class="mix-play">Play</span>
      </div>
      <!-- July + June rows: same shape, existing URLs/covers -->
    </div>

    <div class="mixes-player reveal" id="mixPlayer" style="display:none;">
      <iframe id="mixFrame" height="60" allow="autoplay" title="Bump & Grind mix player"></iframe>
    </div>

    <a href="https://www.mixcloud.com/heyokaytk" target="_blank" rel="noopener" class="btn-mixcloud reveal"><!-- keep existing svg -->All mixes on Mixcloud</a>

    <!-- Song requests, folded in -->
    <form class="mix-request reveal" id="requestsForm" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="b6fb76de-b533-4d31-98c4-b805f0e711e1">
      <div style="position:absolute;left:-9999px" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
      <label for="songRequestInput" class="sr-only">Song title and artist</label>
      <input type="text" name="song_request" id="songRequestInput" placeholder="Request a song for the next mix" required autocomplete="off">
      <input type="hidden" name="subject" value="New Song Request — Bump & Grind Website">
      <button type="submit" id="requestsBtn">Send</button>
    </form>
    <div class="requests-success" id="requestsSuccess">Got it — thanks for the request!</div>
    <div class="requests-error" id="requestsError">Something went wrong. Email us at <a href="mailto:bumpandgrindhfx@gmail.com" style="color:#c0392b">bumpandgrindhfx@gmail.com</a>.</div>
  </div>
</section>
```

Drop the standalone `#requests` heading/sub/cassette SVG. `loadMix` still marks `.mix-card.active` — either add `mix-card` as a second class on `.mix-row` **or** change the two `.mix-card` selectors in `loadMix` to `.mix-row`. Prefer editing `loadMix` (2 selectors) for cleanliness; note it in the commit.

- [ ] **Step 2: Replace the CSS**

Delete the `.mixes-grid`, `.mix-card*`, `.mix-art*`, `.mix-badge`, `.mix-body`, `.mix-num`, `.mix-date`, `.mix-play-btn*` rules and the whole `/* ── REQUESTS ── */` block except keep `.requests-success` / `.requests-error` (restyle to match). Add row styles (match `mockup-full-homepage.html` `.mixrow`):

```css
#mixes-section, #mixes { background: var(--blush-light); }
.mix-list { margin-top: 8px; }
.mix-row { display: flex; align-items: center; gap: 14px; padding: 14px 0; border-top: 1px solid var(--blush); cursor: pointer; }
.mix-row:first-child { border-top: none; }
.mix-row.active .mix-t { color: var(--blush-deep-text); }
.mix-cov { flex: none; width: 54px; height: 54px; border-radius: 8px; overflow: hidden; position: relative; }
.mix-cov img { width: 100%; height: 100%; object-fit: cover; display: block; }
.mix-cov::after { content: "▶"; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 13px; text-shadow: 0 1px 4px rgba(0,0,0,.5); }
.mix-info { flex: 1; }
.mix-t { display: block; font-family: var(--sans); font-weight: 500; font-size: 13px; }
.mix-m { display: block; font-family: var(--sans); font-weight: 300; font-size: 12px; color: var(--mid-gray); }
.mix-play { flex: none; font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--blush-deep-text); }
.btn-mixcloud { margin-top: 22px; }           /* keep existing button rule; just spacing */
.mix-request { display: flex; max-width: 460px; margin: 40px 0 0; }
.mix-request input[type="text"] { flex: 1; background: var(--white); border: 1.5px solid var(--light-gray); border-right: none; color: var(--dark); font-family: var(--sans); font-size: 14px; padding: 14px 18px; outline: none; }
.mix-request input[type="text"]:focus { border-color: var(--blush-deep); }
.mix-request button { background: var(--blush-deep); border: none; color: var(--white); font-family: var(--sans); font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; padding: 14px 22px; cursor: pointer; white-space: nowrap; }
.mix-request button:disabled { opacity: 0.7; cursor: default; }
```

Add to the mobile media block: `.mix-request { flex-direction: column; } .mix-request input[type="text"] { border-right: 1.5px solid var(--light-gray); border-bottom: none; }`.

- [ ] **Step 3: Verify**

- Mixes shows 3 rows; clicking one sets `#mixPlayer` `display:block`, loads the Mixcloud iframe, scrolls it into view; the active row's title turns terracotta.
- "All mixes on Mixcloud" link works.
- Song request: type a song, Send → row hides, `#requestsSuccess` shows. (Use a throwaway value; it emails bumpandgrindhfx.) Network shows a 200 from `api.web3forms.com`.
- Honeypot still present and visually hidden.
- Console clean.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Rebuild Mixes as a 3-row list; fold Song Requests into an inline input"
```

---

## Task 7: Memories — static photo grid + vanilla lightbox

**Files:**
- Modify: `index.html` `#gallery-section` markup (~946–1016)
- Modify: `index.html` `<style>` `/* ── GALLERY ── */` (~483–504) and `/* ── INSTAGRAM ── */` (~516–536)
- Modify: `index.html` `<script>` — delete gallery carousel IIFE (~1274–1306) and Behold fetch (~1251–1272); add lightbox module

**Interfaces:**
- Consumes: `.eyebrow`, `.shell`.
- Produces: `id="memories"` anchor target.

- [ ] **Step 1: Rebuild the markup**

All 21 photos from `IMAGES/GALLERY/PHOTO-1.jpg … PHOTO-21.jpg` in one responsive grid. Reuse the existing descriptive `alt` text from the current markup (do not regress alt quality). Skeleton:

```html
<section id="memories">
  <div class="shell">
    <p class="eyebrow reveal">Memories</p>
    <h2 class="section-title reveal">Every one sold out.</h2>

    <div class="mem-grid reveal" id="memGrid">
      <button type="button" class="mem-cell" data-full="IMAGES/GALLERY/PHOTO-1.jpg" aria-label="Open photo 1">
        <img src="IMAGES/GALLERY/PHOTO-1.jpg" alt="Three friends posing indoors under blue and purple club lighting" loading="lazy" decoding="async">
      </button>
      <!-- PHOTO-2 … PHOTO-21, same shape -->
    </div>

    <a href="https://www.instagram.com/bumpandgrindhfx" target="_blank" rel="noopener" class="btn-instagram reveal"><!-- keep existing IG svg -->Follow on Instagram</a>
  </div>
</section>

<!-- Lightbox: one instance, appended just before </body> or kept here -->
<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" id="lbClose" aria-label="Close">&times;</button>
  <button class="lb-prev" id="lbPrev" aria-label="Previous photo">&#8249;</button>
  <img class="lb-img" id="lbImg" alt="">
  <button class="lb-next" id="lbNext" aria-label="Next photo">&#8250;</button>
</div>
```

- [ ] **Step 2: Replace the CSS**

Delete all `.gallery-*` and `.instagram-*` rules and the `.gallery-instagram-label` / `#gallery .section-header` rules. Keep `.btn-instagram` (restyle spacing only). Add:

```css
#gallery-section, #memories { background: var(--white); }
.mem-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 12px; }
.mem-cell { padding: 0; border: 0; background: var(--light-gray); border-radius: 6px; overflow: hidden; cursor: pointer; aspect-ratio: 1; }
.mem-cell img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .4s ease; }
.mem-cell:hover img { transform: scale(1.05); }
.mem-cell:focus-visible { outline: 2px solid var(--blush-deep); outline-offset: 2px; }
.btn-instagram { margin-top: 22px; }

.lightbox { position: fixed; inset: 0; z-index: 400; display: flex; align-items: center; justify-content: center; background: rgba(20,15,13,0.92); padding: 5vw; }
.lightbox[hidden] { display: none; }
.lb-img { max-width: 100%; max-height: 90vh; object-fit: contain; border-radius: 4px; }
.lb-close, .lb-prev, .lb-next { position: absolute; background: rgba(255,255,255,0.12); color: #fff; border: 0; cursor: pointer; width: 44px; height: 44px; border-radius: 50%; font-size: 22px; line-height: 1; display: flex; align-items: center; justify-content: center; }
.lb-close { top: 20px; right: 20px; }
.lb-prev { left: 16px; top: 50%; transform: translateY(-50%); }
.lb-next { right: 16px; top: 50%; transform: translateY(-50%); }
.lb-close:hover, .lb-prev:hover, .lb-next:hover { background: rgba(255,255,255,0.25); }
```

Add to the mobile media block: `.mem-grid { gap: 4px; } .lb-prev { left: 6px; } .lb-next { right: 6px; }`.

- [ ] **Step 3: Delete dead JS**

Remove the gallery carousel IIFE and the Behold `fetch('https://feeds.behold.so/...')` block entirely. Grep to confirm no remaining `galleryTrack`, `galleryCarousel`, `gallery-dot`, `instagramGrid`.

- [ ] **Step 4: Add the lightbox module**

Append to the `<script>` block:

```js
// Memories lightbox — no dependencies
(function lightbox() {
  var grid = document.getElementById('memGrid');
  var box = document.getElementById('lightbox');
  if (!grid || !box) return;
  var img = document.getElementById('lbImg');
  var cells = Array.prototype.slice.call(grid.querySelectorAll('.mem-cell'));
  var i = 0, lastFocus = null;

  function show(n) {
    i = (n + cells.length) % cells.length;
    var cell = cells[i];
    img.src = cell.getAttribute('data-full');
    img.alt = cell.querySelector('img').alt;
  }
  function open(n) {
    lastFocus = document.activeElement;
    show(n);
    box.hidden = false;
    document.body.style.overflow = 'hidden';
    document.getElementById('lbClose').focus();
  }
  function close() {
    box.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  grid.addEventListener('click', function (e) {
    var cell = e.target.closest('.mem-cell');
    if (cell) open(cells.indexOf(cell));
  });
  document.getElementById('lbClose').addEventListener('click', close);
  document.getElementById('lbPrev').addEventListener('click', function () { show(i - 1); });
  document.getElementById('lbNext').addEventListener('click', function () { show(i + 1); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
})();
```

- [ ] **Step 5: Verify**

- Memories shows a 3-col grid of all 21 photos; hover zoom; images lazy-load on scroll (Network).
- Click a photo → lightbox opens with that image; `←`/`→` and the on-screen arrows move through all 21 and wrap; `Esc`, the × button, and clicking the dark backdrop all close it; focus returns to the clicked thumbnail.
- Keyboard: Tab to a cell, Enter opens it (it's a `<button>`).
- Mobile: grid still 3-col with tighter gaps (or drop to 2-col if you prefer — adjust the media rule), lightbox arrows reachable.
- Console clean; no Behold/gallery errors; Network shows **no** request to `feeds.behold.so`.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Replace gallery carousel + Instagram feed with static Memories grid + lightbox"
```

---

## Task 8: About

**Files:**
- Modify: `index.html` `#about-section` markup (~805–819)
- Modify: `index.html` `<style>` `/* ── ABOUT ── */` (~316–331)

**Interfaces:** consumes `.eyebrow`, `.shell`.

- [ ] **Step 1: Simplify the markup**

One short paragraph, "since 2016" in the prose, no two-column grid, no pull-quote, no stats:

```html
<section id="about">
  <div class="shell about-shell">
    <p class="eyebrow reveal">About</p>
    <p class="about-body reveal">Bump &amp; Grind is Halifax's original R&amp;B party. Since 2016 we've been filling rooms — rooftop patios to the city's biggest stages — with the songs you forgot you loved. No skips, no filler, just a floor full of people who came to hear the same thing you did.</p>
  </div>
</section>
```

Keep `id="about"` (nav anchor). Drop `#about-section` wrapper or keep it as the styling hook — pick one and update the CSS selector to match.

- [ ] **Step 2: Replace the CSS**

Delete `#about { grid... }`, `.about-pull`. Keep a restyled `.about-body`:

```css
#about { background: var(--blush-light); }
.about-shell { max-width: 760px; }
.about-body { font-family: var(--serif); font-size: clamp(20px, 3vw, 30px); font-weight: 600; line-height: 1.4; color: var(--dark); margin-top: 14px; }
```

(Serif + large = editorial, ties to the section headings. If it reads too heavy, drop to `--sans` weight 300 at 18px.)

- [ ] **Step 3: Verify**

- About is a single centered/left column with one large paragraph; no empty pull-quote element in the DOM; no stats.
- `#about` reachable from nav.
- Mobile: text scales via `clamp`, comfortable measure.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Simplify About to a single paragraph; drop stats and pull-quote"
```

---

## Task 9: Newsletter — dark panel, plumbing untouched

**Files:**
- Modify: `index.html` `#newsletter-section` markup (~1042–1075)
- Modify: `index.html` `<style>` `/* ── NEWSLETTER ── */` (~538–562)

**Interfaces:** consumes `.eyebrow`; **must preserve** `#newsletterForm`, `#newsletterEmail`, `#newsletterBtn`, `#newsletterSuccess`, `#newsletterError`, honeypot.

- [ ] **Step 1: Restyle to a dark panel**

Keep the entire form markup (IDs, honeypot, labels) and the recap block. Change the wrapper copy/structure only. Skeleton:

```html
<section id="newsletter-section">
  <div class="shell news-shell">
    <p class="eyebrow">Newsletter</p>
    <h2 class="section-title">Never miss a date.</h2>
    <p class="newsletter-sub">Ticket links before they go public, mix drops, the occasional guest list. Free, weekly-ish, always worth opening.</p>
    <div class="newsletter-recap"><!-- keep existing recap list + link --></div>
    <form class="newsletter-form" id="newsletterForm"><!-- keep exact inputs/IDs/honeypot --></form>
    <div class="newsletter-success" id="newsletterSuccess">You're on the list. See you in your inbox.</div>
    <div class="newsletter-error" id="newsletterError">Something went wrong. Try again or email us directly.</div>
  </div>
</section>
```

- [ ] **Step 2: CSS**

```css
#newsletter-section { background: var(--dark); }
.news-shell { max-width: 640px; text-align: center; }
#newsletter-section .eyebrow { color: var(--blush); }
#newsletter-section .section-title { color: var(--off-white); }
.newsletter-sub { font-family: var(--sans); font-weight: 300; font-size: 15px; line-height: 1.6; color: rgba(253,248,247,0.8); margin: 8px auto 28px; max-width: 44ch; }
.newsletter-recap { max-width: 460px; margin: 0 auto 28px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 22px 26px; text-align: left; }
.newsletter-recap-label { font-family: var(--sans); font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--blush); margin-bottom: 10px; }
.newsletter-recap-list { list-style: none; padding: 0; margin: 0 0 14px; }
.newsletter-recap-list li { font-size: 13px; color: rgba(253,248,247,0.78); padding: 4px 0 4px 16px; position: relative; line-height: 1.5; }
.newsletter-recap-list li::before { content: "◆"; position: absolute; left: 0; top: 7px; font-size: 6px; color: var(--blush); }
.newsletter-recap-link { font-family: var(--sans); font-size: 11px; font-weight: 600; letter-spacing: 0.1em; color: var(--blush); text-decoration: none; }
.newsletter-form { display: flex; max-width: 460px; margin: 0 auto; }
.newsletter-form input[type="email"] { flex: 1; background: var(--off-white); border: 1.5px solid var(--off-white); border-right: none; color: var(--dark); font-family: var(--sans); font-size: 14px; padding: 15px 18px; outline: none; }
.newsletter-form button { background: var(--blush-deep); border: none; color: var(--white); font-family: var(--sans); font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; padding: 15px 24px; cursor: pointer; white-space: nowrap; }
.newsletter-form button:disabled { opacity: 0.7; cursor: default; }
.newsletter-success, .newsletter-error { display: none; max-width: 460px; margin: 14px auto 0; padding: 14px 18px; font-family: var(--sans); font-size: 13px; text-align: left; border: 1px solid; }
.newsletter-success { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.15); color: var(--off-white); }
.newsletter-error { background: rgba(192,57,43,0.14); border-color: rgba(192,57,43,0.4); color: #f2b8b0; }
```

Keep the mobile stacking rule for `.newsletter-form` (already in the media block; adjust the `border` reset colours to `--off-white`).

- [ ] **Step 3: Verify**

- Dark section; heading + recap + form legible; contrast OK (AA for body text on `--dark`).
- Submit a throwaway email → Network shows POST to `bumpandgrind-subscribe.okaytkokay.workers.dev`; on 200/201 the form hides and `#newsletterSuccess` shows; Pixel Helper shows `Lead`.
- Force an error (offline) → `#newsletterError` shows, button re-enables.
- Honeypot present, `left:-9999px`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Restyle Newsletter as a dark panel; plumbing unchanged"
```

---

## Task 10: Contact — slim form above the footer

**Files:**
- Modify: `index.html` `#contact-section` markup (~1077–1098)
- Modify: `index.html` `<style>` `/* ── CONTACT ── */` (~564–595)

**Interfaces:** **must preserve** `#contactForm` (+ `action`/`method`), `#contactName`, `#contactEmail`, `#contactMessage`, `#contactBtn`, `#contactSuccess`, `#contactError`, hidden `access_key` + `subject`.

- [ ] **Step 1: Trim the markup**

Keep every form field/ID/hidden input. Shorten the copy, drop the big section title in favour of a compact block:

```html
<section id="contact-section">
  <div class="shell contact-shell">
    <p class="eyebrow">Contact</p>
    <h2 class="contact-head">Bookings, press, partnerships.</h2>
    <form class="contact-form" id="contactForm" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="b6fb76de-b533-4d31-98c4-b805f0e711e1">
      <label for="contactName" class="sr-only">Your name</label>
      <input type="text" name="name" id="contactName" placeholder="Your name" autocomplete="name" required>
      <label for="contactEmail" class="sr-only">Email address</label>
      <input type="email" name="email" id="contactEmail" placeholder="Email address" autocomplete="email" required>
      <label for="contactMessage" class="sr-only">Your message</label>
      <textarea name="message" id="contactMessage" placeholder="Your message" required></textarea>
      <input type="hidden" name="subject" value="New Inquiry — Bump & Grind Website">
      <button type="submit" id="contactBtn">Send message</button>
    </form>
    <div class="contact-success" id="contactSuccess">Thanks — we'll get back to you soon.</div>
    <div class="contact-error" id="contactError">Something went wrong. Email us at <a href="mailto:bumpandgrindhfx@gmail.com" style="color:#c0392b">bumpandgrindhfx@gmail.com</a>.</div>
  </div>
</section>
```

- [ ] **Step 2: CSS** (keep it close to current, just lighter)

```css
#contact-section { background: var(--off-white); border-top: 1px solid var(--light-gray); }
.contact-shell { max-width: 520px; padding-top: clamp(48px,7vw,80px); padding-bottom: clamp(48px,7vw,80px); }
.contact-head { font-family: var(--serif); font-size: clamp(22px,3vw,30px); font-weight: 700; margin: 8px 0 20px; }
.contact-form { display: flex; flex-direction: column; max-width: 460px; }
.contact-form input, .contact-form textarea { background: var(--white); border: 1.5px solid var(--light-gray); border-bottom: none; color: var(--dark); font-family: var(--sans); font-size: 14px; padding: 15px 18px; outline: none; width: 100%; resize: none; }
.contact-form input:focus, .contact-form textarea:focus { border-color: var(--blush-deep); }
.contact-form textarea { height: 110px; border-bottom: 1.5px solid var(--light-gray); }
.contact-form button { background: var(--blush-deep); border: none; color: var(--white); font-family: var(--sans); font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; padding: 15px 22px; cursor: pointer; }
.contact-form button:disabled { opacity: 0.7; cursor: default; }
.contact-success, .contact-error { display: none; max-width: 460px; margin: 14px 0 0; padding: 14px 18px; font-family: var(--sans); font-size: 13px; border: 1px solid; }
.contact-success { background: var(--white); border-color: var(--blush); color: var(--dark); }
.contact-error { background: rgba(192,57,43,0.08); border-color: rgba(192,57,43,0.3); color: #c0392b; }
```

Drop `.contact-sub` and `.contact-fine-print` rules (markup for them is removed).

- [ ] **Step 3: Verify**

- Compact contact block sits directly above the footer.
- Submit throwaway values → Network 200 from `api.web3forms.com`; form hides; `#contactSuccess` shows.
- Required validation fires on empty submit.
- Mobile: inputs full-width, comfortable.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Slim down Contact form and move it directly above the footer"
```

---

## Task 11: Footer + delete Testimonials

**Files:**
- Modify: `index.html` `<footer>` markup (~1100–1112)
- Delete: `index.html` `#love-section` markup (~1018–1040)
- Modify: `index.html` `<style>` `/* ── FOOTER ── */` (~597–603) and delete `/* ── LOVE ── */` (~506–514)
- Modify: `index.html` `<style>` reduced-motion block — remove `.love-marquee` from the `animation: none` list (~617)

**Interfaces:** none.

- [ ] **Step 1: Delete the testimonials section**

Remove the entire `<div id="love-section"> … </div>` block. Remove `.love-marquee-wrap`, `.love-marquee`, `.love-card`, `.love-quote`, `.love-handle` CSS. In `@media (prefers-reduced-motion: reduce)`, change `.ticker-inner, .love-marquee { animation: none; }` to `.ticker-inner { animation: none; }`.

- [ ] **Step 2: Rebuild the footer**

```html
<footer>
  <a href="#" class="wordmark">BUMP &amp; GRIND</a>
  <p class="footer-copy">Halifax, NS · © 2026 Bump &amp; Grind</p>
  <div class="footer-social">
    <a href="https://www.instagram.com/bumpandgrindhfx" target="_blank" rel="noopener" aria-label="Instagram"><!-- keep svg --></a>
    <a href="https://www.facebook.com/bumpandgrindhfx" target="_blank" rel="noopener" aria-label="Facebook"><!-- keep svg --></a>
    <a href="https://www.mixcloud.com/heyokaytk" target="_blank" rel="noopener" aria-label="Mixcloud"><!-- reuse the .btn-mixcloud path svg --></a>
  </div>
</footer>
```

Add a TikTok anchor only if TK provides a handle; otherwise leave IG/FB/Mixcloud.

- [ ] **Step 3: CSS** — keep the existing footer rules; just confirm the copy line still centers (`.footer-copy` absolute-center rule) and add the Mixcloud `svg` sizing if needed (`.footer-social svg { width: 20px; height: 20px; fill: currentColor; }` already covers it).

- [ ] **Step 4: Verify**

- No testimonials section anywhere in the page or DOM.
- Footer shows wordmark, centered copy line, three social icons that link out.
- `grep -n "love-" index.html` returns nothing; `grep -n "love-section" index.html` returns nothing.
- Console clean.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Remove Testimonials section; rebuild footer with Mixcloud link"
```

---

## Task 12: Dead-code sweep, nav CTA wiring, full QA, pre-push audit

**Files:**
- Modify: `index.html` `<script>` (nav CTA IIFE ~1369–1404) and any leftover CSS/markup
- No push yet.

- [ ] **Step 1: Replace the nav-CTA milestones IIFE**

Delete the `// Nav ticket CTA — advances through each upcoming show` IIFE. Replace with one that reads `NEXT_EVENT`:

```js
// Nav ticket CTA — follows NEXT_EVENT
(function navCta() {
  var el = document.getElementById('navCta');
  if (!el) return;
  var ms = nextEventMs();
  if (ms && NEXT_EVENT.ticketUrl) {
    el.textContent = 'Tickets';
    el.href = NEXT_EVENT.ticketUrl;
  } else {
    el.textContent = 'See events';
    el.href = '#events';
  }
})();
```

If `NEXT_EVENT.ticketUrl` host is not `bloomtickets.ca`, also update the Pixel handler selector (see "Plumbing contracts").

- [ ] **Step 2: Grep for orphans**

Run each; every one should return **no matches** (or only the definitions you intend to keep):

```bash
grep -nE 'hero-carousel|hero-track|hero-slide|hero-nav-zone|hero-arrow' index.html
grep -nE 'gallery-carousel|gallery-track|gallery-page|gallery-grid|gallery-item|gallery-nav|gallery-arrow|gallery-dot|galleryTrack|galleryCarousel' index.html
grep -nE 'instagram-grid|instagram-item|instagram-loading|instagramGrid|behold\.so|gallery-instagram-label' index.html
grep -nE 'love-marquee|love-card|love-quote|love-handle|love-section' index.html
grep -nE 'event-card|event-date-block|event-status|event-flag|btn-ticket|events-footer-note' index.html
grep -nE 'mixes-grid|mix-card|mix-art|mix-badge|mix-num|mix-date|mix-play-btn|cassette' index.html
grep -nE 'about-pull|section-header-left|newsletter-recap' index.html   # newsletter-recap SHOULD still match — keep it
grep -nE 'seasonpass|waitlist|season-pass|Season Pass' index.html       # expect none
```

Delete any dead CSS rule or stray markup the greps surface. Keep `newsletter-recap`.

- [ ] **Step 3: Anchor-link audit**

`grep -nE 'href="#' index.html` — every in-page anchor must resolve to an existing `id`. Expected targets: `#events`, `#mixes`, `#memories`, `#about`, `#newsletter` (the events note links here — make sure the newsletter section carries `id="newsletter"` on the element the link should land on; add it if the wrapper only has `id="newsletter-section"`), `#newsletterEmail` (recap link), `#` (wordmarks). Fix mismatches.

- [ ] **Step 4: `<head>` + SEO pass**

- Exactly one `<h1>` (`document.querySelectorAll('h1').length` → `1`).
- Heading order sane: `h1` (hero) → `h2` per section, no skipped levels, no stray `h2` above the `h1`.
- `<title>`, meta description, canonical (`https://www.bumpandgrindhfx.com/`), OG/Twitter tags, `facebook-domain-verification`, favicon link — all still present and unchanged.
- Both JSON-LD blocks present; paste each into `validator.schema.org` → no errors; `Event` reflects only real upcoming date(s).
- Every `<img>` has meaningful `alt`; below-the-fold images use `loading="lazy"`; the hero flyer keeps `fetchpriority="high"` + `loading="eager"` + `width`/`height`.

- [ ] **Step 5: Behaviour pass** (local static server: `python3 -m http.server 8000`)

- Nav: sticky, blur, all links scroll correctly, `#navCta` points at the ticket URL, mobile burger opens/closes (tap + `Esc`).
- Hero: one `<h1>`, countdown pill ticks; temporarily set `NEXT_EVENT.date = null` → "New dates soon" + no ticket button behaviour still sane; restore.
- Events: ticket rows navigate out; `InitiateCheckout` + Worker beacon fire (Meta Pixel Helper / Events Manager Test Events + Network).
- Mixes: 3 rows, `loadMix` plays each in the iframe; active row highlights; song-request submits (throwaway) → success state; Network 200 from web3forms.
- Memories: 21 photos, lazy-load; lightbox open/prev/next/wrap/close (× , `Esc`, backdrop); focus returns to thumbnail; no `feeds.behold.so` request.
- Newsletter: throwaway submit → POST to subscribe Worker, success state, `Lead` fires; error path re-enables button.
- Contact: throwaway submit → POST to web3forms, success state; required validation works.
- Footer: social links open in new tabs.
- Reveal-on-scroll works and the 1200ms failsafe still un-hides anything missed.
- `prefers-reduced-motion: reduce` (DevTools rendering emulation): ticker + reveal + shimmer + lightbox transitions quiet down.
- Console clean on load and through every interaction.

- [ ] **Step 6: Responsive pass**

375px, 768px, 1024px, 1440px: no horizontal scroll; hero tagline never clips; event rows, mix rows, mem-grid, forms all reflow; nav collapses at ≤768px.

- [ ] **Step 7: Weight check**

`python3 -m http.server` + DevTools: total transferred on first load. The 21 gallery JPEGs are the risk — confirm they're all `loading="lazy"` so first paint doesn't pull all of them. If any single `IMAGES/GALLERY/*.jpg` is > ~500KB, note it for TK (separate optimization task, not this plan).

- [ ] **Step 8: Run the repo pre-push audit**

Follow the "Pre-Commit / Pre-Push Audit" in `CLAUDE.md` — act as Principal Web Developer + UX/UI + Technical SEO, audit the **full diff** (`git diff main...HEAD`) across the four pillars (UX/conversion, architecture/performance, SEO, roadmap). Produce the prioritized punch list. Present it to TK; don't self-fix beyond obvious mistakes.

- [ ] **Step 9: Commit**

```bash
git add index.html
git commit -m "Wire nav CTA to NEXT_EVENT; dead-code sweep; QA pass"
```

- [ ] **Step 10: Hand off for deploy**

Report to TK: summary of changes, the audit punch list, and screenshots at mobile + desktop. **Do not push.** Deploy (push to `main`, then purge Cloudflare cache if needed) happens only on TK's go-ahead.

---

## Self-review (completed by plan author)

**Spec coverage:**
- Tightened-warm palette / restraint → Tasks 1–11 (shared classes, per-section restyle).
- Anton oversized tagline hero (T2) → Task 3 (+ Task 1 font/class).
- Option A hero (lettering then framed flyer) → Task 3.
- Countdown pill + "New dates soon" fallback → Task 1 (`NEXT_EVENT`) + Task 3 (render).
- Nav = Events/Mixes/Memories/About → Task 2.
- Events full-width rows + "Soon" → Task 5.
- Mixes = 3 rows + "all mixes" + song requests folded in → Task 6.
- Memories = grid + vanilla lightbox + "Follow on Instagram" → Task 7.
- About = one paragraph, "since 2016", no stats, no testimonials → Task 8 (+ Task 11 removes testimonials).
- Newsletter = dark panel, Worker unchanged, CAPI dedup fields kept → Task 9.
- Contact = slim form kept → Task 10.
- Footer = wordmark + copy + socials (incl. Mixcloud) → Task 11.
- Remove from homepage: season pass, waitlist, hero carousel, gallery carousel, Instagram grid, testimonials, standalone song-requests section → Tasks 2/3/5/6/7/11 + Task 12 grep sweep.
- Untouched files (`seasonpass.html`, `waitlist.html`, sitemap, etc.) → Global Constraints.
- Plumbing unchanged: Meta Pixel + CAPI, JSON-LD, Worker newsletter, web3forms, SEO, GitHub Pages → "Plumbing contracts to preserve" + Tasks 3/5/6/9/10/12.
- Add Anton to existing font link → Task 1.
- One `<h1>` → Task 3 + Task 12 check.
- Testing/verification list → Task 12 mirrors the spec's 8 points.

**Placeholder scan:** No "TBD"/"TODO"/"handle edge cases". Styling values are given as concrete CSS with a stated "match the feel" tolerance; logic (countdown, lightbox, nav CTA, form handlers) is given as complete code.

**Type/name consistency:** `NEXT_EVENT`, `nextEventMs()`, `formatCountdown()` defined in Task 1, consumed with the same names in Tasks 3 and 12. `#countdownPill`, `#navCta`, `#memGrid`, `#lightbox`/`#lbImg`/`#lbClose`/`#lbPrev`/`#lbNext` defined in markup and referenced by the same IDs in JS. Preserved form IDs listed once in "Plumbing contracts" and reused verbatim in Tasks 6/9/10. `loadMix` selector change (`.mix-card` → `.mix-row`) is called out in Task 6 Step 1.
