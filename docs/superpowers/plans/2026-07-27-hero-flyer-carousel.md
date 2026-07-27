# Hero Flyer Carousel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current photo/countdown hero on `index.html` with a 2-slide flyer carousel (Aug 22 show, then Season Pass) with a bigger ticket button per slide, so ticket sales get pushed harder.

**Architecture:** Single-file static site (`index.html`, no build step). All changes are inline `<style>` CSS, inline markup, and inline `<script>` JS in that one file. The carousel is a standard sliding-track pattern (flex track, `translateX` per slide) with vanilla-JS arrow/dot/swipe/keyboard controls — no external libraries.

**Tech Stack:** Plain HTML/CSS/vanilla JS. No frameworks, no build tooling, no test runner — this repo has none, so "testing" here means opening `index.html` directly in a browser and manually verifying behavior (matches this project's existing pattern for the burger-menu and countdown IIFEs already in the file).

## Global Constraints

- No autoplay — Aug 22 must stay the slide visitors land on and it must not auto-advance away. (spec: "Carousel mechanics")
- No external JS/CSS libraries — vanilla only, consistent with the existing no-build-step stack. (spec: "Implementation")
- `og:image`, Twitter card image, and JSON-LD `image` fields keep pointing at `IMAGES/BUMPANDGRIND-HERO-TOP.jpg` — do not touch those meta/schema tags. (spec: "Out of scope")
- Aug 22 button href: `https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee` (spec: "Content / links")
- Season Pass button href: `https://bump-grind-r-b-party.bloomtickets.ca/event/1878?B&amp;G2026SeasonPass:All-Access` — note the `&` in TK's supplied URL is HTML-escaped to `&amp;` because it sits inside an HTML attribute; the actual link destination is unchanged. (spec: "Content / links")
- Flyer assets already exist at `IMAGES/AUG22-HERO-FLYER.jpg` and `IMAGES/SEASONPASS-HERO-FLYER.jpg` (1600×2000px, JPG, under 450KB each) — do not re-export or rename them.
- Removed for good, not repurposed: `.hero-bg-letters` ("B&G" watermark), `.hero-eyebrow`, `.hero-h1`, `#heroCountdown` and its digit display, `.btn-outline`. (spec: "Removed elements")

---

### Task 1: Hero markup + carousel CSS

**Files:**
- Modify: `index.html` (CSS: lines 224–369, the `/* ── HERO ── */` block through `.btn-outline:hover`; also line 686 reduced-motion selector list; HTML: lines 796–828, the `<!-- HERO -->` section)

**Interfaces:**
- Produces: DOM elements `#heroCarousel`, `#heroTrack`, `.hero-slide` (×2), `#heroPrev`, `#heroNext`, `#heroDots` with `.hero-dot` (×2, each with `data-index`) — Task 3 (carousel JS) wires these up by these exact IDs/classes.
- Consumes: CSS custom properties already defined in `:root` (line 145) — `--white`, `--blush`, `--blush-deep`, `--dark`, `--sans`.

- [ ] **Step 1: Replace the hero CSS block**

Find the CSS block starting at `/* ── HERO ── */` (currently line 224) and ending at `.btn-outline:hover { ... }` (currently line 369, right before the `/* ── TICKER ── */` comment). Replace that entire block with:

```css
  /* ── HERO ── */
  #hero {
    width: 100%;
    background: var(--dark);
    padding: 132px 24px 56px;
    display: flex;
    justify-content: center;
  }
  .hero-carousel {
    position: relative;
    width: 100%;
    max-width: 560px;
    overflow: hidden;
  }
  .hero-track {
    display: flex;
    transition: transform 0.45s ease;
  }
  .hero-slide {
    flex: 0 0 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 28px;
  }
  .hero-slide-img {
    display: block;
    width: 100%;
    max-height: 72vh;
    object-fit: contain;
    box-shadow: 0 24px 60px rgba(0,0,0,0.45);
  }
  .hero-ticket-btn {
    display: inline-block;
    background: var(--blush-deep);
    border: 1.5px solid var(--blush-deep);
    color: var(--white);
    font-family: var(--sans);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    text-decoration: none;
    padding: 22px 64px;
    transition: background 0.25s, border-color 0.25s, transform 0.2s;
  }
  .hero-ticket-btn:hover { background: var(--blush); border-color: var(--blush); color: var(--dark); transform: translateY(-1px); }
  .hero-nav-zone {
    position: absolute;
    inset: 0 0 130px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px;
    pointer-events: none;
  }
  .hero-arrow {
    pointer-events: auto;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.15);
    color: var(--white);
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }
  .hero-arrow:hover { background: rgba(255,255,255,0.3); }
  .hero-dots {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 24px;
  }
  .hero-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.35);
    padding: 0;
    cursor: pointer;
    transition: background 0.2s;
  }
  .hero-dot.active { background: var(--blush); }
```

Notes on the values above:
- `.hero-nav-zone` reserves 130px at the bottom (button + gap + dots row) so the arrows vertically center on the *image*, not on the whole slide including the button — this stays correct regardless of exact image aspect ratio.
- `.hero-carousel` caps at `max-width: 560px` so the portrait flyer reads as a poster-sized focal image rather than stretching edge-to-edge on wide desktop screens.

- [ ] **Step 2: Update the reduced-motion selector list**

Find this line (currently line 686):

```css
    .hero-eyebrow, .hero-h1, .hero-cta-row { animation: none; }
```

Delete it entirely — none of those classes exist anymore after Step 1, and the new hero has no load-in animation to suppress.

- [ ] **Step 3: Replace the hero HTML section**

Find the `<!-- HERO -->` section (currently lines 796–828):

```html
<!-- HERO -->
<section id="hero">
  <p class="hero-bg-letters" aria-hidden="true">B&amp;G</p>
  <p class="hero-eyebrow">Bump &amp; Grind · Est. 2016</p>
  <h1 class="hero-h1">Halifax's original &amp; favourite R&amp;B party.</h1>
  <div class="hero-countdown" id="heroCountdown" aria-label="Countdown to the next Bump & Grind show">
    <p class="hero-countdown-label">Next Patio Party In</p>
    <div class="hero-countdown-units">
      <div class="countdown-unit">
        <span class="countdown-num" id="cdDays">00</span>
        <span class="countdown-unit-label">Days</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdHours">00</span>
        <span class="countdown-unit-label">Hours</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdMinutes">00</span>
        <span class="countdown-unit-label">Minutes</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdSeconds">00</span>
        <span class="countdown-unit-label">Seconds</span>
      </div>
    </div>
  </div>
  <div class="hero-cta-row">
    <a href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee" class="btn-outline" id="heroCtaPrimary">R&amp;B At The Marquee Tickets</a>
  </div>
</section>
```

Replace it with:

```html
<!-- HERO -->
<section id="hero">
  <div class="hero-carousel" id="heroCarousel" tabindex="0" aria-roledescription="carousel" aria-label="Bump & Grind tickets">
    <div class="hero-track" id="heroTrack">
      <div class="hero-slide">
        <img class="hero-slide-img" src="IMAGES/AUG22-HERO-FLYER.jpg" alt="Bump & Grind presents R&B At The Marquee, Saturday August 22nd" loading="eager">
        <a href="https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee" class="hero-ticket-btn">Get Tickets</a>
      </div>
      <div class="hero-slide">
        <img class="hero-slide-img" src="IMAGES/SEASONPASS-HERO-FLYER.jpg" alt="Bump & Grind Season Passes — one pass, all shows" loading="lazy">
        <a href="https://bump-grind-r-b-party.bloomtickets.ca/event/1878?B&amp;G2026SeasonPass:All-Access" class="hero-ticket-btn">Get Tickets</a>
      </div>
    </div>
    <div class="hero-nav-zone">
      <button type="button" class="hero-arrow hero-arrow-prev" id="heroPrev" aria-label="Previous slide">&#10094;</button>
      <button type="button" class="hero-arrow hero-arrow-next" id="heroNext" aria-label="Next slide">&#10095;</button>
    </div>
    <div class="hero-dots" id="heroDots">
      <button type="button" class="hero-dot active" data-index="0" aria-label="Show Aug 22 show tickets" aria-selected="true"></button>
      <button type="button" class="hero-dot" data-index="1" aria-label="Show Season Pass tickets" aria-selected="false"></button>
    </div>
  </div>
</section>
```

- [ ] **Step 4: Verify in browser**

Open `index.html` directly in a browser (double-click it or `open index.html` on macOS). Confirm:
- The Aug 22 flyer displays in full (not cropped), centered, on a dark background.
- A pink/blush "GET TICKETS" button sits below the flyer, clearly larger than other buttons on the page.
- Two dots appear below the button, first one highlighted.
- Left/right arrow buttons appear on the flyer image (clicking them won't do anything yet — that's Task 3).
- No layout is broken elsewhere on the page (scroll down and check the artist ticker, events section, etc. still look normal).
- Open the browser console — you'll see a JS error referencing `heroCountdown` or `querySelector of null`. That's expected here; Task 2 fixes it.

- [ ] **Step 5: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Replace hero with flyer carousel markup and styles"
```

---

### Task 2: Fix the nav ticket button's countdown script

**Files:**
- Modify: `index.html` (the `<script>` block containing `// Hero countdown — advances through each upcoming show in order`, currently starting around line 1408 — search for that comment text since Task 1 shifted line numbers)

**Interfaces:**
- Consumes: `#navCta` (the nav bar's ticket link, defined in the `<nav>` markup — unaffected by Task 1, still present).
- Produces: nothing new consumed by later tasks — this is a self-contained bugfix for breakage Task 1 introduced (the nav bar's ticket button auto-updates its text/link as show dates pass; the old script also tried to update the now-deleted hero countdown digits and threw on load, which stopped it from ever reaching the `navCta` update).

- [ ] **Step 1: Replace the countdown script**

Find this IIFE (the comment text is the reliable anchor — search for `// Hero countdown`):

```javascript
  // Hero countdown — advances through each upcoming show in order
  (function() {
    var MARQUEE_URL = 'https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee';
    var EVENTS_URL = '#events-section';
    var milestones = [
      { date: new Date('2026-07-26T15:00:00-03:00').getTime(), label: 'Next Patio Party In', doneMsg: 'See You On The Patio! 🎉', ctaText: 'R&B At The Marquee Tickets', ctaHref: MARQUEE_URL },
      { date: new Date('2026-08-22T21:00:00-03:00').getTime(), label: 'R&B At The Marquee In', doneMsg: 'See You At The Marquee! 🎉', ctaText: 'R&B At The Marquee Tickets', ctaHref: MARQUEE_URL },
      { date: new Date('2026-08-23T15:00:00-03:00').getTime(), label: 'Next Patio Party In', doneMsg: 'See You On The Patio! 🎉', ctaText: 'See Upcoming Events', ctaHref: EVENTS_URL },
      { date: new Date('2026-09-20T15:00:00-03:00').getTime(), label: 'Next Patio Party In', doneMsg: 'See You On The Patio! 🎉', ctaText: 'See Upcoming Events', ctaHref: EVENTS_URL }
    ];

    var container = document.getElementById('heroCountdown');
    var labelEl = container.querySelector('.hero-countdown-label');
    var navCta = document.getElementById('navCta');
    var heroCta = document.getElementById('heroCtaPrimary');
    var els = {
      days: document.getElementById('cdDays'),
      hours: document.getElementById('cdHours'),
      minutes: document.getElementById('cdMinutes'),
      seconds: document.getElementById('cdSeconds')
    };

    function getCountdownParts(targetMs, nowMs) {
      var diff = targetMs - nowMs;
      if (diff <= 0) return null;
      var days = Math.floor(diff / (1000 * 60 * 60 * 24));
      var hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      var minutes = Math.floor((diff / (1000 * 60)) % 60);
      var seconds = Math.floor((diff / 1000) % 60);
      return { days: days, hours: hours, minutes: minutes, seconds: seconds };
    }

    function pad(n) {
      return String(n).padStart(2, '0');
    }

    function setCta(text, href) {
      if (navCta) { navCta.textContent = text; navCta.href = href; }
      if (heroCta) { heroCta.textContent = text; heroCta.href = href; }
    }

    var activeIndex = -1;
    var timer;
    function tick() {
      var now = Date.now();
      var index = milestones.findIndex(function(m) { return m.date > now; });

      if (index === -1) {
        clearInterval(timer);
        container.innerHTML = '<p class="hero-countdown-message">' + milestones[milestones.length - 1].doneMsg + '</p>';
        setCta('See Upcoming Events', EVENTS_URL);
        return false;
      }

      if (index !== activeIndex) {
        activeIndex = index;
        labelEl.textContent = milestones[index].label;
        setCta(milestones[index].ctaText, milestones[index].ctaHref);
      }

      var parts = getCountdownParts(milestones[index].date, now);
      els.days.textContent = pad(parts.days);
      els.hours.textContent = pad(parts.hours);
      els.minutes.textContent = pad(parts.minutes);
      els.seconds.textContent = pad(parts.seconds);
      return true;
    }

    if (tick()) {
      timer = setInterval(tick, 1000);
    }
  })();
```

Replace it with:

```javascript
  // Nav ticket CTA — advances through each upcoming show in order
  (function() {
    var MARQUEE_URL = 'https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee';
    var EVENTS_URL = '#events-section';
    var milestones = [
      { date: new Date('2026-07-26T15:00:00-03:00').getTime(), ctaText: 'R&B At The Marquee Tickets', ctaHref: MARQUEE_URL },
      { date: new Date('2026-08-22T21:00:00-03:00').getTime(), ctaText: 'R&B At The Marquee Tickets', ctaHref: MARQUEE_URL },
      { date: new Date('2026-08-23T15:00:00-03:00').getTime(), ctaText: 'See Upcoming Events', ctaHref: EVENTS_URL },
      { date: new Date('2026-09-20T15:00:00-03:00').getTime(), ctaText: 'See Upcoming Events', ctaHref: EVENTS_URL }
    ];

    var navCta = document.getElementById('navCta');
    function setCta(text, href) {
      if (navCta) { navCta.textContent = text; navCta.href = href; }
    }

    var activeIndex = -1;
    function tick() {
      var now = Date.now();
      var index = milestones.findIndex(function(m) { return m.date > now; });

      if (index === -1) {
        setCta('See Upcoming Events', EVENTS_URL);
        return false;
      }

      if (index !== activeIndex) {
        activeIndex = index;
        setCta(milestones[index].ctaText, milestones[index].ctaHref);
      }
      return true;
    }

    if (tick()) {
      setInterval(tick, 60000);
    }
  })();
```

(The interval dropped from every 1 second to every 60 seconds — the only thing this script drives now is the nav button's text/link, which only changes at the four milestone date boundaries, not every second. No visible behavior change, just less pointless work.)

- [ ] **Step 2: Verify in browser**

Reload `index.html` in the browser. Confirm:
- No console errors on page load.
- Nav bar's ticket button (top right, "R&B At The Marquee Tickets") still shows correctly and links to the Marquee event.

- [ ] **Step 3: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Decouple nav CTA countdown script from removed hero elements"
```

---

### Task 3: Carousel interactivity (arrows, dots, swipe, keyboard)

**Files:**
- Modify: `index.html` (add a new `<script>` IIFE; insert it right after the burger-menu IIFE, which ends with `})();` right before the `// Nav ticket CTA` comment added in Task 2 — search for that comment text as the anchor)

**Interfaces:**
- Consumes: `#heroCarousel`, `#heroTrack`, `.hero-slide`, `#heroPrev`, `#heroNext`, `#heroDots .hero-dot`, `data-index` attributes — all produced by Task 1.

- [ ] **Step 1: Add the carousel script**

Insert this new IIFE immediately before the `// Nav ticket CTA` comment (added in Task 2):

```javascript
  // Hero flyer carousel
  (function() {
    var carousel = document.getElementById('heroCarousel');
    var track = document.getElementById('heroTrack');
    var slides = track.querySelectorAll('.hero-slide');
    var dots = document.querySelectorAll('#heroDots .hero-dot');
    var prevBtn = document.getElementById('heroPrev');
    var nextBtn = document.getElementById('heroNext');
    var index = 0;

    function goTo(newIndex) {
      index = (newIndex + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (index * 100) + '%)';
      dots.forEach(function(dot, i) {
        var active = i === index;
        dot.classList.toggle('active', active);
        dot.setAttribute('aria-selected', active ? 'true' : 'false');
      });
    }

    prevBtn.addEventListener('click', function() { goTo(index - 1); });
    nextBtn.addEventListener('click', function() { goTo(index + 1); });
    dots.forEach(function(dot) {
      dot.addEventListener('click', function() { goTo(parseInt(dot.dataset.index, 10)); });
    });

    carousel.addEventListener('keydown', function(event) {
      if (event.key === 'ArrowLeft') goTo(index - 1);
      if (event.key === 'ArrowRight') goTo(index + 1);
    });

    var touchStartX = null;
    carousel.addEventListener('touchstart', function(event) {
      touchStartX = event.touches[0].clientX;
    }, { passive: true });
    carousel.addEventListener('touchend', function(event) {
      if (touchStartX === null) return;
      var deltaX = event.changedTouches[0].clientX - touchStartX;
      if (deltaX > 40) goTo(index - 1);
      if (deltaX < -40) goTo(index + 1);
      touchStartX = null;
    });
  })();

```

- [ ] **Step 2: Verify in browser — desktop**

Reload `index.html`. Confirm:
- Clicking the right arrow slides to the Season Pass flyer; its button links to the Season Pass Bloom event; the second dot becomes active.
- Clicking the left arrow (or clicking directly on the first dot) slides back to the Aug 22 flyer.
- Clicking on the carousel image area to focus it, then pressing the keyboard left/right arrow keys, also switches slides.
- No autoplay — leave the page open for ~15 seconds and confirm the slide does not change on its own.

- [ ] **Step 3: Verify in browser — mobile viewport**

Using browser dev tools, switch to a mobile viewport (e.g. iPhone size). Confirm:
- The flyer fills the width without being cropped.
- Touch-dragging (simulate via dev tools touch emulation, or test on an actual phone) left/right switches slides.
- Arrow buttons and dots are still tappable and not overlapping the button text.

- [ ] **Step 4: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Add arrow/dot/swipe/keyboard controls to hero flyer carousel"
```

---

### Task 4: Full QA pass and push

**Files:**
- None (verification only, plus the site's existing pre-push audit)

**Interfaces:**
- Consumes: everything from Tasks 1–3.

- [ ] **Step 1: Run the full manual QA checklist**

With `index.html` open in a browser:
- [ ] Aug 22 slide is the default on page load.
- [ ] Aug 22 button href is exactly `https://bump-grind-r-b-party.bloomtickets.ca/event/2099?Bump%EF%BC%86Grind-R%EF%BC%86BAtTheMarquee` (right-click → Inspect, or hover and check the status bar).
- [ ] Season Pass button href is exactly `https://bump-grind-r-b-party.bloomtickets.ca/event/1878?B&G2026SeasonPass:All-Access` (the `&amp;` in source should render as a plain `&` in the actual link).
- [ ] Resize the browser from mobile width up to a large desktop width — the flyer never crops and the carousel never overflows horizontally.
- [ ] Scroll through the rest of the page (ticker, events, mixes, gallery) — nothing below the hero visually shifted or broke.
- [ ] Browser console shows zero errors on load and after clicking through both slides multiple times.

- [ ] **Step 2: Run the site's standard pre-push audit**

Per this repo's `CLAUDE.md`, run the four-pillar audit (UX/conversion, technical/performance, SEO/schema, roadmap) scoped to this diff before pushing. Pay particular attention to:
- Conversion flow: does the bigger button and default-Aug-22 slide clearly help the path to ticket purchase?
- Performance: confirm the two new flyer JPGs (under 450KB each) don't meaningfully increase page weight versus the 5.5MB photo they replaced.
- SEO: confirm `og:image`/JSON-LD `image` still correctly reference `BUMPANDGRIND-HERO-TOP.jpg` (untouched, per this plan's Global Constraints) and that the new `<img>` alt text is descriptive.

Present findings as a punch list; fix anything Critical before pushing, note High Impact / Long-Term items for TK to decide on.

- [ ] **Step 3: Push**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git push
```

If the change doesn't appear live on bumpandgrindhfx.com after the push, purge the Cloudflare cache (per this repo's `CLAUDE.md`).
